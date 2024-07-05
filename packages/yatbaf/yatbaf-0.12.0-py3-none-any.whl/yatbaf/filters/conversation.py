from __future__ import annotations

__all__ = (
    "ActiveConversation",
    "ConversationState",
)

from typing import TYPE_CHECKING

from yatbaf.filters import BaseFilter

if TYPE_CHECKING:
    from yatbaf.types import Message


class ConversationState(BaseFilter):
    __slots__ = (
        "_state",
        "_priority",
    )

    def __init__(self, state: str, *, priority: int = 100) -> None:
        self._state = state
        self._priority = priority

    @property
    def priority(self) -> int:
        return self._priority

    async def check(self, update: Message) -> bool:
        return update.ctx["conversation"].current_state == self._state


class ActiveConversation(BaseFilter):
    __slots__ = ("_priority",)

    def __init__(self, *, priority: int = 2000) -> None:
        self._priority = priority

    @property
    def priority(self) -> int:
        return self._priority

    async def check(self, update: Message) -> bool:
        return update.ctx["conversation"].current_state is not None
