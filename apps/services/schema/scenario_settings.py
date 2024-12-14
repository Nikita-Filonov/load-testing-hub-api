from pydantic import Field, BaseModel

from utils.schema.database_model import DatabaseModel


class ScenarioMethodSettings(DatabaseModel):
    method: str
    response_time: float = Field(alias="responseTime", default=0.0)
    content_length: float = Field(alias="contentLength", default=0.0)
    min_response_time: float = Field(alias="minResponseTime", default=0.0)
    max_response_time: float = Field(alias="maxResponseTime", default=0.0)
    number_of_requests: float = Field(alias="numberOfRequests", default=0.0)
    number_of_failures: float = Field(alias="numberOfFailures", default=0.0)
    requests_per_second: float = Field(alias="requestsPerSecond", default=0.0)
    failures_per_second: float = Field(alias="failuresPerSecond", default=0.0)


class ScenarioSettings(DatabaseModel):
    scenario_id: int
    response_time: float = Field(alias="responseTime", default=0.0)
    number_of_users: float = Field(alias="numberOfUsers", default=0.0)
    min_response_time: float = Field(alias="minResponseTime", default=0.0)
    max_response_time: float = Field(alias="maxResponseTime", default=0.0)
    number_of_requests: float = Field(alias="numberOfRequests", default=0.0)
    number_of_failures: float = Field(alias="numberOfFailures", default=0.0)
    requests_per_second: float = Field(alias="requestsPerSecond", default=0.0)
    failures_per_second: float = Field(alias="failuresPerSecond", default=0.0)

    methods_settings: list[ScenarioMethodSettings] = Field(alias="methodsSettings")


class UpdateScenarioSettingsRequest(BaseModel):
    response_time: float | None = Field(alias="responseTime", default=None)
    number_of_users: float | None = Field(alias="numberOfUsers", default=None)
    min_response_time: float | None = Field(alias="minResponseTime", default=None)
    max_response_time: float | None = Field(alias="maxResponseTime", default=None)
    number_of_requests: float | None = Field(alias="numberOfRequests", default=None)
    number_of_failures: float | None = Field(alias="numberOfFailures", default=None)
    requests_per_second: float | None = Field(alias="requestsPerSecond", default=None)
    failures_per_second: float | None = Field(alias="failuresPerSecond", default=None)

    methods_settings: list[ScenarioMethodSettings] | None = Field(alias="methodsSettings", default=None)


class GetScenarioSettingsResponse(BaseModel):
    settings: ScenarioSettings
