from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from apps.compares.schema.compares.compare import MethodResultCompare
from apps.results.schema.methods import GetMethodDetailsQuery


class GetCompareMethodWithScenarioQuery(GetMethodDetailsQuery):
    service_id: int = Field(alias="serviceId")
    scenario_id: int = Field(alias="scenarioId")

    @classmethod
    async def as_query(
            cls,
            method: str = Query(),
            service_id: int = Query(alias="serviceId"),
            scenario_id: int = Query(alias="scenarioId"),
            end_datetime: datetime = Query(alias="endDatetime"),
            start_datetime: datetime = Query(alias="startDatetime")
    ) -> Self:
        return GetCompareMethodWithScenarioQuery(
            method=method,
            service_id=service_id,
            scenario_id=scenario_id,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )


class GetCompareMethodWithScenarioResponse(BaseModel):
    compare: MethodResultCompare
