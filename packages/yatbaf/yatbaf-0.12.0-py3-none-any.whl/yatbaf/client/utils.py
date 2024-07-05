from __future__ import annotations

__all__ = (
    "build_decoder",
    "decode_content",
    "decode_error",
    "decode_response",
    "decode_webhook",
)

from typing import TYPE_CHECKING
from typing import TypeVar

from msgspec import DecodeError
from msgspec.json import Decoder

from yatbaf.exceptions import JSONDecodeError
from yatbaf.types import Update

from .models import ResponseError
from .models import ResponseOk

if TYPE_CHECKING:
    from collections.abc import Callable

    from yatbaf.methods.abc import TelegramMethod
    from yatbaf.typing import ResultT

    F = TypeVar("F", bound=Callable)

    def lru_cache(
        maxsize: int | None = 128,  # noqa: U100
        typed: bool = False,  # noqa: U100
    ) -> Callable[[F], F]:
        pass
else:
    from functools import lru_cache
    F = TypeVar("F")

T = TypeVar("T")


def decode_content(content: bytes, decoder: Decoder[T]) -> T:
    """Decode content.

    :meta private:
    :param content: Raw content.
    :param decoder: Decoder object.
    """

    try:
        return decoder.decode(content)
    except DecodeError as error:
        raise JSONDecodeError(
            message=str(error),
            raw_content=content,
        ) from None


@lru_cache(maxsize=None)
def build_decoder(model: type[T]) -> Decoder[T]:
    return Decoder(model)


def decode_response(
    method: TelegramMethod[ResultT],
    content: bytes,
    decoder: Decoder[ResponseOk[ResultT]] | None = None,
) -> ResponseOk[ResultT]:
    """Decode response content.

    :meta private:
    :param method: TelegramMethod object.
    :param content: Response raw content.
    :param decoder: *Optional.* Decoder object.
    """

    if decoder is None:
        model = method._get_result_model()
        decoder = build_decoder(ResponseOk[model])  # type: ignore[valid-type]
    return decode_content(content, decoder)


def decode_webhook(content: bytes) -> Update:
    """Decode webhook content.

    :meta private:
    :param content: Request raw content.
    """

    decoder = build_decoder(Update)
    return decode_content(content, decoder)


def decode_error(content: bytes) -> ResponseError:
    """Decode response error.

    :meta private:
    """

    decoder = build_decoder(ResponseError)
    return decode_content(content, decoder)
