from typing import Self

from fastapi import Query
from pydantic import BaseModel, HttpUrl

from services.postgres.models.services import ServiceType
from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class Service(DatabaseModel):
    id: int
    url: HttpUrl
    name: str
    type: ServiceType


class ServiceDetails(Service):
    cluster: str
    namespace: str


class CreateServiceRequest(BaseModel):
    url: HttpUrl
    name: str
    type: ServiceType
    cluster: str
    namespace: str


class UpdateServiceRequest(BaseModel):
    url: HttpUrl | None = None
    name: str | None = None
    type: ServiceType | None = None
    cluster: str | None = None
    namespace: str | None = None


class GetServicesQuery(QueryModel):
    types: list[ServiceType] | None = None

    @classmethod
    async def as_query(cls, types: list[ServiceType] | None = Query(default=None)) -> Self:
        return GetServicesQuery(types=types)


class GetServicesResponse(BaseModel):
    services: list[Service]


class GetServiceResponse(BaseModel):
    service: Service


class GetServiceDetailsResponse(BaseModel):
    details: ServiceDetails
