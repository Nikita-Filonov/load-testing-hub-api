from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class NumberOfRequestsAnalytics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    datetime: datetime
    number_of_requests: int = Field(alias="numberOfRequests")
    number_of_failures: int = Field(alias="numberOfFailures")


class GetNumberOfRequestsAnalyticsResponse(BaseModel):
    analytics: list[NumberOfRequestsAnalytics]
