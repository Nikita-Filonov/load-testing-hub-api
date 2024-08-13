from typing import Self

from fastapi import Query
from pydantic import BaseModel, HttpUrl, Field

from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class Service(DatabaseModel):
    url: HttpUrl
    name: str
    is_internal: bool = Field(alias="isInternal")


class GetServicesQuery(QueryModel):
    with_internal: bool = Field(default=False, alias="withInternal")

    @classmethod
    async def as_query(
            cls,
            with_internal: bool = Query(default=False, alias="withInternal")
    ) -> Self:
        return GetServicesQuery(with_internal=with_internal)


class GetServicesResponse(BaseModel):
    services: list[Service]


class GetServiceResponse(BaseModel):
    service: Service
