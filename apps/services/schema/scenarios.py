from enum import Enum
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from apps.results.schema.ratio_results import RootRatioResult
from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class ScenarioTag(str, Enum):
    LEGACY = 'LEGACY'
    LATEST = 'LATEST'
    EXPERIMENT = 'EXPERIMENT'


class Scenario(DatabaseModel):
    id: int
    name: str
    tags: list[ScenarioTag]
    version: str


class ScenarioDetails(Scenario):
    file: str
    ratio_total: RootRatioResult = Field(alias="ratioTotal")
    ratio_per_class: RootRatioResult = Field(alias="ratioPerClass")


class GetScenariosQuery(QueryModel):
    service_id: int = Field(alias="serviceId")

    @classmethod
    async def as_query(cls, service_id: int = Query(alias="serviceId")) -> Self:
        return GetScenariosQuery(service_id=service_id)


class GetScenariosResponse(BaseModel):
    scenarios: list[Scenario]


class GetScenarioResponse(BaseModel):
    scenario: Scenario


class UpdateScenarioRequest(BaseModel):
    name: str | None = None
    file: str | None = None
    tags: list[ScenarioTag] | None = None
    version: str | None = None
    ratio_total: RootRatioResult | None = Field(alias="ratioTotal", default=None)
    ratio_per_class: RootRatioResult | None = Field(alias="ratioPerClass", default=None)


class CreateScenarioRequest(BaseModel):
    name: str
    file: str
    tags: list[ScenarioTag]
    version: str
    service_id: int = Field(alias="serviceId")
    ratio_total: RootRatioResult = Field(alias="ratioTotal", default=[])
    ratio_per_class: RootRatioResult = Field(alias="ratioPerClass", default=[])


class GetScenarioDetailsResponse(BaseModel):
    details: ScenarioDetails
