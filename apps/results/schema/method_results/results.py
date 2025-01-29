from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from apps.results.schema.method_results.compares import MethodResultSummaryCompare
from utils.schema.database import DatabaseSchema
from utils.schema.metrics.base import MetricsSchema
from utils.schema.metrics.content_length import ContentLengthSchema
from utils.schema.query import QuerySchema


class ShortMethodResult(DatabaseSchema):
    id: int
    method: str


class MethodResult(ShortMethodResult, MetricsSchema, ContentLengthSchema):
    protocol: str


class MethodResultDetails(MethodResult):
    compare: MethodResultSummaryCompare | None = None


class CreateMethodResult(MetricsSchema, ContentLengthSchema):
    method: str
    protocol: str
    service_id: int = Field(alias="serviceId")
    scenario_id: int = Field(alias="scenarioId")


class GetMethodResultsQuery(QuerySchema):
    load_test_result_id: int = Field(alias="loadTestResultId")

    @classmethod
    async def as_query(
            cls,
            load_test_result_id: int = Query(alias="loadTestResultId")
    ) -> Self:
        return GetMethodResultsQuery(load_test_result_id=load_test_result_id)


class GetMethodResultDetailsQuery(QuerySchema):
    scenario_id: int | None = Field(alias="scenarioId", default=None)

    @classmethod
    async def as_query(
            cls,
            scenario_id: int | None = Query(alias="scenarioId", default=None)
    ) -> Self:
        return GetMethodResultDetailsQuery(scenario_id=scenario_id)


class GetMethodResultsResponse(BaseModel):
    results: list[MethodResult]


class GetMethodResultDetailsResponse(BaseModel):
    details: MethodResultDetails


class CreateMethodResultsRequest(BaseModel):
    results: list[CreateMethodResult]
    load_test_result_id: int = Field(alias="loadTestResultId")


class CreateMethodResultsResponse(BaseModel):
    results: list[ShortMethodResult]
