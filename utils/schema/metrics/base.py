from enum import Enum
from typing import Self

from utils.schema.metrics.number_of_requests import NumberOfRequestsSchema
from utils.schema.metrics.percentiles import PercentilesSchema
from utils.schema.metrics.requests_per_second import RequestsPerSecondSchema
from utils.schema.metrics.response_times import ResponseTimesSchema


class MetricKey(Enum):
    NUMBER_OF_USERS = 'number_of_users'
    MIN_RESPONSE_TIME = 'min_response_time'
    MAX_RESPONSE_TIME = 'max_response_time'
    NUMBER_OF_REQUESTS = 'number_of_requests'
    NUMBER_OF_FAILURES = 'number_of_failures'
    REQUESTS_PER_SECOND = 'requests_per_second'
    FAILURES_PER_SECOND = 'failures_per_second'
    MEDIAN_RESPONSE_TIME = 'median_response_time'
    AVERAGE_RESPONSE_TIME = 'average_response_time'
    AVERAGE_CONTENT_LENGTH = 'average_content_length'
    RESPONSE_TIME_PERCENTILE_50 = 'response_time_percentile_50'
    RESPONSE_TIME_PERCENTILE_60 = 'response_time_percentile_60'
    RESPONSE_TIME_PERCENTILE_70 = 'response_time_percentile_70'
    RESPONSE_TIME_PERCENTILE_80 = 'response_time_percentile_80'
    RESPONSE_TIME_PERCENTILE_90 = 'response_time_percentile_90'
    RESPONSE_TIME_PERCENTILE_95 = 'response_time_percentile_95'
    RESPONSE_TIME_PERCENTILE_99 = 'response_time_percentile_99'
    RESPONSE_TIME_PERCENTILE_100 = 'response_time_percentile_100'

    @classmethod
    def to_list(cls, exclude: list[Self] | None = None) -> list[Self]:
        return [item for item in list(cls) if item not in (exclude or [])]


class MetricName(Enum):
    NUMBER_OF_USERS = 'Number of users'
    MIN_RESPONSE_TIME = 'Min response time (ms)'
    MAX_RESPONSE_TIME = 'Max response time (ms)'
    NUMBER_OF_REQUESTS = 'Number of requests'
    NUMBER_OF_FAILURES = 'Number of failures'
    REQUESTS_PER_SECOND = 'Requests per second'
    FAILURES_PER_SECOND = 'Failures per second'
    MEDIAN_RESPONSE_TIME = 'Median response time (ms)'
    AVERAGE_RESPONSE_TIME = 'Average response time (ms)'
    AVERAGE_CONTENT_LENGTH = 'Average content length (bytes)'
    RESPONSE_TIME_PERCENTILE_50 = '50%-ile (ms)'
    RESPONSE_TIME_PERCENTILE_60 = '60%-ile (ms)'
    RESPONSE_TIME_PERCENTILE_70 = '70%-ile (ms)'
    RESPONSE_TIME_PERCENTILE_80 = '80%-ile (ms)'
    RESPONSE_TIME_PERCENTILE_90 = '90%-ile (ms)'
    RESPONSE_TIME_PERCENTILE_95 = '95%-ile (ms)'
    RESPONSE_TIME_PERCENTILE_99 = '99%-ile (ms)'
    RESPONSE_TIME_PERCENTILE_100 = '100%-ile (ms)'


class MetricsSchema(
    PercentilesSchema,
    ResponseTimesSchema,
    NumberOfRequestsSchema,
    RequestsPerSecondSchema,
):
    ...
