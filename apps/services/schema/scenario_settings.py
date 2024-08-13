from pydantic import Field, BaseModel

from utils.schema.database_model import DatabaseModel


class ScenarioMethodSettings(DatabaseModel):
    method: str
    requests_per_second: float = Field(alias="requestsPerSecond")


class ScenarioSettings(DatabaseModel):
    scenario: str
    requests_per_second: float = Field(alias="requestsPerSecond")

    methods_settings: list[ScenarioMethodSettings] = Field(alias="methodsSettings")


class UpdateScenarioSettingsRequest(BaseModel):
    settings: ScenarioSettings


class GetScenarioSettingsResponse(BaseModel):
    settings: ScenarioSettings
