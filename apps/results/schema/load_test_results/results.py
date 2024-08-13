from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field, field_validator

from apps.results.schema.load_test_results.compares import LoadTestResultCompare
from utils.schema.database_model import DatabaseModel
from utils.schema.paginration_model import PaginationResponse
from utils.schema.query_model import PaginationQuery, QueryModel


class LoadTestResult(DatabaseModel):
    id: int
    service: str
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime = Field(alias="finishedAt")
    total_requests: int = Field(alias="totalRequests")
    total_failures: int = Field(alias="totalFailures")
    number_of_users: int = Field(alias="numberOfUsers")
    trigger_ci_pipeline_url: str | None = Field(alias="triggerCIPipelineUrl")
    trigger_ci_project_title: str | None = Field(alias="triggerCIProjectTitle")
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")
    load_tests_ci_pipeline_url: str | None = Field(alias="loadTestsCIPipelineUrl")
    total_requests_per_second: float = Field(alias="totalRequestsPerSecond")

    compare: LoadTestResultCompare | None = None

    @field_validator('total_requests_per_second')
    def validate_total_requests_per_second(cls, total_requests_per_second: float) -> float:
        return round(total_requests_per_second, 2)


class LoadTestResultDetails(LoadTestResult):
    scenario: str
    total_failures_per_second: float = Field(alias="totalFailuresPerSecond")
    average_response_time: float = Field(alias="averageResponseTime")
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")

    @field_validator('max_response_time')
    def validate_max_response_time(cls, max_response_time: float) -> float:
        return round(max_response_time, 2)

    @field_validator('min_response_time')
    def validate_min_response_time(cls, min_response_time: float) -> float:
        return round(min_response_time, 2)

    @field_validator('total_failures_per_second')
    def validate_total_failures_per_second(cls, total_failures_per_second: float) -> float:
        return round(total_failures_per_second, 2)


class GetLoadTestResultDetailsQuery(QueryModel):
    scenario: str | None = None
    load_test_result_id: int = Field(alias="loadTestResultId")

    @classmethod
    async def as_query(
            cls,
            scenario: str | None = Query(default=None),
            load_test_result_id: int = Query(alias="loadTestResultId")
    ) -> Self:
        return GetLoadTestResultDetailsQuery(
            scenario=scenario,
            load_test_result_id=load_test_result_id
        )


class GetLoadTestResultsQuery(PaginationQuery):
    service: str
    scenario: str | None = None
    started_at: datetime | None = Field(alias="startedAt")
    finished_at: datetime | None = Field(alias="finishedAt")
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")

    @classmethod
    async def as_query(
            cls,
            limit: int = Query(default=50),
            offset: int = Query(default=0),
            service: str = Query(),
            scenario: str | None = Query(default=None),
            started_at: datetime | None = Query(default=None, alias="startedAt"),
            finished_at: datetime | None = Query(default=None, alias="finishedAt"),
            trigger_ci_project_version: str | None = Query(
                default=None, alias="triggerCIProjectVersion"
            )
    ) -> Self:
        return GetLoadTestResultsQuery(
            limit=limit,
            offset=offset,
            service=service,
            scenario=scenario,
            started_at=started_at,
            finished_at=finished_at,
            trigger_ci_project_version=trigger_ci_project_version
        )


class GetLoadTestResultsResponse(PaginationResponse[LoadTestResult]):
    ...


class GetLoadTestResultDetailsResponse(BaseModel):
    details: LoadTestResultDetails


class CreateLoadTestResultRequest(BaseModel):
    service: str
    scenario: str
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime = Field(alias="finishedAt")
    total_requests: int = Field(alias="totalRequests")
    number_of_users: int = Field(alias="numberOfUsers")
    trigger_ci_pipeline_url: str | None = Field(alias="triggerCIPipelineUrl")
    trigger_ci_project_title: str | None = Field(alias="triggerCIProjectTitle")
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")
    load_tests_ci_pipeline_url: str | None = Field(alias="loadTestsCIPipelineUrl")
    total_requests_per_second: float = Field(alias="totalRequestsPerSecond")
    total_failures: int = Field(alias="totalFailures")
    total_failures_per_second: float = Field(alias="totalFailuresPerSecond")
    average_response_time: float = Field(alias="averageResponseTime")
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")
