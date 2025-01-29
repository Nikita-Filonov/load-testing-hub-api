from typing import Self, TypeVar, Generic

from pydantic import BaseModel

from utils.schema.database import DatabaseSchema
from utils.schema.datetime import DatetimeSchema
from utils.schema.metrics.number_of_requests import NumberOfRequestsSchema
from utils.schema.metrics.number_of_users import NumberOfUsersSchema
from utils.schema.metrics.requests_per_second import RequestsPerSecondSchema
from utils.schema.metrics.response_times import ResponseTimesSchema

T = TypeVar("T", bound=BaseModel)


class CompareResultHistory(DatetimeSchema, DatabaseSchema, Generic[T]):
    metrics: T


class CompareResultsHistory(BaseModel, Generic[T]):
    title: str
    results: list[CompareResultHistory[T]]

    def slice_results(self, length: int) -> Self:
        self.results = self.results[:length]
        return self


class GetCompareResultsHistoryResponse(BaseModel, Generic[T]):
    compares: list[CompareResultsHistory[T]]


class GetCompareResultsHistoryResponseTimesResponse(
    GetCompareResultsHistoryResponse[ResponseTimesSchema]
):
    ...


class GetCompareResultsHistoryNumberOfUsersResponse(
    GetCompareResultsHistoryResponse[NumberOfUsersSchema]
):
    ...


class GetCompareResultsHistoryNumberOfRequestsResponse(
    GetCompareResultsHistoryResponse[NumberOfRequestsSchema]
):
    ...


class GetCompareResultsHistoryRequestsPerSecondResponse(
    GetCompareResultsHistoryResponse[RequestsPerSecondSchema]
):
    ...
