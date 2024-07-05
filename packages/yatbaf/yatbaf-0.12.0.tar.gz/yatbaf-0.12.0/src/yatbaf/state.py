from __future__ import annotations

__all__ = ("State",)

from typing import TYPE_CHECKING
from typing import final

from .storage import Memory

if TYPE_CHECKING:
    from .abc import AbstractStorage


@final
class State:
    """State manager."""

    __slots__ = ("_storage",)

    def __init__(self, *, storage: AbstractStorage | None = None) -> None:
        """
        :param storage: *Optional.* Storage backend.
            :class:`~yatbaf.storage.Memory` by default.
        """
        self._storage = Memory() if storage is None else storage

    async def _set(self, key: str, value: str | None) -> None:
        if value is None:
            await self._storage.delete(key)
        else:
            await self._storage.set(key, value)

    async def set(
        self,
        chat_id: int,
        user_id: int,
        state: str | None,
        *,
        business_id: str | None = None,
    ) -> None:
        """Set new state.

        :param chat_id: Chat id.
        :param user_id: User id.
        :param state: New state. Pass ``None`` to reset state.
        :param business_id: *Optional.* Business connection id.
        """
        await self._set(
            (
                f"s:{chat_id}.{user_id}" +
                (f".{business_id}" if business_id is not None else "")
            ),
            state,
        )

    async def get(
        self,
        chat_id: int,
        user_id: int,
        *,
        business_id: str | None = None,
    ) -> str | None:
        """Get current state.

        :param chat_id: Chat id.
        :param user_id: User id.
        :param business_id: *Optional.* Business connection id.
        """
        return await self._storage.get(
            f"s:{chat_id}.{user_id}" +
            (f".{business_id}" if business_id is not None else "")
        )

    async def set_data(
        self,
        chat_id: int,
        user_id: int,
        value: str | None,
        *,
        business_id: str | None = None,
    ) -> None:
        """Set extra data.

        :param chat_id: Chat id.
        :param user_id: User id.
        :param business_id: *Optional.* Business connection id.
        """
        await self._set(
            (
                f"d:{chat_id}.{user_id}" +
                (f".{business_id}" if business_id is not None else "")
            ),
            value,
        )

    async def get_data(
        self,
        chat_id: int,
        user_id: int,
        *,
        business_id: str | None = None,
    ) -> str | None:
        """Get extra data.

        :param chat_id: Chat id.
        :param user_id: User id.
        :param business_id: *Optional.* Business connection id.
        """
        return await self._storage.get(
            f"d:{chat_id}.{user_id}" +
            (f".{business_id}" if business_id is not None else "")
        )
