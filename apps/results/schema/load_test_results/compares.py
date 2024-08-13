from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator

from utils.common.compare import get_compare_percent
from utils.schema.query_model import QueryModel


class LoadTestResultCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    previous_id: int | None = Field(default=None, alias="previousId")
    current_total_requests_per_second: float = Field(alias="currentTotalRequestsPerSecond")
    average_total_requests_per_second: float = Field(alias="averageTotalRequestsPerSecond")
    previous_total_requests_per_second: float = Field(alias="previousTotalRequestsPerSecond")

    @computed_field(alias="totalRequestsPerSecondCompareWithAverage")
    def total_requests_per_second_compare_with_average(self) -> float:
        return get_compare_percent(
            previous=self.average_total_requests_per_second,
            current=self.current_total_requests_per_second
        )

    @computed_field(alias="totalRequestsPerSecondCompareWithPrevious")
    def total_requests_per_second_compare_with_previous(self) -> float:
        return get_compare_percent(
            previous=self.previous_total_requests_per_second,
            current=self.current_total_requests_per_second
        )

    @field_validator('current_total_requests_per_second')
    def validate_current_total_requests_per_second(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('average_total_requests_per_second')
    def validate_average_total_requests_per_second(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('previous_total_requests_per_second')
    def validate_previous_total_requests_per_second(cls, value: float) -> float:
        return round(value, 2)


class LoadTestResultScenarioCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    current_requests_per_second: float = Field(alias="currentRequestsPerSecond")
    scenario_requests_per_second: float = Field(alias="scenarioRequestsPerSecond")

    @field_validator('current_requests_per_second')
    def validate_current_requests_per_second(cls, value: float) -> float:
        return round(value, 2)

    @computed_field(alias="requestsPerSecondCompare")
    def requests_per_second_compare(self) -> float:
        return get_compare_percent(
            previous=self.scenario_requests_per_second,
            current=self.current_requests_per_second
        )


class GetLoadTestResultScenarioCompareQuery(QueryModel):
    load_test_result_id: int = Field(alias="loadTestResultId")

    @classmethod
    async def as_query(
            cls,
            load_test_result_id: int = Query(alias="loadTestResultId")
    ) -> Self:
        return GetLoadTestResultScenarioCompareQuery(load_test_result_id=load_test_result_id)


class GetLoadTestResultScenarioCompareResponse(BaseModel):
    compare: LoadTestResultScenarioCompare
