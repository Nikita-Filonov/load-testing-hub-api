from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field, computed_field

from apps.results.schema.load_test_results.compares import LoadTestResultSummaryCompare
from apps.services.schema.scenarios import Scenario
from apps.services.schema.services import ShortService
from utils.schema.database import DatabaseSchema
from utils.schema.metrics.base import MetricsSchema
from utils.schema.metrics.number_of_requests import NumberOfRequestsSchema
from utils.schema.metrics.number_of_users import NumberOfUsersSchema
from utils.schema.metrics.percentiles import PercentilesSchema
from utils.schema.metrics.requests_per_second import RequestsPerSecondSchema
from utils.schema.metrics.response_times import ResponseTimesSchema
from utils.schema.pagination import PaginationResponse
from utils.schema.query import PaginationQuery, QuerySchema


class ShortLoadTestResult(DatabaseSchema):
    id: int
    service: ShortService
    scenario: Scenario
    trigger_ci_job_url: str | None = Field(alias="triggerCIJobUrl")
    trigger_ci_pipeline_url: str | None = Field(alias="triggerCIPipelineUrl")
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")
    load_tests_ci_job_url: str | None = Field(alias="loadTestsCIJobUrl")
    load_tests_ci_pipeline_url: str | None = Field(alias="loadTestsCIPipelineUrl")


class LoadTestResult(
    ShortLoadTestResult,
    NumberOfUsersSchema,
    NumberOfRequestsSchema,
    RequestsPerSecondSchema,
):
    comment: str | None = Field(default=None, max_length=250)
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime = Field(alias="finishedAt")

    compare: LoadTestResultSummaryCompare | None = None

    @computed_field(alias='duration')
    def duration(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()


class LoadTestResultDetails(LoadTestResult, PercentilesSchema, ResponseTimesSchema):
    ...


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


class GetLoadTestResultDetailsQuery(QuerySchema):
    scenario_id: int | None = Field(alias="scenarioId", default=None)

    @classmethod
    async def as_query(
            cls,
            scenario_id: int | None = Query(alias="scenarioId", default=None)
    ) -> Self:
        return GetLoadTestResultDetailsQuery(scenario_id=scenario_id)


class GetLoadTestResultDetailsResponse(BaseModel):
    details: LoadTestResultDetails


class CreateLoadTestResultRequest(MetricsSchema, NumberOfUsersSchema):
    service_id: int = Field(alias="serviceId")
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime = Field(alias="finishedAt")
    scenario_id: int = Field(alias="scenarioId")
    trigger_ci_job_url: str | None = Field(alias="triggerCIJobUrl")
    trigger_ci_pipeline_url: str | None = Field(alias="triggerCIPipelineUrl")
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")
    load_tests_ci_job_url: str | None = Field(alias="loadTestsCIJobUrl")
    load_tests_ci_pipeline_url: str | None = Field(alias="loadTestsCIPipelineUrl")


class UpdateLoadTestResultQuery(GetLoadTestResultDetailsQuery):
    ...


class UpdateLoadTestResultRequest(BaseModel):
    comment: str | None = Field(default=None, max_length=250)
