from pydantic import HttpUrl, Field

from utils.schema.database_model import DatabaseModel


class GetKibanaDiscoverURLResponse(DatabaseModel):
    discover_url: HttpUrl = Field(alias="discoverUrl")
