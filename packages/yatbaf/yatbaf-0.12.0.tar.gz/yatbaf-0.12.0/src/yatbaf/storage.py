from __future__ import annotations

__all__ = ("Memory",)

from typing import final

from .abc import AbstractStorage


@final
class Memory(AbstractStorage):
    """In-memory storage."""

    __slots__ = ("_data",)

    def __init__(self) -> None:
        self._data: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        return self._data.get(key)

    async def set(self, key: str, value: str) -> None:
        self._data[key] = value

    async def delete(self, key: str) -> None:
        self._data.pop(key, None)

    async def clear(self) -> None:
        self._data.clear()
