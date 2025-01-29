from typing import Self

from fastapi import Query
from pydantic import Field

from apps.results.schema.results_history.base import CreateResultsHistoryRequest
from utils.schema.query import QuerySchema


class GetLoadTestResultsHistoryQuery(QuerySchema):
    load_test_result_id: int = Field(alias="loadTestResultId")

    @classmethod
    async def as_query(
            cls,
            load_test_result_id: int = Query(alias="loadTestResultId")
    ) -> Self:
        return GetLoadTestResultsHistoryQuery(load_test_result_id=load_test_result_id)


class CreateLoadTestResultsHistoryRequest(CreateResultsHistoryRequest):
    load_test_result_id: int = Field(alias="loadTestResultId")
