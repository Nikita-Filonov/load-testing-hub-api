from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class RequestsPerSecondAnalytics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    datetime: datetime
    requests_per_second: float = Field(alias="requestsPerSecond")
    failures_per_second: float = Field(alias="failuresPerSecond")


class GetRequestsPerSecondAnalyticsResponse(BaseModel):
    analytics: list[RequestsPerSecondAnalytics]
