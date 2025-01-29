from pydantic import Field, HttpUrl

from services.postgres.models.integrations import IntegrationSystemType
from utils.schema.database import DatabaseSchema
from utils.schema.query import QuerySchema


class BuildIntegrationURLRequest(QuerySchema):
    service_id: int = Field(alias="serviceId")
    system_type: IntegrationSystemType = Field(alias="systemType")
    integration_id: int = Field(alias="integrationId")
    load_test_result_id: int = Field(alias="loadTestResultId")


class BuildIntegrationURLResponse(DatabaseSchema):
    integration_url: HttpUrl = Field(alias="integrationUrl")
