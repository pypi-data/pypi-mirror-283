from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethodWithFile

if TYPE_CHECKING:
    from yatbaf.types import ReplyParameters
    from yatbaf.typing import InputFile
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr
    from yatbaf.typing import ReplyMarkup


@final
class SendSticker(TelegramMethodWithFile[Message]):
    """See :meth:`yatbaf.bot.Bot.send_sticker`"""

    chat_id: str | int
    sticker: InputFile | str
    business_connection_id: NoneStr = None
    message_thread_id: NoneInt = None
    emoji: NoneStr = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    message_effect_id: NoneStr = None
    reply_parameters: ReplyParameters | None = None
    reply_markup: ReplyMarkup | None = None

    __meth_file_fields__: ClassVar[tuple[str, ...]] = ("sticker",)
