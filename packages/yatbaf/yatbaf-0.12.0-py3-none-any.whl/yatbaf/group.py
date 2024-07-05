from __future__ import annotations

__all__ = (
    "OnMessage",
    "OnEditedMessage",
    "OnChannelPost",
    "OnEditedChannelPost",
    "OnBusinessConnection",
    "OnBusinessMessage",
    "OnEditedBusinessMessage",
    "OnDeletedBusinessMessages",
    "OnMessageReaction",
    "OnMessageReactionCount",
    "OnInlineQuery",
    "OnChosenInlineResult",
    "OnCallbackQuery",
    "OnShippingQuery",
    "OnPreCheckoutQuery",
    "OnPoll",
    "OnPollAnswer",
    "OnMyChatMember",
    "OnChatMember",
    "OnChatJoinRequest",
    "OnChatBoost",
    "OnRemovedChatBoost",
)

from collections import defaultdict
from itertools import count
from typing import TYPE_CHECKING
from typing import Final
from typing import ParamSpec
from typing import TypeVar
from typing import cast
from typing import final
from typing import overload

from .enums import Event
from .exceptions import FrozenInstanceError
from .exceptions import GuardException
from .handler import BaseHandler
from .handler import Handler
from .middleware import Middleware
from .types import BusinessConnection
from .types import BusinessMessagesDeleted
from .types import CallbackQuery
from .types import ChatBoostRemoved
from .types import ChatBoostUpdated
from .types import ChatJoinRequest
from .types import ChatMemberUpdated
from .types import ChosenInlineResult
from .types import InlineQuery
from .types import Message
from .types import MessageReactionCountUpdated
from .types import MessageReactionUpdated
from .types import Poll
from .types import PollAnswer
from .types import PreCheckoutQuery
from .types import ShippingQuery
from .typing import EventT
from .utils import wrap_middleware
from .warnings import warn_duplicate

if TYPE_CHECKING:
    from collections.abc import Iterable
    from collections.abc import Iterator
    from collections.abc import Sequence

    from .di import Provide
    from .filters.base import BaseFilter
    from .typing import CONCAT
    from .typing import FN
    from .typing import WRP
    from .typing import HandlerCallable
    from .typing import HandlerCallableType
    from .typing import HandlerGuard
    from .typing import HandlerMiddleware
    from .typing import Handlers
    from .typing import MiddlewareCallable
    from .typing import Scope

P = ParamSpec("P")
_group_count = count(1).__next__


