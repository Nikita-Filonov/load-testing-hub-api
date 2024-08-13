from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import Field, field_validator, computed_field, BaseModel

from apps.results.schema.methods.schema import GetMethodDetailsQuery
from utils.common.compare import get_compare_percent
from utils.schema.database_model import DatabaseModel


class MethodScenarioCompare(DatabaseModel):
    average_requests_per_second: float = Field(alias="averageRequestsPerSecond")
    scenario_requests_per_second: float = Field(alias="scenarioRequestsPerSecond")

    @field_validator('average_requests_per_second')
    def validate_average_requests_per_second(cls, value: float) -> float:
        return round(value, 2)

    @computed_field(alias="averageRequestsPerSecondCompare")
    def average_requests_per_second_compare(self) -> float:
        return get_compare_percent(
            previous=self.scenario_requests_per_second,
            current=self.average_requests_per_second
        )


class GetMethodScenarioCompareQuery(GetMethodDetailsQuery):
    scenario: str

    @classmethod
    async def as_query(
            cls,
            method: str = Query(),
            scenario: str = Query(),
            end_datetime: datetime = Query(alias="endDatetime"),
            start_datetime: datetime = Query(alias="startDatetime")
    ) -> Self:
        return GetMethodScenarioCompareQuery(
            method=method,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )


class GetMethodScenarioCompareResponse(BaseModel):
    compare: MethodScenarioCompare
