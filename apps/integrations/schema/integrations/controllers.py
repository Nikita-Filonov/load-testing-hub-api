from typing import Self

from fastapi import Query
from pydantic import Field, BaseModel, HttpUrl

from services.postgres.models.integrations import IntegrationEnvironmentType, IntegrationSystemType
from utils.schema.database import DatabaseSchema
from utils.schema.query import QuerySchema


class ShortIntegration(DatabaseSchema):
    id: int
    name: str
    system_type: IntegrationSystemType = Field(alias="systemType")
    environment_type: IntegrationEnvironmentType = Field(alias="environmentType")


class Integration(ShortIntegration):
    order_index: int = Field(alias="orderIndex")
    url_template: str = Field(alias="urlTemplate")


class CreateIntegrationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    service_id: int = Field(alias="serviceId")
    system_type: IntegrationSystemType = Field(alias="systemType")
    order_index: int = Field(alias="orderIndex")
    url_template: HttpUrl = Field(alias="urlTemplate")
    environment_type: IntegrationEnvironmentType = Field(alias="environmentType")


class UpdateIntegrationRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    system_type: IntegrationSystemType | None = Field(alias="systemType", default=None)
    order_index: int | None = Field(alias="orderIndex", default=None)
    url_template: HttpUrl | None = Field(alias="urlTemplate", default=None)
    environment_type: IntegrationEnvironmentType | None = Field(
        alias="environmentType", default=None
    )


class GetIntegrationsQuery(QuerySchema):
    service_id: int = Field(alias="serviceId")

    @classmethod
    async def as_query(cls, service_id: int = Query(alias="serviceId")) -> Self:
        return GetIntegrationsQuery(service_id=service_id)


class GetIntegrationResponse(BaseModel):
    integration: Integration


class GetIntegrationsResponse(BaseModel):
    integrations: list[Integration]


class GetShortIntegrationsResponse(BaseModel):
    integrations: list[ShortIntegration]
