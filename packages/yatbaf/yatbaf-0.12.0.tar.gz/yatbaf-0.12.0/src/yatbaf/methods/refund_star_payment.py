from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class RefundStarPayment(TelegramMethod[bool]):
    """See :meth:`~yatbaf.bot.Bot.refund_star_payment`."""

    user_id: int
    telegram_payment_charge_id: str
