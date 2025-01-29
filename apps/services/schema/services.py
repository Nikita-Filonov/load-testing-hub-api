from pydantic import BaseModel, HttpUrl, Field

from utils.schema.database import DatabaseSchema


class ShortService(DatabaseSchema):
    id: int
    url: HttpUrl
    name: str


class Service(ShortService):
    number_of_scenarios: int = Field(alias="numberOfScenarios")
    number_of_load_test_results: int = Field(alias="numberOfLoadTestResults")


class ServiceDetails(Service):
    cluster: str
    namespace: str


class CreateServiceRequest(BaseModel):
    url: HttpUrl = Field(max_length=250)
    name: str = Field(min_length=1, max_length=100)
    cluster: str = Field(min_length=1, max_length=100)
    namespace: str = Field(min_length=1, max_length=250)


class UpdateServiceRequest(BaseModel):
    url: HttpUrl | None = Field(default=None, max_length=250)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    cluster: str | None = Field(default=None, min_length=1, max_length=100)
    namespace: str | None = Field(default=None, min_length=1, max_length=250)


class GetServicesResponse(BaseModel):
    services: list[Service]


class GetServiceResponse(BaseModel):
    service: Service


class GetServiceDetailsResponse(BaseModel):
    details: ServiceDetails
