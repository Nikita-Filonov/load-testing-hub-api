from pydantic import Field, field_validator

from utils.schema.database import DatabaseSchema


class NumberOfRequestsSchema(DatabaseSchema):
    number_of_requests: float = Field(alias="numberOfRequests")
    number_of_failures: float = Field(alias="numberOfFailures")

    @field_validator(
        "number_of_requests",
        "number_of_failures",
        mode='before'
    )
    def validate_number_of_requests(cls, value: float | None) -> float:
        return round(value or 0, 2)
