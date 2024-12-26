from pydantic import Field, HttpUrl

from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class BuildIntegrationURLRequest(QueryModel):
    service_id: int = Field(alias="serviceId")
    integration_id: int = Field(alias="integrationId")
    load_test_result_id: int = Field(alias="loadTestResultId")


class BuildKibanaDiscoverURLResponse(DatabaseModel):
    discover_url: HttpUrl = Field(alias="discoverUrl")


class BuildGrafanaDashboardURLResponse(DatabaseModel):
    dashboard_url: HttpUrl = Field(alias="dashboardUrl")
