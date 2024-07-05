from __future__ import annotations

__all__ = (
    "HandlerGuard",
    "HandlerCallable",
    "HandlerMiddleware",
    "RouterGuard",
    "RouterCallable",
    "RouterMiddleware",
    "ResultT",
    "Handlers",
    "MiddlewareCallable",
    "EventT",
    "EventModel",
    "ReplyMarkup",
    "NoneStr",
    "NoneInt",
    "NoneBool",
)

from typing import TYPE_CHECKING
from typing import Any
from typing import Concatenate
from typing import Literal
from typing import ParamSpec
from typing import Protocol
from typing import TypeAlias
from typing import TypedDict
from typing import TypeVar
from typing import runtime_checkable

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from collections.abc import Awaitable
    from collections.abc import Callable

    from .abc import AbstractHandler
    from .bot import Bot
    from .middleware import Middleware
    from .types import BusinessConnection
    from .types import BusinessMessagesDeleted
    from .types import CallbackQuery
    from .types import ChatBoostRemoved
    from .types import ChatBoostUpdated
    from .types import ChatJoinRequest
    from .types import ChatMemberUpdated
    from .types import ChosenInlineResult
    from .types import ForceReply
    from .types import InlineKeyboardMarkup
    from .types import InlineQuery
    from .types import Message
    from .types import MessageReactionCountUpdated
    from .types import MessageReactionUpdated
    from .types import Poll
    from .types import PollAnswer
    from .types import PreCheckoutQuery
    from .types import ReplyKeyboardMarkup
    from .types import ReplyKeyboardRemove
    from .types import ShippingQuery
    from .types import Update
    from .types.abc import TelegramType

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")

EventT = TypeVar(
    "EventT",
    bound=(
        "CallbackQuery "
        "| ChatJoinRequest "
        "| ChatMemberUpdated "
        "| InlineQuery "
        "| ChosenInlineResult "
        "| Message "
        "| MessageReactionCountUpdated "
        "| MessageReactionUpdated "
        "| Poll "
        "| PollAnswer "
        "| PreCheckoutQuery "
        "| ShippingQuery "
        "| ChatBoostRemoved "
        "| ChatBoostUpdated "
        "| BusinessConnection "
        "| BusinessMessagesDeleted"
    )
)

ResultT = TypeVar("ResultT", bound="TelegramType | list | int | str | bool")

EventModel: TypeAlias = (
    "CallbackQuery "
    "| ChatJoinRequest "
    "| ChatMemberUpdated "
    "| InlineQuery "
    "| ChosenInlineResult "
    "| Message "
    "| MessageReactionCountUpdated "
    "| MessageReactionUpdated "
    "| Poll "
    "| PollAnswer "
    "| PreCheckoutQuery "
    "| ShippingQuery"
    "| ChatBoostRemoved"
    "| ChatBoostUpdated"
    "| BusinessConnection"
    "| BusinessMessagesDeleted"
)

ReplyMarkup: TypeAlias = (
    "ForceReply "
    "| InlineKeyboardMarkup "
    "| ReplyKeyboardMarkup "
    "| ReplyKeyboardRemove"
)

NoneStr: TypeAlias = "str | None"
NoneInt: TypeAlias = "int | None"
NoneBool: TypeAlias = "bool | None"

FN: TypeAlias = "Callable[[T], Awaitable[None]]"
WRP: TypeAlias = "Callable[[T], T]"
CONCAT: TypeAlias = "Callable[Concatenate[T, P], T]"

MiddlewareCallable: TypeAlias = "WRP[FN[T]]"

RouterCallable: TypeAlias = "FN[Update]"
RouterGuard: TypeAlias = "FN[Update]"
RouterMiddleware: TypeAlias = "Middleware[Update, Any] | MiddlewareCallable[Update]"  # noqa: E501

HandlerCallable: TypeAlias = "Callable[Concatenate[EventT, ...], Awaitable[None]]"  # noqa: E501
HandlerCallableType: TypeAlias = "FN[EventT]"
HandlerGuard: TypeAlias = "FN[EventT]"
HandlerMiddleware: TypeAlias = "Middleware[EventT, Any] | MiddlewareCallable[EventT]"  # noqa: E501
HandlerDependency: TypeAlias = (
    "Callable[..., Awaitable[Any]] "
    "| Callable[..., Any] "
    "| Callable[..., AsyncGenerator[Any, None]] "
    "| type[Any]"
)

Scope: TypeAlias = "Literal['group', 'handler', 'local']"

PollingHook: TypeAlias = "FN[Bot]"

FilterType: TypeAlias = "Literal['content', 'sender', 'chat']"
FilterPriority: TypeAlias = "dict[FilterType, tuple[int, int | tuple[int, int]]]"  # noqa: E501
FilterWeight: TypeAlias = "tuple[int, tuple[int, int]]"
HandlerPriority: TypeAlias = "tuple[FilterWeight, FilterWeight, FilterWeight]"


class Handlers(TypedDict):
    message: AbstractHandler[Message] | None
    edited_message: AbstractHandler[Message] | None
    channel_post: AbstractHandler[Message] | None
    edited_channel_post: AbstractHandler[Message] | None
    business_connection: AbstractHandler[BusinessConnection] | None
    business_message: AbstractHandler[Message] | None
    edited_business_message: AbstractHandler[Message] | None
    deleted_business_messages: AbstractHandler[BusinessMessagesDeleted] | None
    message_reaction: AbstractHandler[MessageReactionUpdated] | None
    message_reaction_count: AbstractHandler[MessageReactionCountUpdated] | None
    inline_query: AbstractHandler[InlineQuery] | None
    chosen_inline_result: AbstractHandler[ChosenInlineResult] | None
    callback_query: AbstractHandler[CallbackQuery] | None
    shipping_query: AbstractHandler[ShippingQuery] | None
    pre_checkout_query: AbstractHandler[PreCheckoutQuery] | None
    poll: AbstractHandler[Poll] | None
    poll_answer: AbstractHandler[PollAnswer] | None
    my_chat_member: AbstractHandler[ChatMemberUpdated] | None
    chat_member: AbstractHandler[ChatMemberUpdated] | None
    chat_join_request: AbstractHandler[ChatJoinRequest] | None
    chat_boost: AbstractHandler[ChatBoostUpdated] | None
    removed_chat_boost: AbstractHandler[ChatBoostRemoved] | None


@runtime_checkable
class InputFile(Protocol):
    """File protocol"""

    @property
    def file_name(self) -> str:
        """Name of file."""

    async def read(self) -> bytes:
        """Returns the file content."""
