from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class HistoryResult(DatabaseModel):
    datetime: datetime
    number_of_users: int = Field(alias="numberOfUsers")
    requests_per_second: float = Field(alias="requestsPerSecond")
    failures_per_second: float = Field(alias="failuresPerSecond")
    average_response_time: float = Field(alias="averageResponseTime")
    response_time_percentile_95: float = Field(alias="responseTimePercentile95")


class GetHistoryResultsQuery(QueryModel):
    load_test_result_id: int = Field(alias="loadTestResultId")

    @classmethod
    async def as_query(
            cls,
            load_test_result_id: int = Query(alias="loadTestResultId")
    ) -> Self:
        return GetHistoryResultsQuery(load_test_result_id=load_test_result_id)


class GetHistoryResultsResponse(BaseModel):
    results: list[HistoryResult]


class CreateHistoryResultsRequest(BaseModel):
    results: list[HistoryResult]
    load_test_results_id: int = Field(alias="loadTestResultId")
