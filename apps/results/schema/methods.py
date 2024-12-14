from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field, field_validator

from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class ShortMethod(DatabaseModel):
    method: str


class Method(ShortMethod):
    average_response_time: float = Field(alias="averageResponseTime")
    average_number_of_requests: float = Field(alias="averageNumberOfRequests")
    average_number_of_failures: float = Field(alias="averageNumberOfFailures")
    average_requests_per_second: float = Field(alias="averageRequestsPerSecond")

    @field_validator('average_number_of_requests', mode='before')
    def validate_average_number_of_requests(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('average_number_of_failures', mode='before')
    def validate_average_number_of_failures(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('average_response_time', mode='before')
    def validate_average_response_time(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('average_requests_per_second', mode='before')
    def validate_average_requests_per_second(cls, value: float | None) -> float:
        return round(value or 0, 2)


class MethodDetails(Method):
    average_max_response_time: float = Field(alias="averageMaxResponseTime")
    average_min_response_time: float = Field(alias="averageMinResponseTime")
    average_failures_per_second: float = Field(alias="averageFailuresPerSecond")

    @field_validator('average_max_response_time', mode='before')
    def validate_average_max_response_time(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('average_min_response_time', mode='before')
    def validate_average_min_response_time(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('average_failures_per_second', mode='before')
    def validate_average_failures_per_second(cls, value: float | None) -> float:
        return round(value or 0, 2)


class GetMethodsQuery(QueryModel):
    method: str | None = None
    service_id: int = Field(alias="serviceId")
    scenario_id: int | None = Field(alias="scenarioId", default=None)
    end_datetime: datetime = Field(default_factory=datetime.now, alias="endDatetime")
    start_datetime: datetime = Field(default_factory=datetime.now, alias="startDatetime")

    @classmethod
    async def as_query(
            cls,
            method: str | None = Query(default=None),
            service_id: int = Query(alias="serviceId"),
            scenario_id: int | None = Query(alias="scenarioId", default=None),
            end_datetime: datetime = Query(alias="endDatetime"),
            start_datetime: datetime = Query(alias="startDatetime")
    ) -> Self:
        return GetMethodsQuery(
            method=method,
            service_id=service_id,
            scenario_id=scenario_id,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )


class GetMethodsResponse(BaseModel):
    methods: list[Method]


class GetMethodDetailsQuery(QueryModel):
    method: str
    service_id: int = Field(alias="serviceId")
    scenario_id: int | None = Field(alias="scenarioId", default=None)
    end_datetime: datetime = Field(alias="endDatetime")
    start_datetime: datetime = Field(alias="startDatetime")

    @classmethod
    async def as_query(
            cls,
            method: str = Query(),
            service_id: int = Query(alias="serviceId"),
            scenario_id: int | None = Query(alias="scenarioId", default=None),
            end_datetime: datetime = Query(alias="endDatetime"),
            start_datetime: datetime = Query(alias="startDatetime")
    ) -> Self:
        return GetMethodDetailsQuery(
            method=method,
            service_id=service_id,
            scenario_id=scenario_id,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )


class GetMethodDetailsResponse(BaseModel):
    details: MethodDetails


class GetShortMethodsQuery(QueryModel):
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
