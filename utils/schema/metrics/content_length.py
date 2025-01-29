from pydantic import Field, field_validator

from utils.schema.database import DatabaseSchema


class ContentLengthSchema(DatabaseSchema):
    average_content_length: float = Field(alias="averageContentLength")

    @field_validator("average_content_length", mode='before')
    def validate_content_length(cls, value: float | None) -> float:
        return round(value or 0, 2)
