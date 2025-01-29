from pydantic import Field

from utils.schema.database import DatabaseSchema


class NumberOfUsersSchema(DatabaseSchema):
    number_of_users: float = Field(alias="numberOfUsers")
