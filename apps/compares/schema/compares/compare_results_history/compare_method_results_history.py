from typing import Self

from fastapi import Query
from pydantic import Field

from utils.schema.query import QuerySchema


class GetCompareMethodResultsHistoryQuery(QuerySchema):
    method: str
    load_test_result_id: int = Field(alias="loadTestResultId")
    compare_with_load_test_results: list[int] = Field(alias="compareWithLoadTestResults")

    @classmethod
    async def as_query(
            cls,
            method: str = Query(),
            load_test_result_id: int = Query(alias="loadTestResultId"),
            compare_with_load_test_results: list[int] = Query(alias="compareWithLoadTestResults")
    ) -> Self:
        return GetCompareMethodResultsHistoryQuery(
            method=method,
            load_test_result_id=load_test_result_id,
            compare_with_load_test_results=compare_with_load_test_results
        )
