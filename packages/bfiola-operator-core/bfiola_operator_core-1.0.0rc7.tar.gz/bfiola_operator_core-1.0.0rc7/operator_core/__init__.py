import asyncio
import contextlib
import functools
import inspect
import logging
import os
import pathlib
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    ClassVar,
    Coroutine,
    Generic,
    Protocol,
    TypeVar,
    cast,
)

import fastapi
import kopf
import kopf._cogs.structs.diffs
import kopf._core.intents.callbacks
import lightkube.config.kubeconfig
import lightkube.core.async_client
import lightkube.core.resource
import lightkube.core.resource_registry
import lightkube.generic_resource
import lightkube.models.meta_v1
import pydantic
import uvicorn


class OperatorError(Exception):
    """
    Defines a custom exception raised by this module.

    Used primarily to help identify known errors for proper error management.

    (NOTE: see `handle_hook_exception`)
    """

    recoverable: bool

    def __init__(self, message: str, recoverable: bool = False):
        super().__init__(message)
        self.recoverable = recoverable


ResourceSpec = TypeVar("ResourceSpec")


class Status(Generic[ResourceSpec]):
    """
    A generic data container for resource statuses.
    """

    # the currently applied spec for the resource (can differ from the resource 'spec' when an invalid edit is made)
    currentSpec: ResourceSpec | None


class ResourceMixin(Generic[ResourceSpec]):
    """
    Provides common resource fields and methods for *Resource classes.

    NOTE: `from_dict` and `to_dict` is required for the lightkube client to work - it replaces `lightkube.core.dataclasses_dict.DataclassDictMixIn`.
    """

    metadata: lightkube.models.meta_v1.ObjectMeta
    spec: ResourceSpec
    status: Status[ResourceSpec]

    apiVersion: ClassVar[str] = cast(str, None)
    kind: ClassVar[str] = cast(str, None)
    _immutable_fields: ClassVar[set[str]] = cast(set[str], None)
    _plural: ClassVar[str] = cast(str, None)
    _api_info: ClassVar[lightkube.core.resource.ApiInfo] = cast(lightkube.core.resource.ApiInfo, None)

    @classmethod
    def from_dict(cls, v, **kwargs):
        # use pydantic to automatically validate and parse an incoming object
        return cls(**v)

    def to_dict(self, **kwargs):
        # use pydantic to automatically dump the dataclass into a `dict` object.
        return pydantic.RootModel[self.__class__](self).model_dump()


def init_resource_subclass(cls: "type[NamespacedResource | GlobalResource]"):
    """
    Common __init_subclass__ routine for *Resource classes.

    - Validates that subclasses have defined apiVersion, kind and _plural attributes.
    - Creates the resource's _api_info metadata.
    - Registers the subclass with lightkube's resource registry
    """

    for attr in ("apiVersion", "kind", "_plural"):
        if getattr(cls, attr) is None:
            raise RuntimeError(f"{attr} undefined: {cls}")

    if cls._immutable_fields is None:
        cls._immutable_fields = set()

    group, version = cls.apiVersion.split("/")
    cls._api_info = lightkube.generic_resource.create_api_info(group, version, cls.kind, cls._plural)

    lightkube.core.resource_registry.resource_registry.register(cls)


class NamespacedResource(
    lightkube.core.resource.NamespacedResource,
    Generic[ResourceSpec],
    ResourceMixin[ResourceSpec],
):
    """
    Convenience base-class for namespaced resources.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        init_resource_subclass(cls)


class GlobalResource(
    lightkube.core.resource.GlobalResource,
    Generic[ResourceSpec],
    ResourceMixin[ResourceSpec],
):
    """
    Convenience base-class for global resources.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        init_resource_subclass(cls)


Resource = NamespacedResource | GlobalResource


SomeResource = TypeVar("SomeResource", bound=Resource, contravariant=True)


class ResourceCallback(Protocol[SomeResource]):
    async def __call__(self, resource: SomeResource, *, logger: kopf.Logger) -> None: ...


SomeCallable = TypeVar("SomeCallable", bound=Callable)


