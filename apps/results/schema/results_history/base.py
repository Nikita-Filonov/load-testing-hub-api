from pydantic import BaseModel

from utils.schema.datetime import DatetimeSchema
from utils.schema.metrics.base import MetricsSchema
from utils.schema.metrics.content_length import ContentLengthSchema
from utils.schema.metrics.number_of_users import NumberOfUsersSchema


class ResultsHistory(DatetimeSchema, MetricsSchema, ContentLengthSchema, NumberOfUsersSchema):
    ...


class GetResultsHistoryResponse(BaseModel):
    results: list[ResultsHistory]


class CreateResultsHistoryRequest(BaseModel):
    results: list[ResultsHistory]
