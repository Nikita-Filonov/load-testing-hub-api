from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from apps.results.constants.method_results.protocol import ProtocolType
from utils.schema.database import DatabaseSchema
from utils.schema.metrics.content_length import ContentLengthSchema
from utils.schema.metrics.number_of_requests import NumberOfRequestsSchema
from utils.schema.metrics.percentiles import PercentilesSchema
from utils.schema.metrics.requests_per_second import RequestsPerSecondSchema
from utils.schema.metrics.response_times import ResponseTimesSchema
from utils.schema.query import QuerySchema


class ShortMethod(DatabaseSchema):
    method: str
    protocol: ProtocolType


class Method(
    ShortMethod,
    ResponseTimesSchema,
    NumberOfRequestsSchema,
    RequestsPerSecondSchema,
):
    ...


class MethodDetails(
    Method,
    PercentilesSchema,
    ContentLengthSchema
):
    ...


class GetMethodsQuery(QuerySchema):
    method: str | None = None
    protocol: ProtocolType | None = None
    service_id: int = Field(alias="serviceId")
    scenario_id: int | None = Field(alias="scenarioId", default=None)
    end_datetime: datetime = Field(default_factory=datetime.now, alias="endDatetime")
    start_datetime: datetime = Field(default_factory=datetime.now, alias="startDatetime")

    @classmethod
    async def as_query(
            cls,
            method: str | None = Query(default=None),
            protocol: ProtocolType | None = Query(default=None),
            service_id: int = Query(alias="serviceId"),
            scenario_id: int | None = Query(alias="scenarioId", default=None),
            end_datetime: datetime = Query(alias="endDatetime"),
            start_datetime: datetime = Query(alias="startDatetime")
    ) -> Self:
        return GetMethodsQuery(
            method=method,
            protocol=protocol,
            service_id=service_id,
            scenario_id=scenario_id,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )


class GetMethodsResponse(BaseModel):
    methods: list[Method]


class GetMethodDetailsQuery(QuerySchema):
    method: str
    protocol: ProtocolType
    service_id: int = Field(alias="serviceId")
    scenario_id: int | None = Field(alias="scenarioId", default=None)
    end_datetime: datetime = Field(alias="endDatetime")
    start_datetime: datetime = Field(alias="startDatetime")

    @classmethod
    async def as_query(
            cls,
            method: str = Query(),
            protocol: ProtocolType = Query(),
            service_id: int = Query(alias="serviceId"),
            scenario_id: int | None = Query(alias="scenarioId", default=None),
            end_datetime: datetime = Query(alias="endDatetime"),
            start_datetime: datetime = Query(alias="startDatetime")
    ) -> Self:
        return GetMethodDetailsQuery(
            method=method,
            protocol=protocol,
            service_id=service_id,
            scenario_id=scenario_id,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )


class GetMethodDetailsResponse(BaseModel):
    details: MethodDetails


class GetShortMethodsQuery(QuerySchema):
    service_id: int = Field(alias="serviceId")
    scenario_id: int | None = Field(alias="scenarioId", default=None)

    @classmethod
    async def as_query(
            cls,
            service_id: int = Query(alias="serviceId"),
            scenario_id: int | None = Query(alias="scenarioId", default=None),
    ) -> Self:
        return GetShortMethodsQuery(service_id=service_id, scenario_id=scenario_id)


class GetShortMethodsResponse(BaseModel):
    methods: list[ShortMethod]
