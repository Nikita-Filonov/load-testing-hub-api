from pydantic import BaseModel, HttpUrl

from utils.schema.database_model import DatabaseModel


class Service(DatabaseModel):
    id: int
    url: HttpUrl
    name: str


class ServiceDetails(Service):
    cluster: str
    namespace: str


class CreateServiceRequest(BaseModel):
    url: HttpUrl
    name: str
    cluster: str
    namespace: str


class UpdateServiceRequest(BaseModel):
    url: HttpUrl | None = None
    name: str | None = None
    cluster: str | None = None
    namespace: str | None = None


class GetServicesResponse(BaseModel):
    services: list[Service]


class GetServiceResponse(BaseModel):
    service: Service


class GetServiceDetailsResponse(BaseModel):
    details: ServiceDetails
