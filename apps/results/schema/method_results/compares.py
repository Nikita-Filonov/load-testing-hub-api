from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator

from utils.common.compare import get_compare_percent
from utils.schema.query_model import QueryModel


class MethodResultCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    method: str
    current_requests_per_second: float = Field(alias="currentRequestsPerSecond")
    average_requests_per_second: float = Field(alias="averageRequestsPerSecond")
    previous_requests_per_second: float = Field(alias="previousRequestsPerSecond")

    @computed_field(alias="requestsPerSecondCompareWithAverage")
    def total_requests_per_second_compare_with_average(self) -> float:
        return get_compare_percent(
            previous=self.average_requests_per_second,
            current=self.current_requests_per_second
        )

    @computed_field(alias="requestsPerSecondCompareWithPrevious")
    def total_requests_per_second_compare_with_previous(self) -> float:
        return get_compare_percent(
            previous=self.previous_requests_per_second,
            current=self.current_requests_per_second
        )

    @field_validator('current_requests_per_second')
    def validate_current_requests_per_second(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('average_requests_per_second')
    def validate_average_requests_per_second(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('previous_requests_per_second')
    def validate_previous_requests_per_second(cls, value: float) -> float:
        return round(value, 2)


class MethodResultScenarioCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    method: str
    current_requests_per_second: float = Field(alias="currentRequestsPerSecond")
    scenario_requests_per_second: float = Field(alias="scenarioRequestsPerSecond")

    @computed_field(alias="requestsPerSecondCompare")
    def requests_per_second_compare(self) -> float:
        return get_compare_percent(
            previous=self.scenario_requests_per_second,
            current=self.current_requests_per_second
        )


class GetMethodResultsComparesQuery(QueryModel):
    service: str
    scenario: str | None = None
    load_test_result_id: int = Field(alias="loadTestResultId")

    @classmethod
    async def as_query(
            cls,
            service: str = Query(),
            scenario: str | None = Query(default=None),
            load_test_result_id: int = Query(alias="loadTestResultId")
    ) -> Self:
        return GetMethodResultsComparesQuery(
            service=service,
            scenario=scenario,
            load_test_result_id=load_test_result_id
        )


class GetMethodResultsComparesResponse(BaseModel):
    compares: list[MethodResultCompare]


class GetMethodResultsScenarioComparesQuery(QueryModel):
    scenario: str
    load_test_result_id: int = Field(alias="loadTestResultId")

    @classmethod
    async def as_query(
            cls,
            scenario: str = Query(),
            load_test_result_id: int = Query(alias="loadTestResultId")
    ) -> Self:
        return GetMethodResultsScenarioComparesQuery(
            scenario=scenario,
            load_test_result_id=load_test_result_id
        )


class GetMethodResultsScenarioComparesResponse(BaseModel):
    compares: list[MethodResultScenarioCompare]
