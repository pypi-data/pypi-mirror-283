from __future__ import annotations

__all__ = (
    "RevenueWithdrawalState",
    "RevenueWithdrawalStatePending",
    "RevenueWithdrawalStateSucceeded",
    "RevenueWithdrawalStateFailed",
)

from typing import ClassVar
from typing import TypeAlias
from typing import final

from .abc import TelegramType


@final
class RevenueWithdrawalStatePending(TelegramType, tag="pending"):
    """The withdrawal is in progress.

    See: https://core.telegram.org/bots/api#revenuewithdrawalstatepending
    """

    type: ClassVar[str] = "pending"
    """Type of the state, always `pending`."""


@final
class RevenueWithdrawalStateSucceeded(TelegramType, tag="succeeded"):
    """The withdrawal succeeded.

    See: https://core.telegram.org/bots/api#revenuewithdrawalstatesucceeded
    """

    date: int
    """Date the withdrawal was completed in Unix time."""

    url: str
    """An HTTPS URL that can be used to see transaction details."""

    type: ClassVar[str] = "succeeded"
    """Type of the state, always `succeeded`."""


@final
class RevenueWithdrawalStateFailed(TelegramType, tag="failed"):
    """The withdrawal failed and the transaction was refunded.

    See: https://core.telegram.org/bots/api#revenuewithdrawalstatefailed
    """

    type: ClassVar[str] = "failed"
    """Type of the state, always `failed`."""


RevenueWithdrawalState: TypeAlias = (
    RevenueWithdrawalStatePending
    | RevenueWithdrawalStateSucceeded
    | RevenueWithdrawalStateFailed
)
"""This object describes the state of a revenue withdrawal operation.

See: https://core.telegram.org/bots/api#revenuewithdrawalstate
"""
