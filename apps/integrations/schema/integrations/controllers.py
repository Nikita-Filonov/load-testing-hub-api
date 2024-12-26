from typing import Self

from fastapi import Query
from pydantic import Field, BaseModel

from services.postgres.models.integrations import IntegrationEnvironmentType
from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class Integration(DatabaseModel):
    id: int
    name: str
    cluster: str
    namespace: str
    environment_type: IntegrationEnvironmentType = Field(alias="environmentType")


class CreateIntegrationRequest(BaseModel):
    name: str
    cluster: str
    namespace: str
    service_id: int = Field(alias="serviceId")
    environment_type: IntegrationEnvironmentType = Field(alias="environmentType")


class UpdateIntegrationRequest(BaseModel):
    name: str | None = None
    cluster: str | None = None
    namespace: str | None = None
    environment_type: IntegrationEnvironmentType | None = Field(
        alias="environmentType", default=None
    )


class GetIntegrationsQuery(QueryModel):
    service_id: int = Field(alias="serviceId")

    @classmethod
    async def as_query(cls, service_id: int = Query(alias="serviceId")) -> Self:
        return GetIntegrationsQuery(service_id=service_id)


class GetIntegrationResponse(BaseModel):
    integration: Integration


class GetIntegrationsResponse(BaseModel):
    integrations: list[Integration]
