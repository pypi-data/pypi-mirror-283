from __future__ import annotations

__all__ = (
    "InputPaidMedia",
    "InputPaidMediaPhoto",
    "InputPaidMediaVideo",
)

from typing import ClassVar
from typing import Literal
from typing import TypeAlias
from typing import final

from yatbaf.typing import InputFile
from yatbaf.typing import NoneBool
from yatbaf.typing import NoneInt

from .abc import TelegramType


@final
class InputPaidMediaPhoto(TelegramType, tag="photo"):
    """The paid media to send is a photo.

    See: https://core.telegram.org/bots/api#inputpaidmediaphoto
    """

    media: InputFile | str
    """File to send."""

    type: ClassVar[Literal["photo"]] = "photo"
    """Type of the media, must be `photo`."""

    __type_file_fields__: ClassVar[tuple[str, ...]] = ("media",)


@final
class InputPaidMediaVideo(TelegramType, tag="video"):
    """The paid media to send is a video.

    See: https://core.telegram.org/bots/api#inputpaidmediavideo
    """

    media: InputFile | str
    """File to send."""

    thumbnail: InputFile | str | None = None
    """*Optional.* Thumbnail of the file sent; can be ignored if thumbnail
    generation for the file is supported server-side. The thumbnail should be
    in JPEG format and less than 200 kB in size. A thumbnail's width and height
    should not exceed 320.
    """

    width: NoneInt = None
    """*Optional.* Video width."""

    height: NoneInt = None
    """*Optional.* Video height."""

    duration: NoneInt = None
    """*Optional.* Video duration in seconds."""

    supports_streaming: NoneBool = None
    """*Optional.* Pass ``True`` if the uploaded video is suitable for streaming."""  # noqa: E501

    type: ClassVar[Literal["video"]] = "video"
    """Type of the media, must be `video`."""

    __type_file_fields__: ClassVar[tuple[str, ...]] = ("media",)


InputPaidMedia: TypeAlias = InputPaidMediaPhoto | InputPaidMediaVideo
"""This object describes the paid media to be sent.

See: https://core.telegram.org/bots/api#inputpaidmedia
"""
