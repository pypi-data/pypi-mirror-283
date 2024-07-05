from __future__ import annotations

__all__ = ("Middleware",)

from typing import TYPE_CHECKING
from typing import Concatenate
from typing import Generic
from typing import ParamSpec
from typing import TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

    from yatbaf.typing import FN

T = TypeVar("T")
P = ParamSpec("P")


class Middleware(Generic[T, P]):

    def __init__(
        self,
        obj: Callable[Concatenate[FN[T], P], FN[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        self.obj = obj
        self.args = args
        self.kwargs = kwargs

    def __call__(self, fn: FN[T]) -> FN[T]:
        return self.obj(fn, *self.args, **self.kwargs)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Middleware) and (  # yapf: disable
            other is self or (
                other.obj is self.obj
                and other.args == self.args
                and other.kwargs == self.kwargs
            )
        )
