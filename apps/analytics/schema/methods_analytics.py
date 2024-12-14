from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import Field

from utils.schema.query_model import QueryModel


class GetMethodsAnalyticsQuery(QueryModel):
    method: str
    service_id: int = Field(alias="serviceId")
    scenario_id: int | None = Field(alias="scenarioId", default=None)
    start_datetime: datetime = Field(alias="startDatetime")
    end_datetime: datetime = Field(alias="endDatetime")

    @classmethod
    async def as_query(
            cls,
            method: str,
            service_id: int = Query(alias="serviceId"),
            scenario_id: int | None = Query(alias="scenarioId", default=None),
            start_datetime: datetime = Query(alias="startDatetime"),
            end_datetime: datetime = Query(alias="endDatetime")
    ) -> Self:
        return GetMethodsAnalyticsQuery(
            method=method,
            service_id=service_id,
            scenario_id=scenario_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )
