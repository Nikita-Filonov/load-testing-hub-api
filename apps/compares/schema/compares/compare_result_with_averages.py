from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from apps.compares.schema.compares.compare import MethodResultCompare, LoadTestResultCompare
from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class CompareResultWithAverages(DatabaseModel):
    method_result_compares: list[MethodResultCompare] = Field(alias="methodResultCompares")
    load_test_result_compare: LoadTestResultCompare = Field(alias="loadTestResultCompare")


class GetCompareResultWithAveragesQuery(QueryModel):
    scenario_id: int | None = Field(alias="scenarioId", default=None)
    end_datetime: datetime = Field(alias="endDatetime")
    start_datetime: datetime = Field(alias="startDatetime")
    load_test_result_id: int = Field(alias="loadTestResultId")

    @classmethod
    async def as_query(
            cls,
            scenario_id: int | None = Query(alias="scenarioId", default=None),
            end_datetime: datetime = Query(alias="endDatetime"),
            start_datetime: datetime = Query(alias="startDatetime"),
            load_test_result_id: int = Query(alias="loadTestResultId"),
    ) -> Self:
        return GetCompareResultWithAveragesQuery(
            scenario_id=scenario_id,
            end_datetime=end_datetime,
            start_datetime=start_datetime,
            load_test_result_id=load_test_result_id,
        )


class GetCompareResultWithAveragesResponse(BaseModel):
    compare: CompareResultWithAverages
