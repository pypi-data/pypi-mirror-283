from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramType
from .chat import Chat

if TYPE_CHECKING:
    from yatbaf.bot import Bot


@final
class BusinessMessagesDeleted(TelegramType):
    """This object is received when messages are deleted from a connected
    business account.

    See: https://core.telegram.org/bots/api#businessmessagesdeleted
    """

    business_connection_id: str
    """Unique identifier of the business connection."""

    chat: Chat
    """Information about a chat in the business account. The bot may not have
    access to the chat or the corresponding user.
    """

    message_ids: list[int]
    """List of identifiers of deleted messages in the chat of the business
    account.
    """

    def _bind_bot_obj(self, bot: Bot) -> None:
        super()._bind_bot_obj(bot)
        self.chat._bind_bot_obj(bot)
