from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ResponseTimesAnalytics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    datetime: datetime
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")
    average_response_time: float = Field(alias="averageResponseTime")


class GetResponseTimesAnalyticsResponse(BaseModel):
    analytics: list[ResponseTimesAnalytics]
