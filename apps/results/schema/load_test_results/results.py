from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field, field_validator, computed_field

from apps.results.schema.load_test_results.compares import LoadTestResultSummaryCompare
from apps.services.schema.scenarios import Scenario
from apps.services.schema.services import Service
from utils.schema.database_model import DatabaseModel
from utils.schema.paginration_model import PaginationResponse
from utils.schema.query_model import PaginationQuery, QueryModel


class ShortLoadTestResult(DatabaseModel):
    id: int
    service: Service
    scenario: Scenario
    trigger_ci_job_url: str | None = Field(alias="triggerCIJobUrl")
    trigger_ci_pipeline_url: str | None = Field(alias="triggerCIPipelineUrl")
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")
    load_tests_ci_job_url: str | None = Field(alias="loadTestsCIJobUrl")
    load_tests_ci_pipeline_url: str | None = Field(alias="loadTestsCIPipelineUrl")


class LoadTestResult(ShortLoadTestResult):
    comment: str | None = Field(default=None, max_length=250)
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime = Field(alias="finishedAt")
    total_requests: int = Field(alias="totalRequests")
    total_failures: int = Field(alias="totalFailures")
    number_of_users: int = Field(alias="numberOfUsers")
    total_requests_per_second: float = Field(alias="totalRequestsPerSecond")

    compare: LoadTestResultSummaryCompare | None = None

    @computed_field(alias='duration')
    def duration(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()

    @field_validator('total_requests_per_second')
    def validate_total_requests_per_second(cls, total_requests_per_second: float) -> float:
        return round(total_requests_per_second, 2)


class LoadTestResultDetails(LoadTestResult):
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")
    average_response_time: float = Field(alias="averageResponseTime")
    total_failures_per_second: float = Field(alias="totalFailuresPerSecond")

    @field_validator('max_response_time')
    def validate_max_response_time(cls, max_response_time: float) -> float:
        return round(max_response_time, 2)

    @field_validator('min_response_time')
    def validate_min_response_time(cls, min_response_time: float) -> float:
        return round(min_response_time, 2)

    @field_validator('average_response_time')
    def validate_average_response_time(cls, average_response_time: float) -> float:
        return round(average_response_time, 2)

    @field_validator('total_failures_per_second')
    def validate_total_failures_per_second(cls, total_failures_per_second: float) -> float:
        return round(total_failures_per_second, 2)


class GetLoadTestResultsQuery(PaginationQuery):
    service_id: int = Field(alias="serviceId")
    started_at: datetime | None = Field(alias="startedAt")
    finished_at: datetime | None = Field(alias="finishedAt")
    scenario_id: int | None = Field(alias="scenarioId", default=None)
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")

    @classmethod
    async def as_query(
            cls,
            limit: int = Query(default=50),
            offset: int = Query(default=0),
            service_id: int = Query(alias="serviceId"),
            started_at: datetime | None = Query(default=None, alias="startedAt"),
            finished_at: datetime | None = Query(default=None, alias="finishedAt"),
            scenario_id: int | None = Query(default=None, alias="scenarioId"),
            trigger_ci_project_version: str | None = Query(
                default=None, alias="triggerCIProjectVersion"
            )
    ) -> Self:
        return GetLoadTestResultsQuery(
            limit=limit,
            offset=offset,
            service_id=service_id,
            started_at=started_at,
            finished_at=finished_at,
            scenario_id=scenario_id,
            trigger_ci_project_version=trigger_ci_project_version
        )


class GetLoadTestResultsResponse(PaginationResponse[LoadTestResult]):
    ...


class GetLoadTestResultDetailsQuery(QueryModel):
    scenario_id: int | None = Field(alias="scenarioId", default=None)

    @classmethod
    async def as_query(
            cls,
            scenario_id: int | None = Query(alias="scenarioId", default=None)
    ) -> Self:
        return GetLoadTestResultDetailsQuery(scenario_id=scenario_id)


class GetLoadTestResultDetailsResponse(BaseModel):
    details: LoadTestResultDetails


class CreateLoadTestResultRequest(BaseModel):
    service_id: int = Field(alias="serviceId")
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime = Field(alias="finishedAt")
    scenario_id: int = Field(alias="scenarioId")
    total_requests: int = Field(alias="totalRequests")
    number_of_users: int = Field(alias="numberOfUsers")
    trigger_ci_job_url: str | None = Field(alias="triggerCIJobUrl")
    trigger_ci_pipeline_url: str | None = Field(alias="triggerCIPipelineUrl")
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")
    load_tests_ci_job_url: str | None = Field(alias="loadTestsCIJobUrl")
    load_tests_ci_pipeline_url: str | None = Field(alias="loadTestsCIPipelineUrl")
    total_requests_per_second: float = Field(alias="totalRequestsPerSecond")
    total_failures: int = Field(alias="totalFailures")
    total_failures_per_second: float = Field(alias="totalFailuresPerSecond")
    average_response_time: float = Field(alias="averageResponseTime")
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")


class UpdateLoadTestResultQuery(GetLoadTestResultDetailsQuery):
    ...


class UpdateLoadTestResultRequest(BaseModel):
    comment: str | None = Field(default=None, max_length=250)
