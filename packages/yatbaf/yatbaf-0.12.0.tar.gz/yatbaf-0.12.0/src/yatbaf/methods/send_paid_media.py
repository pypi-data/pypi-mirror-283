from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethodWithMedia

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.types import InputPaidMedia
    from yatbaf.types import MessageEntity
    from yatbaf.types import ReplyParameters
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneStr
    from yatbaf.typing import ReplyMarkup


@final
class SendPaidMedia(TelegramMethodWithMedia[Message]):
    """See :meth:`~yatbaf.bot.Bot.send_paid_media`"""

    chat_id: int | str
    star_count: int
    media: list[InputPaidMedia]
    caption: NoneStr = None
    parse_mode: ParseMode | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: NoneBool = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_parameters: ReplyParameters | None = None
    reply_markup: ReplyMarkup | None = None
