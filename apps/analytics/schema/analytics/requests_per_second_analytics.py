from pydantic import BaseModel

from utils.schema.datetime import DatetimeSchema
from utils.schema.metrics.requests_per_second import RequestsPerSecondSchema


class RequestsPerSecondAnalytics(DatetimeSchema, RequestsPerSecondSchema):
    ...


class GetRequestsPerSecondAnalyticsResponse(BaseModel):
    analytics: list[RequestsPerSecondAnalytics]
