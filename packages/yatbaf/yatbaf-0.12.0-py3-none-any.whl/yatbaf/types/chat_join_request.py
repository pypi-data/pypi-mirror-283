from __future__ import annotations

from typing import ClassVar
from typing import final

from msgspec import field

from yatbaf.typing import NoneStr

from .abc import TelegramType
from .chat import Chat
from .chat_invite_link import ChatInviteLink
from .user import User

# from datetime import datetime


@final
class ChatJoinRequest(TelegramType):
    """Represents a join request sent to a chat.

    See: https://core.telegram.org/bots/api#chatjoinrequest
    """

    chat: Chat
    """Chat to which the request was sent."""

    from_: User = field(name="from")
    """User that sent the join request."""

    user_chat_id: int
    """Identifier of a private chat with the user who sent the join request."""

    date: int  # TODO: datetime
    """Date the request was sent in Unix time."""

    bio: NoneStr = None
    """*Optional.* Bio of the user."""

    invite_link: ChatInviteLink | None = None
    """*Optional.* Chat invite link that was used by the user to send the join request."""  # noqa: E501

    __type_tg_fields__: ClassVar[tuple[str, ...]] = (
        "chat",
        "from_",
    )

    async def approve(self) -> bool:
        """See :meth:`~yatbaf.bot.Bot.approve_chat_join_request`"""
        return await self.bot.approve_chat_join_request(
            chat_id=self.chat.id,
            user_id=self.from_.id,
        )

    async def decline(self) -> bool:
        """See :meth:`~yatbaf.bot.Bot.decline_chat_join_request`"""
        return await self.bot.decline_chat_join_request(
            chat_id=self.chat.id,
            user_id=self.from_.id,
        )
