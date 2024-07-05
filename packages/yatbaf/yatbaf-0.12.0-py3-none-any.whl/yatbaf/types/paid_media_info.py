from __future__ import annotations

from typing import final

from .abc import TelegramType
from .paid_media import PaidMedia


@final
class PaidMediaInfo(TelegramType):
    """Describes the paid media added to a message.

    See: https://core.telegram.org/bots/api#paidmediainfo
    """

    star_count: int
    """The number of Telegram Stars that must be paid to buy access to the media."""  # noqa: E501

    paid_media: list[PaidMedia]
    """Information about the paid media."""
