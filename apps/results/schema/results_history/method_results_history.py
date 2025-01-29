from typing import Self

from fastapi import Query
from pydantic import Field

from apps.results.schema.results_history.base import CreateResultsHistoryRequest
from utils.schema.query import QuerySchema


class GetMethodResultsHistoryQuery(QuerySchema):
    method_result_id: int = Field(alias="methodResultId")

    @classmethod
    async def as_query(
            cls,
            method_result_id: int = Query(alias="methodResultId")
    ) -> Self:
        return GetMethodResultsHistoryQuery(method_result_id=method_result_id)


class CreateMethodResultsHistoryRequest(CreateResultsHistoryRequest):
    method_result_id: int = Field(alias="methodResultId")
