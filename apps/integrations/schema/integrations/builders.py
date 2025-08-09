from pydantic import Field, HttpUrl

from apps.integrations.constants.integrations.system import IntegrationSystemType
from utils.schema.database import DatabaseSchema


class BuildIntegrationURLRequest(DatabaseSchema):
    system_type: IntegrationSystemType = Field(alias="systemType")
    integration_id: int = Field(alias="integrationId")
    load_test_result_id: int = Field(alias="loadTestResultId")


class BuildIntegrationURLResponse(DatabaseSchema):
    integration_url: HttpUrl = Field(alias="integrationUrl")
