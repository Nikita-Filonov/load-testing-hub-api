from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from apps.compares.schema.compares.compare import LoadTestResultCompare, MethodResultCompare
from apps.results.schema.load_test_results.results import ShortLoadTestResult
from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class CompareResultWithResultsAverageSummary(DatabaseModel):
    method_result_compares: list[MethodResultCompare] = Field(alias="methodResultCompares")
    load_test_result_compare: LoadTestResultCompare = Field(alias="loadTestResultCompare")


class CompareResultWithResults(DatabaseModel):
    method_result_compares: list[MethodResultCompare] = Field(alias="methodResultCompares")
    load_test_result_compare: LoadTestResultCompare = Field(alias="loadTestResultCompare")
    compare_with_load_test_result: ShortLoadTestResult = Field(alias="compareWithLoadTestResult")


class GetCompareResultWithResultsQuery(QueryModel):
    load_test_result_id: int = Field(alias="loadTestResultId")
    compare_with_load_test_results: list[int] = Field(alias="compareWithLoadTestResults")

    @classmethod
    async def as_query(
            cls,
            load_test_result_id: int = Query(alias="loadTestResultId"),
            compare_with_load_test_results: list[int] = Query(default=[], alias="compareWithLoadTestResults")
    ) -> Self:
        return GetCompareResultWithResultsQuery(
            load_test_result_id=load_test_result_id,
            compare_with_load_test_results=compare_with_load_test_results
        )


class GetCompareResultWithResultsResponse(BaseModel):
    summary: CompareResultWithResultsAverageSummary
    compares: list[CompareResultWithResults]
