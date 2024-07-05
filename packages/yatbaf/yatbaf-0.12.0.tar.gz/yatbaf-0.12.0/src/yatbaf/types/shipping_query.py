from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from msgspec import field

from .abc import TelegramType
from .shipping_address import ShippingAddress
from .user import User

if TYPE_CHECKING:
    from yatbaf.bot import Bot


@final
class ShippingQuery(TelegramType):
    """This object contains information about an incoming shipping query.

    See: https://core.telegram.org/bots/api#shippingquery
    """

    id: str
    """Unique query identifier."""

    from_: User = field(name="from")
    """User who sent the query."""

    invoice_payload: str
    """Bot specified invoice payload."""

    shipping_address: ShippingAddress
    """User specified shipping address."""

    def _bind_bot_obj(self, bot: Bot) -> None:
        super()._bind_bot_obj(bot)
        self.from_._bind_bot_obj(bot)
