from __future__ import annotations

__all__ = (
    "TransactionPartner",
    "TransactionPartnerFragment",
    "TransactionPartnerUser",
    "TransactionPartnerTelegramAds",
    "TransactionPartnerOther",
)

from typing import ClassVar
from typing import TypeAlias
from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType
from .revenue_withdrawal_state import RevenueWithdrawalState
from .user import User


@final
class TransactionPartnerFragment(TelegramType, tag="fragment"):
    """Describes a withdrawal transaction with Fragment.

    See: https://core.telegram.org/bots/api#transactionpartnerfragment
    """

    withdrawal_state: RevenueWithdrawalState | None = None
    """*Optional.* State of the transaction if the transaction is outgoing."""

    type: ClassVar[str] = "fragment"
    """Type of the transaction partner, always `fragment`."""


@final
class TransactionPartnerUser(TelegramType, tag="user"):
    """Describes a transaction with a user.

    See: https://core.telegram.org/bots/api#transactionpartneruser
    """

    user: User
    """Information about the user."""

    invoice_payload: NoneStr = None
    """*Optional.* Bot-specified invoice payload."""

    type: ClassVar[str] = "user"
    """Type of the transaction partner, always `user`."""


@final
class TransactionPartnerTelegramAds(TelegramType, tag="telegram_ads"):
    """Describes a withdrawal transaction to the Telegram Ads platform.

    See: https://core.telegram.org/bots/api#transactionpartnertelegramads
    """

    type: ClassVar[str] = "telegram_ads"
    """Type of the transaction partner, always `telegram_ads`."""


@final
class TransactionPartnerOther(TelegramType, tag="other"):
    """Describes a transaction with an unknown source or recipient.

    See: https://core.telegram.org/bots/api#transactionpartnerother
    """

    type: ClassVar[str] = "other"
    """Type of the transaction partner, always `other`."""


TransactionPartner: TypeAlias = (
    TransactionPartnerFragment
    | TransactionPartnerUser
    | TransactionPartnerTelegramAds
    | TransactionPartnerOther
)
"""This object describes the source of a transaction, or its recipient for
outgoing transactions.

See: https://core.telegram.org/bots/api#transactionpartner
"""
