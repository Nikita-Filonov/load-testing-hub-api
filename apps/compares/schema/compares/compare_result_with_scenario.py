from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from apps.compares.schema.compares.compare import MethodResultCompare, LoadTestResultCompare
from apps.services.schema.scenarios import Scenario
from utils.schema.database import DatabaseSchema
from utils.schema.query import QuerySchema


class CompareResultWithScenario(DatabaseSchema):
    scenario: Scenario
    method_result_compares: list[MethodResultCompare] = Field(alias="methodResultCompares")
    load_test_result_compare: LoadTestResultCompare = Field(alias="loadTestResultCompare")


class GetCompareResultWithScenarioQuery(QuerySchema):
    load_test_result_id: int = Field(alias="loadTestResultId")

    @classmethod
    async def as_query(
            cls,
            load_test_result_id: int = Query(alias="loadTestResultId")
    ) -> Self:
        return GetCompareResultWithScenarioQuery(load_test_result_id=load_test_result_id)


class GetCompareResultWithScenarioResponse(BaseModel):
    compare: CompareResultWithScenario
