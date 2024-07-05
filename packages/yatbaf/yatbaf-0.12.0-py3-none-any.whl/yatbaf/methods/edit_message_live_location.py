from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import InlineKeyboardMarkup
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class EditMessageLiveLocation(TelegramMethod[Message | bool]):
    """See :meth:`yatbaf.bot.Bot.edit_message_live_location`"""

    latitude: float
    longitude: float
    chat_id: str | int | None = None
    business_connection_id: NoneStr = None
    message_id: NoneInt = None
    inline_message_id: NoneStr = None
    live_period: NoneInt = None
    horizontal_accuracy: float | None = None
    heading: NoneInt = None
    proximity_alert_radius: NoneInt = None
    reply_markup: InlineKeyboardMarkup | None = None