class HandlerGroup(BaseHandler[EventT]):
    """Group of handlers."""

    __slots__ = (
        "_name",
        "_frozen",
        "_handlers",
        "_handler_guards",
        "_handler_middleware",
        "_middleware_stack",
        "_sort_handlers",
        "_stop_propagate",
    )

    def __init__(  # yapf: disable
        self,
        update_type: Event | str,
        *,
        filters: Sequence[BaseFilter[EventT]] | None = None,
        handlers: Sequence[BaseHandler[EventT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[EventT] | tuple[HandlerGuard[EventT], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[EventT] | tuple[HandlerMiddleware[EventT], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[EventT]] | None = None,
        middleware: Sequence[HandlerMiddleware[EventT]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        """
        :param update_type: Group type.
        :param handlers: *Optional.* A sequence of :class:`~yatbaf.handler.BaseHandler`.
        :param dependencies: *Optional.* A mapping of dependency providers.
        :param handler_guards: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerGuard`.
        :param handler_middleware: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerMiddleware`.
        :param guards: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerGuard`.
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerMiddleware`.
        :param name: *Optional.* HandlerGroup name.
        :param sort_handlers: *Optional.* Pass ``False``, if you don't want to
            sort handlers.
        :param stop_propagate: *Optional.* Pass ``True`` to stop propagate to
            next router even if no handler is found. Default ``bool(filters)``.
        """  # noqa: E501
        super().__init__(
            update_type=Event(update_type),
            filters=filters,
            guards=guards,
            middleware=middleware,
            dependencies=dependencies,
        )

        self._name: Final[str] = name if name else f"group-{_group_count()}"
        self._frozen = False
        self._middleware_stack: HandlerCallableType[EventT] = self._handle
        self._sort_handlers = sort_handlers
        self._stop_propagate = (
            stop_propagate if stop_propagate is not None else bool(filters)
        )

        self._handler_guards = list(handler_guards or [])
        self._handler_middleware = list(handler_middleware or [])

        self._handlers: list[BaseHandler[EventT]] = []
        for handler in (handlers or []):
            self.add_handler(handler)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}[name={self._name}]>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, HandlerGroup) and (  # yapf: disable
            other is self or (
                other.update_type == self.update_type
                and other._handlers == self._handlers
                and other._handler_guards == self._handler_guards
                and other._handler_middleware == self._handler_middleware
                and other._guards == self._guards
                and other._middleware == self._middleware
                and other._dependencies == self._dependencies
            )
        )

    @property
    def name(self) -> str:
        """Group name."""
        return self._name

    def add_filter(self, filter: BaseFilter[EventT], /) -> None:
        """Add new filter to group.

        :param filter: Filter object.
        """
        self._filters.append(filter)

    def add_guard(
        self, obj: HandlerGuard[EventT], /, scope: Scope = "handler"
    ) -> None:
        """Add a new guard.

        :param obj: :class:`~yatbaf.typing.HandlerGuard` object.
        :param scope: *Optional.* Scope of guard.
        :raises FrozenInstanceError: If you try to register a Guard after Bot
            object has been initialized.
        """
        if self._frozen:
            raise FrozenInstanceError(
                "It is not possible to add a new Guard at runtime "
                "after Bot object has been initialized."
            )

        if scope == "group":
            self._guards.append(obj)
        else:
            self._handler_guards.append(
                obj if scope != "local" else (obj, "local")
            )

    def add_middleware(  # yapf: disable
        self, obj: HandlerMiddleware[EventT], /, scope: Scope = "handler"
    ) -> None:
        """Add a new middleware.

        Usage::

            def middleware(
                handler: HandlerCallableType[EventT]
            ) -> HandlerCallableType[EventT]:
                async def wrapper(update: EventT) -> None:
                    await handler(update)
                return wrapper

            group.add_middleware(middleware)

        :param obj: :class:`~yatbaf.typing.HandlerMiddleware` object.
        :param scope: *Optional.* Scope of middleware.
        :raises FrozenInstanceError: If you try to register a Middleware after
            Bot object has been initialized.
        """  # noqa: E501
        if self._frozen:
            raise FrozenInstanceError(
                "It is not possible to add a new Middleware at runtime "
                "after Bot object has been initialized."
            )

        if scope == "group":
            self._middleware.append(obj)
        else:
            self._handler_middleware.append(
                obj if scope != "local" else (obj, "local")
            )

    @overload
    def add_handler(self, handler: BaseHandler[EventT], /) -> None:
        ...

    @overload
    def add_handler(
        self,
        handler: HandlerCallable[EventT],
        *,
        filters: Sequence[BaseFilter[EventT]] | None = None,
        middleware: Sequence[HandlerMiddleware[EventT]] | None = None,
        guards: Sequence[HandlerGuard[EventT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        ...

    def add_handler(  # yapf: disable
        self,
        handler: HandlerCallable[EventT] | BaseHandler[EventT],
        *,
        filters: Sequence[BaseFilter[EventT]] | None = None,
        middleware: Sequence[HandlerMiddleware[EventT]] | None = None,
        guards: Sequence[HandlerGuard[EventT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        """Use this method to register a new handler or group.

        :param handler: :class:`~yatbaf.handler.Handler`, :class:`~yatbaf.typing.HandlerCallable`
            or :class:`~yatbaf.router.HandlerGroup`.
        :param filters: *Optional.* A sequence of :class:`~yatbaf.filters.base.BaseFilter`.
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerMiddleware`.
        :param guards: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerGuard`.
        :param dependencies: *Optional.* A mapping of dependency providers.
        :raises FrozenInstanceError: If you try to register a Handler after Bot
            object has been initialized.
        """  # noqa: E501
        if self._frozen:
            raise FrozenInstanceError(
                f"{self!r} is frozen. It is not possible to add a new Handler "
                "at runtime after Bot object has been initialized."
            )

        if not issubclass(type(handler), BaseHandler):
            handler = Handler(
                fn=handler,  # type: ignore[arg-type]
                update_type=self.update_type,
                filters=filters,
                middleware=middleware,
                guards=guards,
                dependencies=dependencies,
            )
        handler = cast("BaseHandler[EventT]", handler)

        self._validate_handler(handler)
        if handler.parent or (handler in self._handlers):
            warn_duplicate(handler, self)
            return

        self._handlers.append(handler)
        handler.parent = self

    def _validate_handler(self, handler: BaseHandler[EventT]) -> None:
        if handler is self:
            raise ValueError(
                f"It is not possible to add {handler!r} to itself."
            )

        if handler.update_type != self.update_type:
            raise ValueError(
                f"Incompatible type! Cannot add {handler!r} to {self!r}"
            )

        if (parent := handler.parent) and parent is not self:
            raise ValueError(f"{handler!r} alredy registered in {parent!r}")

    @overload
    def __call__(  # yapf: disable
        self, __fn: HandlerCallable[EventT], /
    ) -> HandlerCallable[EventT]:
        ...

    @overload
    def __call__(
        self,
        *,
        filters: Sequence[BaseFilter[EventT]] | None = None,
        middleware: Sequence[HandlerMiddleware[EventT]] | None = None,
        guards: Sequence[HandlerGuard[EventT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> MiddlewareCallable[EventT]:
        ...

    def __call__(  # yapf: disable
        self,
        __fn: HandlerCallable[EventT] | None = None,
        *,
        filters: Sequence[BaseFilter[EventT]] | None = None,
        middleware: Sequence[HandlerMiddleware[EventT]] | None = None,
        guards: Sequence[HandlerGuard[EventT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> MiddlewareCallable[EventT] | HandlerCallable[EventT]:
        """Handler decorator.

        See :meth:`add_handler`.

        Use this decorator to register a new handler::

            @router
            async def handler(message):
                # handle any message
                ...


            @router(filters=[Command("foo")])
            async def handler(message):
                # handle command `/foo`
                ...
        """

        def wrapper(fn: HandlerCallable[EventT]) -> HandlerCallable[EventT]:
            self.add_handler(
                handler=fn,
                filters=filters,
                middleware=middleware,
                guards=guards,
                dependencies=dependencies,
            )
            return fn

        if __fn is not None:
            return wrapper(__fn)
        return wrapper

    # yapf: disable
    @overload
    def middleware(self, __fn: WRP[FN[EventT]], /) -> WRP[FN[EventT]]:
        ...

    @overload
    def middleware(
        self,
        __scope: Scope, /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> WRP[CONCAT[FN[EventT], P]]:
        ...

    def middleware(
        self,
        __fn_scope: CONCAT[FN[EventT], P] | Scope = "handler", /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> WRP[CONCAT[FN[EventT], P]] | WRP[FN[EventT]]:
        """Middleware decorator.

        Use this decorator to register a new middleware::

            @group.middleware
            def middleware(
                handler: HandlerCallableType[Message]
            ) -> HandlerCallableType[Message]:
                async def wrapper(message: Message) -> None:
                    await handler(message)
                return wrapper


            @group.middleware("handler", 1, y="data")
            def middleware(
                handler: HandlerCallableType[Message],
                x: int,
                y: str,
            ) -> HandlerCallableType[Message]:
                async def wrapper(message: Message) -> None:
                    log.info(f"{x=}, {y=}")
                    await handler(message)
                return wrapper
        """  # noqa: E501
        # yapf: enable

        def wrapper(fn: CONCAT[FN[EventT], P]) -> CONCAT[FN[EventT], P]:
            scope = cast("Scope", __fn_scope)
            if args or kwargs:
                self.add_middleware(Middleware(fn, *args, **kwargs), scope)
            else:
                self.add_middleware(fn, scope)
            return fn

        if not isinstance(__fn_scope, str):
            fn = __fn_scope
            __fn_scope = "handler"
            return wrapper(fn)
        return wrapper

    # yapf: disable
    @overload
    def guard(self, __fn: HandlerGuard[EventT], /) -> HandlerGuard[EventT]:
        ...

    @overload
    def guard(self, __scope: Scope, /) -> WRP[HandlerGuard[EventT]]:
        ...

    def guard(
        self, __fn_scope: HandlerGuard[EventT] | Scope = "handler"
    ) -> HandlerGuard[EventT] | WRP[HandlerGuard[EventT]]:
        """Guard decorator.

        Use this decorator to register a guard for handlers or group::

            users = [...]

            @group.guard
            async def guard(message: Message) -> None:
                if message.from_.id not in users:
                    raise GuardException


            @group.guard("group")
            async def guard(message: Message) -> None:
                if message.from_.id not in users:
                    raise GuardException
        """
        # yapf: enable

        def wrapper(fn: HandlerGuard[EventT]) -> HandlerGuard[EventT]:
            scope: Scope = __fn_scope  # type: ignore[assignment]
            self.add_guard(fn, scope)
            return fn

        if not isinstance(__fn_scope, str):
            fn = __fn_scope
            __fn_scope = "handler"
            return wrapper(fn)
        return wrapper

    async def handle(self, update: EventT, /) -> None:
        if not self._filters or await self.match(update):
            await self._middleware_stack(update)

    async def _handle(self, update: EventT, /) -> None:
        try:
            if self._guards:
                await self._check_guards(update)
        except GuardException:
            update.__usrctx__["handled"] = self._stop_propagate
            return

        for handler in self._handlers:
            await handler.handle(update)
            if update.__usrctx__["handled"]:
                return

        # skip other routers
        update.__usrctx__["handled"] = self._stop_propagate

    def _get_guards(  # yapf: disable
        self, exclude_locals: bool
    ) -> Iterable[HandlerGuard[EventT]]:
        return _unpack(self._handler_guards, exclude_locals)

    def _get_middleware(  # yapf: disable
        self, exclude_locals: bool
    ) -> Iterable[HandlerMiddleware[EventT]]:
        return _unpack(self._handler_middleware, exclude_locals)

    def _prepare_handlers(self) -> None:
        for handler in self._handlers:
            handler.on_registration()

        if self._sort_handlers:
            self._handlers.sort(reverse=True)

    def on_registration(self) -> None:
        self._resolve_filters()
        self._prepare_handlers()
        self._resolve_guards()
        self._resolve_middleware()

        self._middleware_stack = wrap_middleware(self._handle, self._middleware)
        self._frozen = True


T = TypeVar("T")


def _unpack(
    objs: Sequence[T | tuple[T, str]],
    exclude_local: bool = False,
) -> Iterator[T]:
    for obj in objs:
        scope = ""
        if isinstance(obj, tuple):
            obj, scope = obj
            if scope == "local" and exclude_local:
                continue
        yield cast("T", obj)


@final
class OnMessage(HandlerGroup[Message]):
    """message group.

    See :attr:`Update.message <yatbaf.types.update.Update.message>`
    """

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        handlers: Sequence[BaseHandler[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[Message] | tuple[HandlerGuard[Message], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[Message] | tuple[HandlerMiddleware[Message], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.MESSAGE,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnEditedMessage(HandlerGroup[Message]):
    """edited_message group.

    See :attr:`Update.edited_message <yatbaf.types.update.Update.edited_message>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        handlers: Sequence[BaseHandler[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[Message] | tuple[HandlerGuard[Message], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[Message] | tuple[HandlerMiddleware[Message], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.EDITED_MESSAGE,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnChannelPost(HandlerGroup[Message]):
    """channel_post group.

    See :attr:`Update.channel_post <yatbaf.types.update.Update.channel_post>`
    """

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        handlers: Sequence[BaseHandler[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[Message] | tuple[HandlerGuard[Message], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[Message] | tuple[HandlerMiddleware[Message], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CHANNEL_POST,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnEditedChannelPost(HandlerGroup[Message]):
    """edited_channel_post group.

    See :attr:`Update.edited_channel_post <yatbaf.types.update.Update.edited_channel_post>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        handlers: Sequence[BaseHandler[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[Message] | tuple[HandlerGuard[Message], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[Message] | tuple[HandlerMiddleware[Message], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.EDITED_CHANNEL_POST,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnBusinessConnection(HandlerGroup[BusinessConnection]):
    """business_connection group.

    See :attr:`~yatbaf.types.update.Update.business_connection`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[BusinessConnection]] | None = None,
        handlers: Sequence[BaseHandler[BusinessConnection]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[BusinessConnection] | tuple[HandlerGuard[BusinessConnection], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[BusinessConnection] | tuple[HandlerMiddleware[BusinessConnection], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[BusinessConnection]] | None = None,
        middleware: Sequence[HandlerMiddleware[BusinessConnection]] | None = None,  # noqa: E501
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.BUSINESS_CONNECTION,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnBusinessMessage(HandlerGroup[Message]):
    """business_message group.

    See :attr:`~yatbaf.types.update.Update.business_message`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        handlers: Sequence[BaseHandler[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[Message] | tuple[HandlerGuard[Message], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[Message] | tuple[HandlerMiddleware[Message], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.BUSINESS_MESSAGE,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnEditedBusinessMessage(HandlerGroup[Message]):
    """edited_business_message group.

    See :attr:`~yatbaf.types.update.Update.edited_business_message`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        handlers: Sequence[BaseHandler[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[Message] | tuple[HandlerGuard[Message], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[Message] | tuple[HandlerMiddleware[Message], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.EDITED_BUSINESS_MESSAGE,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnDeletedBusinessMessages(HandlerGroup[BusinessMessagesDeleted]):
    """deleted_business_messages group.

    See :attr:`~yatbaf.types.update.Update.deleted_business_messages`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[BusinessMessagesDeleted]] | None = None,
        handlers: Sequence[BaseHandler[BusinessMessagesDeleted]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[BusinessMessagesDeleted] | tuple[HandlerGuard[BusinessMessagesDeleted], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[BusinessMessagesDeleted] | tuple[HandlerMiddleware[BusinessMessagesDeleted], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[BusinessMessagesDeleted]] | None = None,
        middleware: Sequence[HandlerMiddleware[BusinessMessagesDeleted]] | None = None,  # noqa: E501
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.DELETED_BUSINESS_MESSAGES,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnMessageReaction(HandlerGroup[MessageReactionUpdated]):
    """message_reaction group.

    See :attr:`Update.message_reaction <yatbaf.types.update.Update.message_reaction>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[MessageReactionUpdated]] | None = None,
        handlers: Sequence[BaseHandler[MessageReactionUpdated]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[MessageReactionUpdated] | tuple[HandlerGuard[MessageReactionUpdated], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[MessageReactionUpdated] | tuple[HandlerMiddleware[MessageReactionUpdated], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[MessageReactionUpdated]] | None = None,
        middleware: Sequence[HandlerMiddleware[MessageReactionUpdated]] | None = None,  # noqa: E501
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.MESSAGE_REACTION,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnMessageReactionCount(HandlerGroup[MessageReactionCountUpdated]):
    """message_reaction group.

    See :attr:`Update.message_reaction_count <yatbaf.types.update.Update.message_reaction_count>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[MessageReactionCountUpdated]] | None = None,  # noqa: E501
        handlers: Sequence[BaseHandler[MessageReactionCountUpdated]] | None = None,  # noqa: E501
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[MessageReactionCountUpdated] | tuple[HandlerGuard[MessageReactionCountUpdated], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[MessageReactionCountUpdated] | tuple[HandlerMiddleware[MessageReactionCountUpdated], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[MessageReactionCountUpdated]] | None = None,  # noqa: E501
        middleware: Sequence[HandlerMiddleware[MessageReactionCountUpdated]] | None = None,  # noqa: E501
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.MESSAGE_REACTION_COUNT,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnInlineQuery(HandlerGroup[InlineQuery]):
    """inline_query group.

    See :attr:`Update.inline_query <yatbaf.types.update.Update.inline_query>`
    """

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[InlineQuery]] | None = None,
        handlers: Sequence[BaseHandler[InlineQuery]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[InlineQuery] | tuple[HandlerGuard[InlineQuery], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[InlineQuery] | tuple[HandlerMiddleware[InlineQuery], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[InlineQuery]] | None = None,
        middleware: Sequence[HandlerMiddleware[InlineQuery]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.INLINE_QUERY,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnChosenInlineResult(HandlerGroup[ChosenInlineResult]):
    """chosen_inline_result group.

    See :attr:`Update.chosen_inline_result <yatbaf.types.update.Update.chosen_inline_result>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[ChosenInlineResult]] | None = None,
        handlers: Sequence[BaseHandler[ChosenInlineResult]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[ChosenInlineResult] | tuple[HandlerGuard[ChosenInlineResult], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[ChosenInlineResult] | tuple[HandlerMiddleware[ChosenInlineResult], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[ChosenInlineResult]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChosenInlineResult]] | None = None,  # noqa: E501
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CHOSEN_INLINE_RESULT,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnCallbackQuery(HandlerGroup[CallbackQuery]):
    """callback_query group.

    See :attr:`Update.callback_query <yatbaf.types.update.Update.callback_query>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[CallbackQuery]] | None = None,
        handlers: Sequence[BaseHandler[CallbackQuery]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[CallbackQuery] | tuple[HandlerGuard[CallbackQuery], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[CallbackQuery] | tuple[HandlerMiddleware[CallbackQuery], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[CallbackQuery]] | None = None,
        middleware: Sequence[HandlerMiddleware[CallbackQuery]] | None = None,  # noqa: E501
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CALLBACK_QUERY,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnShippingQuery(HandlerGroup[ShippingQuery]):
    """shipping_query group.

    See :attr:`Update.shipping_query <yatbaf.types.update.Update.shipping_query>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[ShippingQuery]] | None = None,
        handlers: Sequence[BaseHandler[ShippingQuery]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[ShippingQuery] | tuple[HandlerGuard[ShippingQuery], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[ShippingQuery] | tuple[HandlerMiddleware[ShippingQuery], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[ShippingQuery]] | None = None,
        middleware: Sequence[HandlerMiddleware[ShippingQuery]] | None = None,  # noqa: E501
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.SHIPPING_QUERY,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnPreCheckoutQuery(HandlerGroup[PreCheckoutQuery]):
    """pre_checkout_query group.

    See :attr:`Update.pre_checkout_query <yatbaf.types.update.Update.pre_checkout_query>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[PreCheckoutQuery]] | None = None,
        handlers: Sequence[BaseHandler[PreCheckoutQuery]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[PreCheckoutQuery] | tuple[HandlerGuard[PreCheckoutQuery], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[PreCheckoutQuery] | tuple[HandlerMiddleware[PreCheckoutQuery], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[PreCheckoutQuery]] | None = None,
        middleware: Sequence[HandlerMiddleware[PreCheckoutQuery]] | None = None,  # noqa: E501
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.PRE_CHECKOUT_QUERY,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnPoll(HandlerGroup[Poll]):
    """poll group.

    See :attr:`Update.poll <yatbaf.types.update.Update.poll>`
    """

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[Poll]] | None = None,
        handlers: Sequence[BaseHandler[Poll]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[Poll] | tuple[HandlerGuard[Poll], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[Poll] | tuple[HandlerMiddleware[Poll], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[Poll]] | None = None,
        middleware: Sequence[HandlerMiddleware[Poll]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.POLL,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnPollAnswer(HandlerGroup[PollAnswer]):
    """poll_answer group.

    See :attr:`Update.poll_answer <yatbaf.types.update.Update.poll_answer>`
    """

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[PollAnswer]] | None = None,
        handlers: Sequence[BaseHandler[PollAnswer]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[PollAnswer] | tuple[HandlerGuard[PollAnswer], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[PollAnswer] | tuple[HandlerMiddleware[PollAnswer], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[PollAnswer]] | None = None,
        middleware: Sequence[HandlerMiddleware[PollAnswer]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.POLL_ANSWER,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnMyChatMember(HandlerGroup[ChatMemberUpdated]):
    """my_chat_member group.

    See :attr:`Update.my_chat_member <yatbaf.types.update.Update.my_chat_member>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[ChatMemberUpdated]] | None = None,
        handlers: Sequence[BaseHandler[ChatMemberUpdated]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[ChatMemberUpdated] | tuple[HandlerGuard[ChatMemberUpdated], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[ChatMemberUpdated] | tuple[HandlerMiddleware[ChatMemberUpdated], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[ChatMemberUpdated]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChatMemberUpdated]] | None = None,  # noqa: E501
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.MY_CHAT_MEMBER,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnChatMember(HandlerGroup[ChatMemberUpdated]):
    """chat_member group.

    See :attr:`Update.chat_member <yatbaf.types.update.Update.chat_member>`
    """

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[ChatMemberUpdated]] | None = None,
        handlers: Sequence[BaseHandler[ChatMemberUpdated]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[ChatMemberUpdated] | tuple[HandlerGuard[ChatMemberUpdated], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[ChatMemberUpdated] | tuple[HandlerMiddleware[ChatMemberUpdated], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[ChatMemberUpdated]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChatMemberUpdated]] | None = None,  # noqa: E501
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CHAT_MEMBER,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnChatJoinRequest(HandlerGroup[ChatJoinRequest]):
    """chat_join_request group.

    See :attr:`Update.chat_join_request <yatbaf.types.update.Update.chat_join_request>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[ChatJoinRequest]] | None = None,
        handlers: Sequence[BaseHandler[ChatJoinRequest]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[ChatJoinRequest] | tuple[HandlerGuard[ChatJoinRequest], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[ChatJoinRequest] | tuple[HandlerMiddleware[ChatJoinRequest], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[ChatJoinRequest]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChatJoinRequest]] | None = None,  # noqa: E501
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CHAT_JOIN_REQUEST,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnChatBoost(HandlerGroup[ChatBoostUpdated]):
    """chat_boost group.

    See :attr:`Update.chat_boost <yatbaf.types.update.Update.chat_boost>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[ChatBoostUpdated]] | None = None,
        handlers: Sequence[BaseHandler[ChatBoostUpdated]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[ChatBoostUpdated] | tuple[HandlerGuard[ChatBoostUpdated], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[ChatBoostUpdated] | tuple[HandlerMiddleware[ChatBoostUpdated], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[ChatBoostUpdated]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChatBoostUpdated]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CHAT_BOOST,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


@final
class OnRemovedChatBoost(HandlerGroup[ChatBoostRemoved]):
    """removed_chat_boost group.

    See :attr:`Update.removed_chat_boost <yatbaf.types.update.Update.removed_chat_boost>`
    """  # noqa: E501

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[ChatBoostRemoved]] | None = None,
        handlers: Sequence[BaseHandler[ChatBoostRemoved]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[ChatBoostRemoved] | tuple[HandlerGuard[ChatBoostRemoved], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[ChatBoostRemoved] | tuple[HandlerMiddleware[ChatBoostRemoved], Scope]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[ChatBoostRemoved]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChatBoostRemoved]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.REMOVED_CHAT_BOOST,
            filters=filters,
            handlers=handlers,
            dependencies=dependencies,
            handler_guards=handler_guards,
            handler_middleware=handler_middleware,
            guards=guards,
            middleware=middleware,
            name=name,
            sort_handlers=sort_handlers,
            stop_propagate=stop_propagate,
        )


def parse_handlers(
    handlers: Sequence[BaseHandler],
    dependencies: dict[str, Provide] | None = None,
) -> Handlers:
    """:meta private:"""
    dependencies = dependencies or {}
    tmp: dict[str, list[BaseHandler]] = defaultdict(lambda: [])
    for handler_ in handlers:
        tmp[handler_.update_type].append(handler_)

    result = {}
    for type_, h in tmp.items():
        handler: BaseHandler
        if len(h) == 1:
            handler = h[0]
            handler._dependencies = {**dependencies, **handler._dependencies}
        else:
            handler = HandlerGroup(
                update_type=type_,
                handlers=h,
                dependencies=dependencies,
            )
        result[type_] = handler
        handler.on_registration()

    return cast("Handlers", result)
