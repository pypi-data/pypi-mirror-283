from __future__ import annotations

__all__ = ("ConversationContext",)

from typing import TYPE_CHECKING
from typing import final

if TYPE_CHECKING:
    from yatbaf.state import State


@final
class ConversationContext:
    """Helper object for manage conversation state.

    This object will be available inside a message handler::

        @on_message(...)
        async def message(m: Message) -> None:
            conv: ConversationContext = m.ctx["conversation"]
    """

    __slots__ = (
        "_chat_id",
        "_user_id",
        "_business_id",
        "_current_state",
        "_manager",
    )

    def __init__(
        self,
        chat_id: int,
        user_id: int,
        business_id: str | None,
        current_state: str | None,
        state_manager: State,
    ) -> None:
        """:meta private:

        :param chat_id: Current chat id.
        :param user_id: Current user id.
        :param business_id: Business connection id.
        :param current_state: Conversation state.
        :param state_manager: State manager
        """
        self._chat_id = chat_id
        self._user_id = user_id
        self._business_id = business_id
        self._current_state = current_state
        self._manager = state_manager

    @property
    def manager(self) -> State:
        """State manager."""
        return self._manager

    @property
    def current_state(self) -> str | None:
        """Current state."""
        return self._current_state

    async def set_state(self, state: str | None) -> None:
        """Set new state.

        :param state: New state. Pass ``None`` to reset state.
        """
        await self._manager.set(
            chat_id=self._chat_id,
            user_id=self._user_id,
            state=state,
            business_id=self._business_id,
        )

    async def get_data(self) -> str | None:
        """Get extra data for current user."""
        return await self._manager.get_data(
            chat_id=self._chat_id,
            user_id=self._user_id,
            business_id=self._business_id,
        )

    async def set_data(self, value: str | None) -> str | None:
        """Set extra data for current user.

        :param value: New data. Pass ``None`` to remove existing content.
        """
        await self._manager.set_data(
            chat_id=self._chat_id,
            user_id=self._user_id,
            value=value,
            business_id=self._business_id,
        )
        return value
