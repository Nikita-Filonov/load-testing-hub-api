from pydantic import Field, BaseModel

from apps.results.constants.method_results.protocol import ProtocolType
from utils.schema.database import DatabaseSchema
from utils.schema.metrics.base import MetricsSchema
from utils.schema.metrics.content_length import ContentLengthSchema
from utils.schema.metrics.number_of_users import NumberOfUsersSchema


class ScenarioResultSettings(MetricsSchema, NumberOfUsersSchema):
    ...


class ScenarioMethodSettings(MetricsSchema, ContentLengthSchema):
    method: str
    protocol: ProtocolType = ProtocolType.GRPC


class ScenarioSettings(DatabaseSchema):
    scenario_id: int

    result_settings: ScenarioResultSettings = Field(alias="resultSettings")
    methods_settings: list[ScenarioMethodSettings] = Field(alias="methodsSettings")


class UpdateScenarioSettingsRequest(BaseModel):
    result_settings: ScenarioResultSettings | None = Field(alias="resultSettings", default=None)
    methods_settings: list[ScenarioMethodSettings] | None = Field(alias="methodsSettings", default=None)


class GetScenarioSettingsResponse(BaseModel):
    settings: ScenarioSettings
