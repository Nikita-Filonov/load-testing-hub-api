from pydantic import BaseModel, HttpUrl

from services.postgres.models.services import ServiceType
from utils.schema.database_model import DatabaseModel


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


class GetServicesResponse(BaseModel):
    services: list[Service]


class GetServiceResponse(BaseModel):
    service: Service


class GetServiceDetailsResponse(BaseModel):
    details: ServiceDetails
