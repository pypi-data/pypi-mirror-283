from __future__ import annotations

__all__ = (
    "AbstractClient",
    "AbstractRouter",
    "AbstractHandler",
    "AbstractStorage",
)

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Generic

from .typing import EventT

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from contextlib import AbstractAsyncContextManager

    from .client.models import HTTPResponse
    from .client.models import Request
    from .types import Update


class AbstractClient(ABC):
    """Abstract http client."""

    __slots__ = ()

    @abstractmethod
    async def send_post(
        self,
        request: Request,  # noqa: U100
        *,
        timeout: float | None = None  # noqa: U100
    ) -> HTTPResponse[bytes]:
        """Send POST request.

        :param request: :class:`~yatbaf.client.models.Request` instance.
        :param timeout: Request timeout.
        """

    @abstractmethod
    def file_stream(
        self,
        url: str,  # noqa: U100
        chunk_size: int,  # noqa: U100
    ) -> AbstractAsyncContextManager[HTTPResponse[AsyncIterator[bytes]]]:
        """Download file content.

        :param url: File URL.
        :param chunk_size: Chunk length in bytes.
        """

    @abstractmethod
    async def close(self) -> None:
        """Close the client."""


class AbstractRouter(ABC):
    __slots__ = ()

    @abstractmethod
    async def resolve(self, update: Update, /) -> None:
        """Process new update.

        :param update: :class:`~yatbaf.types.update.Update` instance.
        """


class AbstractHandler(ABC, Generic[EventT]):
    __slots__ = ()

    @abstractmethod
    async def handle(self, update: EventT, /) -> None:
        """Process the update.

        :param update: Event instance. See :class:`~yatbaf.types.update.Update`.
        """


class AbstractStorage(ABC):
    """Key-Value storage backend."""

    @abstractmethod
    async def get(self, key: str) -> str | None:
        """Get a value."""

    @abstractmethod
    async def set(self, key: str, value: str) -> None:
        """Set or update a value."""

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a value."""

    @abstractmethod
    async def clear(self) -> None:
        """Delete all values."""
