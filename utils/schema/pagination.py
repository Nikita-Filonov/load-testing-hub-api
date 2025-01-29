from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int = 10
    offset: int = 0
