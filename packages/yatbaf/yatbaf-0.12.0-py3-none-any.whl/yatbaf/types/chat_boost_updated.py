from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramType
from .chat import Chat
from .chat_boost import ChatBoost

if TYPE_CHECKING:
    from yatbaf.bot import Bot


@final
class ChatBoostUpdated(TelegramType):
    """This object represents a boost added to a chat or changed.

    See: https://core.telegram.org/bots/api#chatboostupdated
    """

    chat: Chat
    """Chat which was boosted."""

    boost: ChatBoost
    """Infomation about the chat boost."""

    def _bind_bot_obj(self, bot: Bot) -> None:
        super()._bind_bot_obj(bot)
        self.chat._bind_bot_obj(bot)
        self.boost._bind_bot_obj(bot)
