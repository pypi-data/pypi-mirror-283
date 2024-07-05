from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethodWithFile

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.types import MessageEntity
    from yatbaf.types import ReplyParameters
    from yatbaf.typing import InputFile
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr
    from yatbaf.typing import ReplyMarkup


@final
class SendAnimation(TelegramMethodWithFile[Message]):
    """See :meth:`yatbaf.bot.Bot.send_animation`"""

    chat_id: str | int
    animation: InputFile | str
    business_connection_id: NoneStr = None
    message_thread_id: NoneInt = None
    duration: NoneInt = None
    width: NoneInt = None
    height: NoneInt = None
    thumbnail: InputFile | str | None = None
    caption: NoneStr = None
    parse_mode: ParseMode | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: NoneBool = None
    has_spoiler: NoneBool = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    message_effect_id: NoneStr = None
    reply_parameters: ReplyParameters | None = None
    reply_markup: ReplyMarkup | None = None

    __meth_file_fields__: ClassVar[tuple[str, ...]] = (
        "animation",
        "thumbnail",
    )
