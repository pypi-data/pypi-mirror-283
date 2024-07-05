from __future__ import annotations

__all__ = (
    "Handler",
    "on_message",
    "on_edited_message",
    "on_channel_post",
    "on_business_connection",
    "on_business_message",
    "on_edited_business_message",
    "on_deleted_business_messages",
    "on_edited_channel_post",
    "on_message_reaction",
    "on_message_reaction_count",
    "on_inline_query",
    "on_chosen_inline_result",
    "on_callback_query",
    "on_shipping_query",
    "on_pre_checkout_query",
    "on_poll",
    "on_poll_answer",
    "on_my_chat_member",
    "on_chat_member",
    "on_chat_join_request",
    "on_chat_boost",
    "on_removed_chat_boost",
)

from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Self
from typing import final

from .abc import AbstractHandler
from .di import Provide
from .di import create_dependency_batches
from .di import create_dependency_graph
from .di import get_parameters
from .di import is_reserved_key
from .di import resolve_dependencies
from .di import validate_provider
from .enums import Event
from .exceptions import GuardException
from .filters.base import check_compatibility
from .filters.base import merge_priority
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
from .utils import ensure_unique
from .utils import wrap_middleware

if TYPE_CHECKING:
    from collections.abc import Iterable
    from collections.abc import Sequence

    from .di import Dependency
    from .filters.base import BaseFilter
    from .typing import FilterPriority
    from .typing import HandlerCallable
    from .typing import HandlerCallableType
    from .typing import HandlerGuard
    from .typing import HandlerMiddleware
    from .typing import HandlerPriority


