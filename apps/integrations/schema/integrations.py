from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import Field

from utils.schema.query_model import QueryModel


class GetIntegrationURLQuery(QueryModel):
    service: str
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime = Field(alias="finishedAt")

    @classmethod
    async def as_query(
            cls,
            service: str = Query(),
            started_at: datetime = Query(alias="startedAt"),
            finished_at: datetime = Query(alias="finishedAt")
    ) -> Self:
        return GetIntegrationURLQuery(
            service=service,
            started_at=started_at,
            finished_at=finished_at
        )
