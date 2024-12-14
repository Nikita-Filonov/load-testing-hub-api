from pydantic import Field, BaseModel, field_validator

from utils.schema.database_model import DatabaseModel


class AverageAnalytics(DatabaseModel):
    total_requests: float = Field(alias="totalRequests")
    total_failures: float = Field(alias="totalFailures")
    number_of_users: float = Field(alias="numberOfUsers")
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")
    average_response_time: float = Field(alias="averageResponseTime")
    total_requests_per_second: float = Field(alias="totalRequestsPerSecond")
    total_failures_per_second: float = Field(alias="totalFailuresPerSecond")

    @field_validator('total_requests', mode='before')
    def validate_total_requests(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('total_failures', mode='before')
    def validate_total_failures(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('number_of_users', mode='before')
    def validate_number_of_users(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('max_response_time', mode='before')
    def validate_max_response_time(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('min_response_time', mode='before')
    def validate_min_response_time(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('average_response_time', mode='before')
    def validate_average_response_time(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('total_requests_per_second', mode='before')
    def validate_total_requests_per_second(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('total_failures_per_second', mode='before')
    def validate_total_failures_per_second(cls, value: float | None) -> float:
        return round(value or 0, 2)


class GetAverageAnalyticsResponse(BaseModel):
    analytics: AverageAnalytics
