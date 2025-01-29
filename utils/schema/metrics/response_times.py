from pydantic import Field, field_validator

from utils.schema.database import DatabaseSchema


class ResponseTimesSchema(DatabaseSchema):
    min_response_time: float = Field(alias="minResponseTime")
    max_response_time: float = Field(alias="maxResponseTime")
    median_response_time: float = Field(alias="medianResponseTime")
    average_response_time: float = Field(alias="averageResponseTime")

    @field_validator(
        'max_response_time',
        'min_response_time',
        'median_response_time',
        'average_response_time',
        mode='before'
    )
    def validate_response_times(cls, value: float | None) -> float:
        return round(value or 0, 2)
