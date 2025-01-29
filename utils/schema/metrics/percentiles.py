from pydantic import Field, field_validator

from utils.schema.database import DatabaseSchema


class PercentilesSchema(DatabaseSchema):
    response_time_percentile_50: float = Field(alias="responseTimePercentile50")
    response_time_percentile_60: float = Field(alias="responseTimePercentile60")
    response_time_percentile_70: float = Field(alias="responseTimePercentile70")
    response_time_percentile_80: float = Field(alias="responseTimePercentile80")
    response_time_percentile_90: float = Field(alias="responseTimePercentile90")
    response_time_percentile_95: float = Field(alias="responseTimePercentile95")
    response_time_percentile_99: float = Field(alias="responseTimePercentile99")
    response_time_percentile_100: float = Field(alias="responseTimePercentile100")

    @field_validator(
        'response_time_percentile_50',
        'response_time_percentile_60',
        'response_time_percentile_70',
        'response_time_percentile_80',
        'response_time_percentile_90',
        'response_time_percentile_95',
        'response_time_percentile_99',
        'response_time_percentile_100',
        mode='before'
    )
    def validate_percentiles(cls, value: float | None) -> float:
        return round(value or 0, 2)