class Operator:
    """
    Implements a base operator class on which concrete operators can be built.
    """

    # health fastapi instance
    health_fastapi: fastapi.FastAPI
    # port used for health endpoint server
    health_port: int
    # a client capable of communcating with kubernetes
    kube_client: lightkube.core.async_client.AsyncClient
    # an (optional) path to a kubeconfig file
    kube_config: pathlib.Path | None
    # logger instance
    logger: logging.Logger
    # event signalling that the operator is ready
    ready_event: asyncio.Event
    # a kopf.OperatorRegistry instance enabling this operator to *not* run in the module scope
    registry: kopf.OperatorRegistry

    def __init__(
        self,
        *,
        health_port: int | None = None,
        kube_config: pathlib.Path | None = None,
        logger: logging.Logger,
    ):
        self.health_fastapi = fastapi.FastAPI()
        self.health_port = health_port or 8888
        self.kube_client = cast(lightkube.core.async_client.AsyncClient, None)
        self.kube_config = kube_config
        self.logger = logger
        self.ready_event = asyncio.Event()
        self.registry = kopf.OperatorRegistry()

        on_login = self.wrap_with_event_context("login", self.login)
        on_startup = self.wrap_with_event_context("startup", self.startup)
        kopf.on.login(registry=self.registry)(cast(Any, on_login))
        kopf.on.startup(registry=self.registry)(on_startup)

        self.health_fastapi.add_api_route("/healthz", self.health, methods=["GET"])

    def watch_resource(
        self,
        resource_cls: type[SomeResource],
        sync_callback: ResourceCallback[SomeResource],
        delete_callback: ResourceCallback[SomeResource],
    ) -> None:
        """
        Watches the given resource class by registering event listeners
        on several kubernetes resource events.
        """
        on_create = self.wrap_with_event_context(
            "create",
            functools.partial(self.resource_create, resource_cls=resource_cls, callback=sync_callback),
        )
        on_update = self.wrap_with_event_context(
            "update",
            functools.partial(self.resource_update, resource_cls=resource_cls, callback=sync_callback),
        )
        on_delete = self.wrap_with_event_context(
            "delete",
            functools.partial(
                self.resource_delete,
                resource_cls=resource_cls,
                callback=delete_callback,
            ),
        )

        group = resource_cls._api_info.resource.group
        version = resource_cls._api_info.resource.version
        plural = resource_cls._api_info.plural

        kopf.on.create(group, version, plural)(on_create)
        kopf.on.update(group, version, plural)(on_update)
        kopf.on.delete(group, version, plural)(on_delete)

    @contextlib.asynccontextmanager
    async def log_events(self, event: str, body: kopf.Body | None = None) -> AsyncGenerator[None, None]:
        """
        A context that logs the start/finish of operator events.
        """
        event_name = event
        if body:
            namespace = body["metadata"].get("namespace", "<cluster>")
            name = body["metadata"]["name"]
            event_name = f"{event_name}:{namespace}/{name}"

        try:
            self.logger.info(f"{event_name} started")
            yield
            self.logger.info(f"{event_name} completed")
        except Exception as e:
            if isinstance(e, kopf.TemporaryError):
                self.logger.error(f"{event_name} failed with retryable error: {e}")
            elif isinstance(e, kopf.PermanentError):
                self.logger.error(f"{event_name} failed with non-retryable error: {e}")
            else:
                # NOTE: assumes 'handle_event_exceptions' is called before this
                raise NotImplementedError(e)
            raise e

    @contextlib.asynccontextmanager
    async def handle_event_exceptions(self) -> AsyncGenerator[None, None]:
        """
        A context that catches, processes and re-raises processed exceptions
        """
        try:
            yield
        except Exception as base_exception:
            exception = self.wrap_exception(base_exception)
            raise exception from base_exception

    def wrap_with_event_context(
        self, event: str, callback: Callable[..., Coroutine[Any, Any, Any]]
    ) -> Callable[..., Coroutine[Any, Any, Any]]:
        """
        Wraps an operator event handler in a sequence of general contexts (e.g., error handling, logging)
        """

        signature = inspect.signature(callback)

        @functools.wraps(callback)
        async def inner(*args, **kwargs):
            async with contextlib.AsyncExitStack() as exit_stack:
                body = kwargs.get("body")
                await exit_stack.enter_async_context(self.log_events(event, body=body))
                await exit_stack.enter_async_context(self.handle_event_exceptions())
                _kwargs = {}
                for key in signature.parameters.keys():
                    if key not in kwargs:
                        continue
                    _kwargs[key] = kwargs[key]
                return await callback(**_kwargs)

        return inner

    async def login(self):
        """
        Authenticates the operator with kubernetes
        """
        if self.kube_config:
            self.logger.debug(f"kopf login using kubeconfig: {self.kube_config}")
            env = os.environ
            try:
                os.environ = dict(os.environ)
                os.environ["KUBECONFIG"] = f"{self.kube_config}"
                return kopf.login_with_kubeconfig()
            finally:
                os.environ = env
        else:
            self.logger.debug(f"kopf login using in-cluster")
            return kopf.login_with_service_account()

    async def startup(self):
        """
        Initializes the operator
        """
        kube_config = None
        if self.kube_config:
            kube_config = lightkube.config.kubeconfig.KubeConfig.from_file(self.kube_config)
        # TODO: remove when https://github.com/gtsystem/lightkube/pull/67 is published
        kube_config = cast(lightkube.config.kubeconfig.KubeConfig, kube_config)
        self.kube_client = lightkube.core.async_client.AsyncClient(kube_config)

    async def resource_create(
        self,
        *,
        resource_cls: type[SomeResource],
        callback: ResourceCallback[SomeResource],
        body: kopf.Body,
        patch: kopf.Patch,
        logger: kopf.Logger,
    ):
        """
        Called when a watched kubernetes resource is created
        """
        model = pydantic.RootModel[resource_cls].model_validate(body).root
        await callback(model, logger=logger)
        patch.status["currentSpec"] = model.to_dict()["spec"]

    def apply_diff_item(self, data: dict, diff_item: kopf.DiffItem):
        """
        Applies a diff item to the data object.

        Used during `resource_update` to incrementally update a resource.
        """
        new_data = dict(data)
        operation, field, old_value, new_value = diff_item
        if operation == "change":
            curr = new_data
            # traverse object parent fields
            for f in field[:-1]:
                curr = data[f]
            # set final field value
            field = field[-1]
            curr[field] = new_value
        else:
            raise NotImplementedError()
        return data

    async def resource_update(
        self,
        *,
        resource_cls: type[SomeResource],
        callback: ResourceCallback[SomeResource],
        immutable_fields: set[str],
        body: kopf.Body,
        patch: kopf.Patch,
        logger: kopf.Logger,
    ):
        """
        Called when a watched kubernetes resource is updated
        """
        if body["status"].get("currentSpec") is None:
            # retry resoure creation if previous attempts have failed
            return await self.resource_create(
                resource_cls=resource_cls,
                callback=callback,
                body=body,
                logger=logger,
                patch=patch,
            )

        # calculate the diff between the desired spec and the current spec
        current = dict(body["status"]["currentSpec"])
        desired = dict(body["spec"])
        diff_items = kopf._cogs.structs.diffs.diff(current, desired)

        # incrementally update the resource
        for diff_item in diff_items:
            if diff_item[1] in immutable_fields:
                # do not attempt to mutate immutable fields
                logger.info(f"ignoring immutable field: {diff_item[1]}")
                continue
            # apply diff item to create an updated model
            current = self.apply_diff_item(current, diff_item)
            data = dict(body)
            data.update({"spec": current})
            model = pydantic.RootModel[resource_cls].model_validate(data).root
            # perform the update
            await callback(model, logger=logger)
            # update status if update successful
            patch.status["currentSpec"] = current

    async def resource_delete(
        self,
        *,
        resource_cls: type[SomeResource],
        callback: ResourceCallback[SomeResource],
        body: kopf.Body,
        logger: kopf.Logger,
    ):
        """
        Called when a watched kubernetes resource is deleted
        """
        model = pydantic.RootModel[resource_cls].model_validate(body).root
        await callback(model, logger=logger)

    def wrap_exception(self, exception: Exception) -> kopf.TemporaryError | kopf.PermanentError:
        """
        Wraps an exception in either a kopf.TemporaryError or kopf.PermamentError and returns it

        NOTE: See `handle
        """
        wrapped_exception = kopf.TemporaryError(str(exception))
        if isinstance(exception, OperatorError):
            if not exception.recoverable:
                wrapped_exception = kopf.PermanentError(str(exception))
        elif isinstance(exception, pydantic.ValidationError):
            wrapped_exception = kopf.PermanentError(str(exception))
        return wrapped_exception

    async def health(self, response: fastapi.Response) -> fastapi.Response:
        """
        Health check, can be overridden - but recommended to call `super().health(response)`.

        Will return 200 if operator is ready, otherwise returns 500.
        """
        # if the operator isn't ready, set the status code to 500
        if not self.ready_event.is_set():
            response.status_code = 500
        # set the status code to 200 if unset
        response.status_code = response.status_code or 200

        passed = response.status_code == 200
        self.logger.debug(f"health check called (passed: {passed})")

        return response

    async def run(self):
        """
        Runs the operator - and blocks until exit.
        """

        class ServerConfig(uvicorn.Config):
            def configure_logging(self) -> None:
                pass

        # create healthcheck server
        server = uvicorn.Server(ServerConfig(app=self.health_fastapi, host="0.0.0.0", port=self.health_port))

        await asyncio.gather(
            kopf.operator(clusterwide=True, ready_flag=self.ready_event, registry=self.registry),
            server._serve(),
        )


__all__ = [
    "GlobalResource",
    "NamespacedResource",
    "OperatorError",
    "Operator",
]
