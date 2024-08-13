from typing import Callable, TypeVar, Iterable

T = TypeVar("T")


def find(func: Callable[[T], bool], iterable: Iterable[T], default: T | None = None) -> T | None:
    return next((filter(lambda item: func(item), iterable)), default)
