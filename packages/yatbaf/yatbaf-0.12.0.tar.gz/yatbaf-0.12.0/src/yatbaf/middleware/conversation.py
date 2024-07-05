from __future__ import annotations

__all__ = ("ConversationMiddleware",)

from typing import TYPE_CHECKING
from typing import final

from yatbaf.helpers.conversation import ConversationContext

if TYPE_CHECKING:
    from yatbaf.state import State
    from yatbaf.types import Message
    from yatbaf.typing import FN


@final
class ConversationMiddleware:

    __slots__ = (
        "_fn",
        "_manager",
    )

    def __init__(self, fn: FN[Message], state: State) -> None:
        self._fn = fn
        self._manager = state

    async def __call__(self, message: Message) -> None:
        user_id = message.from_.id  # type: ignore[union-attr]
        chat_id = message.chat.id
        business_id = message.business_connection_id

        state = await self._manager.get(
            chat_id=chat_id,
            user_id=user_id,
            business_id=business_id,
        )
        message.ctx["conversation"] = ConversationContext(
            chat_id=chat_id,
            user_id=user_id,
            business_id=business_id,
            current_state=state,
            state_manager=self._manager,
        )
        await self._fn(message)
