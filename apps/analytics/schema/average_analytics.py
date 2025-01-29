from pydantic import BaseModel

from utils.schema.metrics.base import MetricsSchema
from utils.schema.metrics.number_of_users import NumberOfUsersSchema


class AverageAnalytics(MetricsSchema, NumberOfUsersSchema):
    ...


class GetAverageAnalyticsResponse(BaseModel):
    analytics: AverageAnalytics
