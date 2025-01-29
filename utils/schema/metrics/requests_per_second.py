from pydantic import Field, field_validator

from utils.schema.database import DatabaseSchema


class RequestsPerSecondSchema(DatabaseSchema):
    requests_per_second: float = Field(alias="requestsPerSecond")
    failures_per_second: float = Field(alias="failuresPerSecond")

    @field_validator(
        "requests_per_second",
        "failures_per_second",
        mode='before'
    )
    def validate_requests_per_second(cls, value: float | None) -> float:
        return round(value or 0, 2)
