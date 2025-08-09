from pydantic import Field, field_validator

from utils.schema.database import DatabaseSchema


class NumberOfUsersSchema(DatabaseSchema):
    number_of_users: float = Field(alias="numberOfUsers")

    @field_validator("number_of_users", mode='before')
    def validate_number_of_users(cls, value: float | None) -> float:
        return round(value or 0, 2)
