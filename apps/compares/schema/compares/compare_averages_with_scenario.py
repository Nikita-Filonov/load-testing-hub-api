from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from apps.analytics.schema.results_analytics import GetResultsAnalyticsQuery
from apps.compares.schema.compares.compare import LoadTestResultCompare


class GetCompareAveragesWithScenarioQuery(GetResultsAnalyticsQuery):
    scenario_id: int = Field(alias="scenarioId")

    @classmethod
    async def as_query(
            cls,
            service_id: int = Query(alias="serviceId"),
            scenario_id: int = Query(alias="scenarioId"),
            start_datetime: datetime = Query(alias="startDatetime"),
            end_datetime: datetime = Query(alias="endDatetime")
    ) -> Self:
        return GetCompareAveragesWithScenarioQuery(
            service_id=service_id,
            scenario_id=scenario_id,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )


class GetCompareAveragesWithScenarioResponse(BaseModel):
    compare: LoadTestResultCompare
