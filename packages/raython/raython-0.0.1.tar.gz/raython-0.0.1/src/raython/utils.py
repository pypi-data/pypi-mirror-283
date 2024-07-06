from typing import (
    Callable,
    TypeVar,
)

_A = TypeVar("_A")
_B = TypeVar("_B")


def _any(items: list[_A]) -> bool:
    return any(items)


def _map(function: Callable[[_A], _B], iterable: list[_A]) -> list[_B]:
    return list(map(function, iterable))


def _filter(predicate: Callable[[_A], bool], iterable: list[_A]) -> list[_A]:
    return list(filter(predicate, iterable))
