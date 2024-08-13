from pydantic import HttpUrl, Field

from utils.schema.database_model import DatabaseModel


class GetGrafanaDashboardURLResponse(DatabaseModel):
    dashboard_url: HttpUrl = Field(alias="dashboardUrl")
