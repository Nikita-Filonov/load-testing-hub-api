from pydantic import BaseModel

from utils.schema.datetime import DatetimeSchema
from utils.schema.metrics.response_times import ResponseTimesSchema


class ResponseTimesAnalytics(DatetimeSchema, ResponseTimesSchema):
    ...


class GetResponseTimesAnalyticsResponse(BaseModel):
    analytics: list[ResponseTimesAnalytics]
