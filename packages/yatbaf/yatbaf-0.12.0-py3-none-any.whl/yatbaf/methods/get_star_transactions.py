from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import StarTransactions

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneInt


@final
class GetStarTransactions(TelegramMethod[StarTransactions]):
    """See: :meth:`yatbaf.bot.Bot.get_star_transactions`"""

    offset: NoneInt = None
    limit: NoneInt = None
