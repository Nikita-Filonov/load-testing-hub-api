from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import Field, BaseModel

from utils.schema.metrics.number_of_requests import NumberOfRequestsSchema
from utils.schema.metrics.requests_per_second import RequestsPerSecondSchema
from utils.schema.metrics.response_times import ResponseTimesSchema
from utils.schema.query import QuerySchema


class MethodsAnalytics(BaseModel):
    method: str


class MethodsResponseTimesAnalytics(MethodsAnalytics, ResponseTimesSchema):
    ...


class MethodsNumberOfRequestsAnalytics(MethodsAnalytics, NumberOfRequestsSchema):
    ...


class MethodsRequestsPerSecondAnalytics(MethodsAnalytics, RequestsPerSecondSchema):
    ...


class GetMethodsResponseTimesAnalyticsResponse(BaseModel):
    analytics: list[MethodsResponseTimesAnalytics]


class GetMethodsNumberOfRequestsAnalyticsResponse(BaseModel):
    analytics: list[MethodsNumberOfRequestsAnalytics]


class GetMethodsRequestsPerSecondAnalyticsResponse(BaseModel):
    analytics: list[MethodsRequestsPerSecondAnalytics]


class GetMethodsAnalyticsQuery(QuerySchema):
    service_id: int = Field(alias="serviceId")
    scenario_id: int | None = Field(alias="scenarioId", default=None)
    end_datetime: datetime = Field(alias="endDatetime")
    start_datetime: datetime = Field(alias="startDatetime")

    @classmethod
    async def as_query(
            cls,
            service_id: int = Query(alias="serviceId"),
            scenario_id: int | None = Query(alias="scenarioId", default=None),
            end_datetime: datetime = Query(alias="endDatetime"),
            start_datetime: datetime = Query(alias="startDatetime"),
    ) -> Self:
        return GetMethodsAnalyticsQuery(
            service_id=service_id,
            scenario_id=scenario_id,
            end_datetime=end_datetime,
            start_datetime=start_datetime,
        )
