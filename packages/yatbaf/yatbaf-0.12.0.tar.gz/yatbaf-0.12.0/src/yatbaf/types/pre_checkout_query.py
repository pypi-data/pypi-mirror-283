from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from msgspec import field

from yatbaf.typing import NoneStr

from .abc import TelegramType
from .order_info import OrderInfo
from .user import User

if TYPE_CHECKING:
    from yatbaf.bot import Bot


@final
class PreCheckoutQuery(TelegramType):
    """This object contains information about an incoming pre-checkout query.

    See: https://core.telegram.org/bots/api#precheckoutquery
    """

    id: str
    """Unique query identifier."""

    from_: User = field(name="from")
    """User who sent the query."""

    currency: str
    """Three-letter ISO 4217 currency code."""

    total_amount: int
    """Total price in the smallest units of the currency.

    .. important::

        Integer, not float/double.
    """

    invoice_payload: str
    """Bot specified invoice payload."""

    shipping_option_id: NoneStr = None
    """*Optional.* Identifier of the shipping option chosen by the user."""

    order_info: OrderInfo | None = None
    """*Optional.* Order information provided by the user."""

    def _bind_bot_obj(self, bot: Bot) -> None:
        super()._bind_bot_obj(bot)
        self.from_._bind_bot_obj(bot)

    async def answer(self, ok: bool, error_message: NoneStr = None) -> bool:
        """See: :meth:`answer_pre_checkout_query <yatbaf.bot.Bot.answer_pre_checkout_query>`"""  # noqa: E501

        return await self.bot.answer_pre_checkout_query(
            pre_checkout_query_id=self.id,
            ok=ok,
            error_message=error_message,
        )

    async def approve(self) -> bool:
        """Approve qeury.

        See :meth:`~yatbaf.bot.Bot.answer_pre_checkout_query`.
        """
        return await self.bot.answer_pre_checkout_query(
            pre_checkout_query_id=self.id,
            ok=True,
        )

    async def cancel(self, message: str) -> bool:
        """Cancel query.

        See :meth:`~yatbaf.bot.Bot.answer_pre_checkout_query`.

        :param message: Error message in human readable form that explains the
        reason for failure to proceed with the checkout. Telegram will display
        this message to the user.
        """
        return await self.bot.answer_pre_checkout_query(
            pre_checkout_query_id=self.id,
            ok=False,
            error_message=message,
        )
