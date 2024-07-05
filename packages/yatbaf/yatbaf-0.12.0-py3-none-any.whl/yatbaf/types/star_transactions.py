from __future__ import annotations

from typing import final

from .abc import TelegramType
from .star_transaction import StarTransaction


@final
class StarTransactions(TelegramType):
    """Contains a list of Telegram Star transactions.

    See: https://core.telegram.org/bots/api#startransactions
    """

    transactions: list[StarTransaction]
    """The list of transactions."""
