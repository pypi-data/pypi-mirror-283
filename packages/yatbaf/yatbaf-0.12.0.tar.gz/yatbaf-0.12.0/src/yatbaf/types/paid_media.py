from __future__ import annotations

__all__ = (
    "PaidMedia",
    "PaidMediaPreview",
    "PaidMediaPhoto",
    "PaidMediaVideo",
)

from typing import ClassVar
from typing import Literal
from typing import TypeAlias
from typing import final

from yatbaf.typing import NoneInt

from .abc import TelegramType
from .photo_size import PhotoSize
from .video import Video


@final
class PaidMediaPreview(TelegramType, tag="preview"):
    """The paid media isn't available before the payment.

    See: https://core.telegram.org/bots/api#paidmediapreview
    """

    width: NoneInt = None
    """*Optional.* Media width as defined by the sender."""

    height: NoneInt = None
    """*Optional.* Media height as defined by the sender."""

    duration: NoneInt = None
    """*Optional.* Duration of the media in seconds as defined by the sender."""

    type: ClassVar[Literal["preview"]] = "preview"
    """Type of the paid media, always `preview`."""


@final
class PaidMediaPhoto(TelegramType, tag="photo"):
    """The paid media is a photo.

    See: https://core.telegram.org/bots/api#paidmediaphoto
    """

    photo: list[PhotoSize]
    """The photo."""

    type: ClassVar[Literal["photo"]] = "photo"
    """Type of the paid media, always `photo`."""


@final
class PaidMediaVideo(TelegramType, tag="video"):
    """The paid media is a video.

    See: https://core.telegram.org/bots/api#paidmediavideo
    """

    video: Video
    """The video."""

    type: ClassVar[Literal["video"]] = "video"
    """Type of the paid media, always `video`."""


PaidMedia: TypeAlias = PaidMediaPreview | PaidMediaPhoto | PaidMediaVideo
"""This object describes paid media.

See: https://core.telegram.org/bots/api#paidmedia
"""