class BaseHandler(AbstractHandler[EventT]):

    __slots__ = (
        "parent",
        "_guards",
        "_filters",
        "_middleware",
        "_filters",
        "_priority",
        "_dependencies",
        "_update_type",
    )

    parent: BaseHandler[EventT] | None

    def __init__(
        self,
        update_type: Event,
        filters: Sequence[BaseFilter[EventT]] | None = None,
        guards: Sequence[HandlerGuard[EventT]] | None = None,
        middleware: Sequence[HandlerMiddleware[EventT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        """
        :param update_type: Handler type. See :class:`~yatbaf.enums.Event`
        :param filters: *Optional.* A sequence of :class:`~yatbaf.filters.base.BaseFilter`.
        :param guards: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerGuard`.
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerMiddleware`.
        :param dependencies: *Optional.* A mapping of dependency providers.
        """  # noqa: E501
        self.parent: BaseHandler[EventT] | None = None
        self._filters = list(filters or [])
        self._guards = list(guards or [])
        self._middleware = list(middleware or [])
        # content, user, chat
        self._priority: HandlerPriority = (
            (0, (0, 0)),
            (0, (0, 0)),
            (0, (0, 0)),
        )
        self._dependencies = dependencies or {}
        self._update_type = update_type

    @final
    def __bool__(self) -> bool:
        return True

    @final
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, BaseHandler):
            return NotImplemented

        s_prior = self._priority
        o_prior = other._priority

        # priority (max, min) [content, sender, chat]
        sp = (s_prior[0][1], s_prior[1][1], s_prior[2][1])
        op = (o_prior[0][1], o_prior[1][1], o_prior[2][1])

        # priority max [content, sender, chat]
        sp_max = (sp[0][0], sp[1][0], sp[2][0])
        op_max = (op[0][0], op[1][0], op[2][0])

        # priority min [content, sender, chat]
        sp_min = (sp[0][1], sp[1][1], sp[2][1])
        op_min = (op[0][1], op[1][1], op[2][1])

        # number of filters [chat, sender, content]
        ss = (s_prior[2][0], s_prior[1][0], s_prior[0][0])
        os = (o_prior[2][0], o_prior[1][0], o_prior[0][0])

        if sp_max == op_max:
            if ss == os:
                return sp_min < op_min
            return ss < os
        return sp_max < op_max

    @final
    def __gt__(self, other: object) -> bool:  # noqa: U100
        return NotImplemented

    @property
    def update_type(self) -> Event:
        """Handler type."""
        return self._update_type

    async def _check_guards(self, update: EventT) -> None:
        for guard in self._guards:
            await guard(update)

    async def match(self, update: EventT, /) -> bool:
        for filter in self._filters:
            if not await filter.check(update):
                return False
        return True

    def _resolve_middleware(self) -> None:
        self._middleware = ensure_unique(self._middleware)

    def _resolve_guards(self) -> None:
        self._guards = ensure_unique(self._guards)

    def _resolve_filters(self) -> None:
        check_compatibility(self._filters, False)
        self._priority = self._parse_priority(self._filters)

    @staticmethod
    def _parse_priority(filters: Sequence[BaseFilter]) -> HandlerPriority:
        data: FilterPriority = {}
        for filter in filters:
            data = merge_priority(data, filter.priority)

        tmp: list[tuple[int, tuple[int, int]]] = []
        for group in ("content", "sender", "chat"):
            if priority := data.get(group):  # type: ignore[call-overload]
                if isinstance(min_max := priority[1], int):
                    tmp.append((priority[0], (min_max, min_max)))
                else:
                    tmp.append(priority)
            else:
                tmp.append((0, (0, 0)))
        return tuple(tmp)  # type: ignore[return-value]

    def _get_guards(
        self, exclude_locals: bool  # noqa: U100
    ) -> Iterable[HandlerGuard[EventT]]:   # yapf: disable
        return self._guards

    def _get_middleware(
        self, exclude_locals: bool  # noqa: U100
    ) -> Iterable[HandlerMiddleware[EventT]]:  # yapf: disable
        return self._middleware

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @abstractmethod
    def on_registration(self) -> None:
        """Init handler."""


class Handler(BaseHandler[EventT]):
    """Handler object."""

    __slots__ = (
        "_fn",
        "_middleware_stack",
        "_resolved_dependencies",
        "_kwargs",
    )

    def __init__(
        self,
        update_type: Event | str,
        *,
        fn: HandlerCallable[EventT] | None = None,
        filters: Sequence[BaseFilter[EventT]] | None = None,
        guards: Sequence[HandlerGuard[EventT]] | None = None,
        middleware: Sequence[HandlerMiddleware[EventT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        """
        :param fn: Handler callback.
        :param update_type: Handler type. See :class:`~yatbaf.enums.Event`
        :param filters: *Optional.* A sequence of :class:`~yatbaf.filters.base.BaseFilter`.
        :param guards: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerGuard`.
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerMiddleware`.
        :param dependencies: *Optional.* A mapping of dependency providers.
        """  # noqa: E501
        super().__init__(
            update_type=Event(update_type),
            filters=filters,
            guards=guards,
            middleware=middleware,
            dependencies=dependencies,
        )

        self._fn = fn
        self._kwargs = self._get_fn_kwargs(fn) if fn else set()
        self._middleware_stack: HandlerCallableType[EventT] = self._handle
        self._resolved_dependencies: list[set[Dependency]] = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}[type={self._update_type!s},id=0x{id(self):x}]>"  # noqa: E501

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Handler) and (  # yapf: disable
            other is self or (
                # type, fn, middleware and deps
                other._update_type == self._update_type
                and other._fn is self._fn
                and other._middleware == self._middleware
                and other._dependencies == self._dependencies
            )
        )

    def __call__(self, fn: HandlerCallable[EventT]) -> Self:
        self._fn = fn
        self._kwargs = self._get_fn_kwargs(fn)
        return self

    @staticmethod
    def _get_fn_kwargs(fn: HandlerCallable[EventT]) -> set[str]:
        return set(get_parameters(fn)[1:])

    @property
    def fn(self) -> HandlerCallable[EventT]:
        """Original function."""
        if self._fn is None:
            raise ValueError(f"{self!r}: callback is not set.")
        return self._fn

    async def handle(self, update: EventT, /) -> None:
        if not self._filters or await self.match(update):
            # handler found -> update handled
            update.__usrctx__["handled"] = True

            await self._middleware_stack(update)

    async def _handle(self, update: EventT, /) -> None:
        try:
            if self._guards:
                await self._check_guards(update)
        except GuardException:
            return

        await self._exec(update)

    async def _exec(self, update: EventT, /) -> None:
        """Resolve dependencies, exec callback."""
        if not self._kwargs:
            await self._fn(update)  # type: ignore[misc]
            return

        values = {"update": update}
        cg = await resolve_dependencies(self._resolved_dependencies, values)
        kwargs = {k: values[k] for k in self._kwargs}

        try:
            await self._fn(update, **kwargs)  # type: ignore[misc]
        except Exception as e:
            await cg.throw(e)
            raise

        await cg.cleanup()

    @property
    def _parents(self) -> list[BaseHandler[EventT]]:
        result: list[BaseHandler[EventT]] = []
        parent: BaseHandler[EventT] | None = self
        while parent is not None:
            result.append(parent)
            parent = parent.parent
        return list(reversed(result))

    def _resolve_guards(self) -> None:
        guards: list[HandlerGuard[EventT]] = []
        for parent in self._parents:
            guards.extend(parent._get_guards(parent is not self.parent))
        self._guards = ensure_unique(guards)

    def _resolve_middleware(self) -> None:
        middleware: list[HandlerMiddleware[EventT]] = []
        for parent in self._parents:
            middleware.extend(parent._get_middleware(parent is not self.parent))
        self._middleware_stack = wrap_middleware(
            self._handle,
            ensure_unique(middleware),
        )

    def _resolve_dependencies(self) -> None:
        if kwargs := self._kwargs:
            providers = self._get_dependency_providers()
            dependencies = set()
            for key in kwargs:
                if not is_reserved_key(key):
                    dependencies.add(create_dependency_graph(key, providers))
            batches = create_dependency_batches(dependencies)
            self._resolved_dependencies = batches

    def _get_dependency_providers(self) -> dict[str, Provide]:
        providers: dict[str, Provide] = {}
        for parent in self._parents:
            if (d := parent._dependencies) is not None:
                for k, v in d.items():
                    validate_provider(k, v, providers)
                    providers[k] = v
        return providers

    def on_registration(self) -> None:
        self.fn  # callback exists or error
        self._resolve_guards()
        self._resolve_middleware()
        self._resolve_filters()
        self._resolve_dependencies()


@final
class on_message(Handler[Message]):
    """Message handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[Message] | None = None,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        guards: Sequence[HandlerGuard[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.MESSAGE,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_edited_message(Handler[Message]):
    """Edited message handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[Message] | None = None,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        guards: Sequence[HandlerGuard[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.EDITED_MESSAGE,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_message_reaction(Handler[MessageReactionUpdated]):
    """Message reaction handler."""

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        fn: HandlerCallable[MessageReactionUpdated] | None = None,
        *,
        filters: Sequence[BaseFilter[MessageReactionUpdated]] | None = None,
        middleware: Sequence[HandlerMiddleware[MessageReactionUpdated]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[MessageReactionUpdated]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.MESSAGE_REACTION,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_message_reaction_count(Handler[MessageReactionCountUpdated]):
    """Message reaction count handler."""

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        fn: HandlerCallable[MessageReactionCountUpdated] | None = None,
        *,
        filters: Sequence[BaseFilter[MessageReactionCountUpdated]] | None = None,  # noqa: E501
        middleware: Sequence[HandlerMiddleware[MessageReactionCountUpdated]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[MessageReactionCountUpdated]] | None = None,  # noqa: E501
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.MESSAGE_REACTION_COUNT,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_channel_post(Handler[Message]):
    """Channel post handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[Message] | None = None,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        guards: Sequence[HandlerGuard[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CHANNEL_POST,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_edited_channel_post(Handler[Message]):
    """Edited channel post handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[Message] | None = None,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        guards: Sequence[HandlerGuard[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.EDITED_CHANNEL_POST,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_inline_query(Handler[InlineQuery]):
    """Inline query handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[InlineQuery] | None = None,
        *,
        filters: Sequence[BaseFilter[InlineQuery]] | None = None,
        middleware: Sequence[HandlerMiddleware[InlineQuery]] | None = None,
        guards: Sequence[HandlerGuard[InlineQuery]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.INLINE_QUERY,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_chosen_inline_result(Handler[ChosenInlineResult]):
    """Chosen inline result handler."""

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        fn: HandlerCallable[ChosenInlineResult] | None = None,
        *,
        filters: Sequence[BaseFilter[ChosenInlineResult]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChosenInlineResult]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[ChosenInlineResult]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CHOSEN_INLINE_RESULT,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_callback_query(Handler[CallbackQuery]):
    """Callback query handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[CallbackQuery] | None = None,
        *,
        filters: Sequence[BaseFilter[CallbackQuery]] | None = None,
        middleware: Sequence[HandlerMiddleware[CallbackQuery]] | None = None,
        guards: Sequence[HandlerGuard[CallbackQuery]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CALLBACK_QUERY,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_shipping_query(Handler[ShippingQuery]):
    """Shipping query handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[ShippingQuery] | None = None,
        *,
        filters: Sequence[BaseFilter[ShippingQuery]] | None = None,
        middleware: Sequence[HandlerMiddleware[ShippingQuery]] | None = None,
        guards: Sequence[HandlerGuard[ShippingQuery]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.SHIPPING_QUERY,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_pre_checkout_query(Handler[PreCheckoutQuery]):
    """Pre-checkout query handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[PreCheckoutQuery] | None = None,
        *,
        filters: Sequence[BaseFilter[PreCheckoutQuery]] | None = None,
        middleware: Sequence[HandlerMiddleware[PreCheckoutQuery]] | None = None,
        guards: Sequence[HandlerGuard[PreCheckoutQuery]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.PRE_CHECKOUT_QUERY,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_poll(Handler[Poll]):
    """Poll handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[Poll] | None = None,
        *,
        filters: Sequence[BaseFilter[Poll]] | None = None,
        middleware: Sequence[HandlerMiddleware[Poll]] | None = None,
        guards: Sequence[HandlerGuard[Poll]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.POLL,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_poll_answer(Handler[PollAnswer]):
    """Poll answer handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[PollAnswer] | None = None,
        *,
        filters: Sequence[BaseFilter[PollAnswer]] | None = None,
        middleware: Sequence[HandlerMiddleware[PollAnswer]] | None = None,
        guards: Sequence[HandlerGuard[PollAnswer]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.POLL_ANSWER,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_my_chat_member(Handler[ChatMemberUpdated]):
    """My chat member handler."""

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        fn: HandlerCallable[ChatMemberUpdated] | None = None,
        *,
        filters: Sequence[BaseFilter[ChatMemberUpdated]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChatMemberUpdated]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[ChatMemberUpdated]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.MY_CHAT_MEMBER,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_chat_member(Handler[ChatMemberUpdated]):
    """Chat member handler."""

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        fn: HandlerCallable[ChatMemberUpdated] | None = None,
        *,
        filters: Sequence[BaseFilter[ChatMemberUpdated]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChatMemberUpdated]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[ChatMemberUpdated]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CHAT_MEMBER,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_chat_join_request(Handler[ChatJoinRequest]):
    """Chat join request handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[ChatJoinRequest] | None = None,
        *,
        filters: Sequence[BaseFilter[ChatJoinRequest]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChatJoinRequest]] | None = None,
        guards: Sequence[HandlerGuard[ChatJoinRequest]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CHAT_JOIN_REQUEST,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_chat_boost(Handler[ChatBoostUpdated]):
    """Chat boost handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[ChatBoostUpdated] | None = None,
        *,
        filters: Sequence[BaseFilter[ChatBoostUpdated]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChatBoostUpdated]] | None = None,
        guards: Sequence[HandlerGuard[ChatBoostUpdated]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.CHAT_BOOST,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_removed_chat_boost(Handler[ChatBoostRemoved]):
    """Removed chat boost handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[ChatBoostRemoved] | None = None,
        *,
        filters: Sequence[BaseFilter[ChatBoostRemoved]] | None = None,
        middleware: Sequence[HandlerMiddleware[ChatBoostRemoved]] | None = None,
        guards: Sequence[HandlerGuard[ChatBoostRemoved]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.REMOVED_CHAT_BOOST,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_business_connection(Handler[BusinessConnection]):
    """Business connection handler."""

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        fn: HandlerCallable[BusinessConnection] | None = None,
        *,
        filters: Sequence[BaseFilter[BusinessConnection]] | None = None,
        middleware: Sequence[HandlerMiddleware[BusinessConnection]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[BusinessConnection]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.BUSINESS_CONNECTION,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_business_message(Handler[Message]):
    """Business message handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[Message] | None = None,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        guards: Sequence[HandlerGuard[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.BUSINESS_MESSAGE,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_edited_business_message(Handler[Message]):
    """Edited business message handler."""

    __slots__ = ()

    def __init__(
        self,
        fn: HandlerCallable[Message] | None = None,
        *,
        filters: Sequence[BaseFilter[Message]] | None = None,
        middleware: Sequence[HandlerMiddleware[Message]] | None = None,
        guards: Sequence[HandlerGuard[Message]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.EDITED_BUSINESS_MESSAGE,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )


@final
class on_deleted_business_messages(Handler[BusinessMessagesDeleted]):
    """Deleted business messages handler."""

    __slots__ = ()

    def __init__(  # yapf: disable
        self,
        fn: HandlerCallable[BusinessMessagesDeleted] | None = None,
        *,
        filters: Sequence[BaseFilter[BusinessMessagesDeleted]] | None = None,
        middleware: Sequence[HandlerMiddleware[BusinessMessagesDeleted]] | None = None,  # noqa: E501
        guards: Sequence[HandlerGuard[BusinessMessagesDeleted]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        super().__init__(
            update_type=Event.DELETED_BUSINESS_MESSAGES,
            fn=fn,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
