from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field, field_validator

from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class MethodResult(DatabaseModel):
    method: str
    service: str
    scenario: str | None
    protocol: str
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")
    number_of_requests: int = Field(alias="numberOfRequests")
    number_of_failures: int = Field(alias="numberOfFailures")
    total_response_time: float = Field(alias="totalResponseTime")
    requests_per_second: float = Field(alias="requestsPerSecond")
    failures_per_second: float = Field(alias="failuresPerSecond")
    average_response_time: float = Field(alias="averageResponseTime")

    @field_validator("max_response_time")
    def validate_max_response_time(cls, max_response_time: float) -> float:
        return round(max_response_time, 2)

    @field_validator("min_response_time")
    def validate_min_response_time(cls, min_response_time: float) -> float:
        return round(min_response_time, 2)

    @field_validator("total_response_time")
    def validate_total_response_time(cls, total_response_time: float) -> float:
        return round(total_response_time, 2)

    @field_validator("requests_per_second")
    def validate_requests_per_second(cls, requests_per_second: float) -> float:
        return round(requests_per_second, 2)

    @field_validator("average_response_time")
    def validate_average_response_time(cls, average_response_time: float) -> float:
        return round(average_response_time, 2)


class GetMethodResultsQuery(QueryModel):
    load_test_result_id: int = Field(alias="loadTestResultId")

    @classmethod
    async def as_query(
            cls,
            load_test_result_id: int = Query(alias="loadTestResultId")
    ) -> Self:
        return GetMethodResultsQuery(load_test_result_id=load_test_result_id)


class GetMethodResultsResponse(BaseModel):
    results: list[MethodResult]


class CreateMethodResultsRequest(BaseModel):
    results: list[MethodResult]
    load_test_results_id: int = Field(alias="loadTestResultId")
