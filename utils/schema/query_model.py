from typing import Self

from fastapi import Query
from pydantic import BaseModel, ConfigDict


class QueryModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    async def as_query(cls, **kwargs) -> Self:
        raise NotImplementedError("Override this method in child model")


class PaginationQuery(QueryModel):
    limit: int = 50
    offset: int = 0

    @classmethod
    async def as_query(
            cls,
            limit: int = Query(default=50),
            offset: int = Query(default=0),
    ) -> Self:
        return PaginationQuery(limit=limit, offset=offset)
