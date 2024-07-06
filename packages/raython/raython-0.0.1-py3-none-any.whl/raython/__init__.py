from multiprocessing import Pool
from typing import (
    Iterable,
    Callable,
)
from .utils import _A, _B


def par_map(function: Callable[[_A], _B], iterable: Iterable[_A]) -> Iterable[_B]:
    with Pool(5) as p:
        return p.map(function, iterable)


__all__ = ["par_map"]
