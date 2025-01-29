from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import Field

from utils.schema.query import QuerySchema


class GetResultsAnalyticsQuery(QuerySchema):
    service_id: int = Field(alias="serviceId")
    scenario_id: int | None = Field(alias="scenarioId", default=None)
    end_datetime: datetime = Field(alias="endDatetime")
    start_datetime: datetime = Field(alias="startDatetime")

    @classmethod
    async def as_query(
            cls,
            service_id: int = Query(alias="serviceId"),
            scenario_id: int | None = Query(alias="scenarioId", default=None),
            end_datetime: datetime = Query(alias="endDatetime"),
            start_datetime: datetime = Query(alias="startDatetime"),
    ) -> Self:
        return GetResultsAnalyticsQuery(
            service_id=service_id,
            scenario_id=scenario_id,
            end_datetime=end_datetime,
            start_datetime=start_datetime,
        )
