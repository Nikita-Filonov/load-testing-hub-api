from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import Field

from utils.schema.query_model import QueryModel


class GetMethodsAnalyticsQuery(QueryModel):
    method: str
    scenario: str | None = None
    start_datetime: datetime = Field(alias="startDatetime")
    end_datetime: datetime = Field(alias="endDatetime")

    @classmethod
    async def as_query(
            cls,
            method: str,
            scenario: str | None = Query(default=None),
            start_datetime: datetime = Query(alias="startDatetime"),
            end_datetime: datetime = Query(alias="endDatetime")
    ) -> Self:
        return GetMethodsAnalyticsQuery(
            method=method,
            scenario=scenario,
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )
