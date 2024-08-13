from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import Field, BaseModel, field_validator, computed_field

from apps.analytics.schema.results_analytics import GetResultsAnalyticsQuery
from utils.common.compare import get_compare_percent
from utils.schema.database_model import DatabaseModel


class AverageAnalytics(DatabaseModel):
    total_requests: float = Field(alias="totalRequests")
    total_failures: float = Field(alias="totalFailures")
    number_of_users: float = Field(alias="numberOfUsers")
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")
    average_response_time: float = Field(alias="averageResponseTime")
    total_requests_per_second: float = Field(alias="totalRequestsPerSecond")
    total_failures_per_second: float = Field(alias="totalFailuresPerSecond")

    @field_validator('total_requests')
    def validate_total_requests(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('total_failures')
    def validate_total_failures(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('number_of_users')
    def validate_number_of_users(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('max_response_time')
    def validate_max_response_time(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('min_response_time')
    def validate_min_response_time(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('average_response_time')
    def validate_average_response_time(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('total_requests_per_second')
    def validate_total_requests_per_second(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('total_failures_per_second')
    def validate_total_failures_per_second(cls, value: float) -> float:
        return round(value, 2)


class AverageAnalyticsScenarioCompare(DatabaseModel):
    total_requests_per_second: float = Field(alias="totalRequestsPerSecond")
    scenario_total_requests_per_second: float = Field(alias="scenarioTotalRequestsPerSecond")

    @field_validator('total_requests_per_second')
    def validate_total_requests_per_second(cls, value: float) -> float:
        return round(value, 2)

    @computed_field(alias="totalRequestsPerSecondCompare")
    def total_requests_per_second_compare(self) -> float:
        return get_compare_percent(
            previous=self.scenario_total_requests_per_second,
            current=self.total_requests_per_second
        )


class GetAverageAnalyticsResponse(BaseModel):
    analytics: AverageAnalytics


class GetAverageAnalyticsScenarioCompareQuery(GetResultsAnalyticsQuery):
    scenario: str

    @classmethod
    async def as_query(
            cls,
            service: str = Query(),
            scenario: str = Query(),
            start_datetime: datetime = Query(alias="startDatetime"),
            end_datetime: datetime = Query(alias="endDatetime")
    ) -> Self:
        return GetAverageAnalyticsScenarioCompareQuery(
            service=service,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )


class GetAverageAnalyticsScenarioCompareResponse(BaseModel):
    compare: AverageAnalyticsScenarioCompare
