from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from apps.compares.schema.compares.compare import LoadTestResultCompare
from utils.schema.query import QuerySchema


class GetCompareAveragesWithScenarioQuery(QuerySchema):
    service_id: int = Field(alias="serviceId")
    scenario_id: int = Field(alias="scenarioId")
    end_datetime: datetime = Field(alias="endDatetime")
    start_datetime: datetime = Field(alias="startDatetime")

    @classmethod
    async def as_query(
            cls,
            service_id: int = Query(alias="serviceId"),
            scenario_id: int = Query(alias="scenarioId"),
            end_datetime: datetime = Query(alias="endDatetime"),
            start_datetime: datetime = Query(alias="startDatetime"),
    ) -> Self:
        return GetCompareAveragesWithScenarioQuery(
            service_id=service_id,
            scenario_id=scenario_id,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )


class GetCompareAveragesWithScenarioResponse(BaseModel):
    compare: LoadTestResultCompare
