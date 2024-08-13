from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from apps.results.schema.ratio_results import RootRatioResult
from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class Scenario(DatabaseModel):
    name: str
    file: str


class ScenarioDetails(Scenario):
    service: str
    ratio_total: RootRatioResult = Field(alias="ratioTotal")
    ratio_per_class: RootRatioResult = Field(alias="ratioPerClass")


class GetScenariosQuery(QueryModel):
    service: str

    @classmethod
    async def as_query(cls, service: str = Query()) -> Self:
        return GetScenariosQuery(service=service)


class GetScenariosResponse(BaseModel):
    scenarios: list[Scenario]


class GetScenarioResponse(BaseModel):
    scenario: Scenario


class CreateScenarioRequest(BaseModel):
    scenario: ScenarioDetails


class GetScenarioDetailsResponse(BaseModel):
    details: ScenarioDetails
