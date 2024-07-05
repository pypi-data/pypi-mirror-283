from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import ReplyParameters
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr
    from yatbaf.typing import ReplyMarkup


@final
class SendVenue(TelegramMethod[Message]):
    """See :meth:`yatbaf.bot.Bot.send_venue`"""

    chat_id: str | int
    latitude: float
    longitude: float
    title: str
    address: str
    business_connection_id: NoneStr = None
    message_thread_id: NoneInt = None
    foursquare_id: NoneStr = None
    foursquare_type: NoneStr = None
    google_place_id: NoneStr = None
    google_place_type: NoneStr = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    message_effect_id: NoneStr = None
    reply_parameters: ReplyParameters | None = None
    reply_markup: ReplyMarkup | None = None
