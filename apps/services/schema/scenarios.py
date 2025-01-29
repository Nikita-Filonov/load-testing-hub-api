from enum import Enum
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from apps.results.schema.ratio_results import RatioResultList
from utils.schema.database import DatabaseSchema
from utils.schema.query import QuerySchema


class ScenarioTag(str, Enum):
    LEGACY = 'LEGACY'
    LATEST = 'LATEST'
    EXPERIMENT = 'EXPERIMENT'


class Scenario(DatabaseSchema):
    id: int
    name: str
    tags: list[ScenarioTag]
    version: str


class ScenarioDetails(Scenario):
    file: str
    ratio_total: RatioResultList = Field(alias="ratioTotal")
    ratio_per_class: RatioResultList = Field(alias="ratioPerClass")
    number_of_users: int = Field(alias="numberOfUsers")
    runtime_duration: str = Field(alias="runtimeDuration")


class GetScenariosQuery(QuerySchema):
    service_id: int = Field(alias="serviceId")

    @classmethod
    async def as_query(cls, service_id: int = Query(alias="serviceId")) -> Self:
        return GetScenariosQuery(service_id=service_id)


class GetScenariosResponse(BaseModel):
    scenarios: list[Scenario]


class GetScenarioResponse(BaseModel):
    scenario: Scenario


class UpdateScenarioRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    file: str | None = Field(default=None, min_length=1, max_length=250)
    tags: list[ScenarioTag] | None = None
    version: str | None = Field(default=None, min_length=1, max_length=50)
    ratio_total: RatioResultList | None = Field(alias="ratioTotal", default=None)
    ratio_per_class: RatioResultList | None = Field(alias="ratioPerClass", default=None)
    number_of_users: int | None = Field(alias="numberOfUsers", default=None)
    runtime_duration: str | None = Field(
        alias="runtimeDuration", default=None, min_length=1, max_length=50
    )


class CreateScenarioRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    file: str = Field(min_length=1, max_length=250)
    tags: list[ScenarioTag]
    version: str = Field(min_length=1, max_length=50)
    service_id: int = Field(alias="serviceId")
    ratio_total: RatioResultList = Field(alias="ratioTotal", default=[])
    ratio_per_class: RatioResultList = Field(alias="ratioPerClass", default=[])
    number_of_users: int = Field(alias="numberOfUsers")
    runtime_duration: str = Field(alias="runtimeDuration", min_length=1, max_length=50)


class GetScenarioDetailsResponse(BaseModel):
    details: ScenarioDetails
