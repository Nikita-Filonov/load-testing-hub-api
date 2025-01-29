from pydantic import BaseModel

from utils.schema.datetime import DatetimeSchema
from utils.schema.metrics.number_of_requests import NumberOfRequestsSchema


class NumberOfRequestsAnalytics(DatetimeSchema, NumberOfRequestsSchema):
    ...


class GetNumberOfRequestsAnalyticsResponse(BaseModel):
    analytics: list[NumberOfRequestsAnalytics]
