from __future__ import annotations

from typing import final

from .abc import TelegramType
from .transaction_partner import TransactionPartner


@final
class StarTransaction(TelegramType):
    """Describes a Telegram Star transaction.

    See: https://core.telegram.org/bots/api#startransaction
    """

    id: str
    """Unique identifier of the transaction. Coincides with the identifer of
    the original transaction for refund transactions. Coincides with
    :attr:`~yatbaf.types.successful_payment.SuccessfulPayment.telegram_payment_charge_id`
    for successful incoming payments from users.
    """

    amount: int
    """Number of Telegram Stars transferred by the transaction."""

    date: int
    """Date the transaction was created in Unix time."""

    source: TransactionPartner | None = None
    """*Optional.* Source of an incoming transaction (e.g., a user purchasing
    goods or services, Fragment refunding a failed withdrawal).

    .. note::

        Only for incoming transactions.
    """

    receiver: TransactionPartner | None = None
    """*Optional.* Receiver of an outgoing transaction (e.g., a user for a
    purchase refund, Fragment for a withdrawal).

    .. note::

        Only for outgoing transactions.
    """
