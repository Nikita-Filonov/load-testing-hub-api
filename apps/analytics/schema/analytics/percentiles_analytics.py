from pydantic import BaseModel

from utils.schema.datetime import DatetimeSchema
from utils.schema.metrics.percentiles import PercentilesSchema


class PercentilesAnalytics(DatetimeSchema, PercentilesSchema):
    ...


class GetPercentilesAnalyticsResponse(BaseModel):
    analytics: list[PercentilesAnalytics]
