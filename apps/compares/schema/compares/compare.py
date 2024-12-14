from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from apps.compares.schema.compare_settings import CompareSettings
from utils.common.compare import get_compare_percent, get_compare_percent_with_weight, ComparePercentWithWeight, \
    ComparePercentDirection


class CompareMetric(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    actual: float
    expected: float
    direction: ComparePercentDirection = Field(exclude=True)

    @computed_field(alias="compare")
    @property
    def compare(self) -> float:
        return get_compare_percent(
            actual=self.actual,
            expected=self.expected,
            direction=self.direction
        )

    @field_validator('actual', mode='before')
    def validate_actual(cls, value: float | None) -> float:
        return round(value or 0, 2)

    @field_validator('expected', mode='before')
    def validate_scenario(cls, value: float | None) -> float:
        return round(value or 0, 2)


class ResponseTimeCompareMetric(CompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.LOWER_IS_BETTER


class MinResponseTimeCompareMetric(CompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.LOWER_IS_BETTER


class MaxResponseTimeCompareMetric(CompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.LOWER_IS_BETTER


class NumberOfRequestsCompareMetric(CompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.HIGHER_IS_BETTER


class NumberOfFailuresCompareMetric(CompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.LOWER_IS_BETTER


class RequestsPerSecondCompareMetric(CompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.HIGHER_IS_BETTER


class FailuresPerSecondCompareMetric(CompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.LOWER_IS_BETTER


class ContentLengthCompareMetric(CompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.HIGHER_IS_BETTER


class NumberOfUsersCompareMetric(CompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.HIGHER_IS_BETTER


class BaseCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    settings: CompareSettings = Field(exclude=True)

    response_time: ResponseTimeCompareMetric = Field(alias="responseTime")
    min_response_time: MinResponseTimeCompareMetric = Field(alias="minResponseTime")
    max_response_time: MaxResponseTimeCompareMetric = Field(alias="maxResponseTime")
    number_of_requests: NumberOfRequestsCompareMetric = Field(alias="numberOfRequests")
    number_of_failures: NumberOfFailuresCompareMetric = Field(alias="numberOfFailures")
    requests_per_second: RequestsPerSecondCompareMetric = Field(alias="requestsPerSecond")
    failures_per_second: FailuresPerSecondCompareMetric = Field(alias="failuresPerSecond")

    @computed_field(alias="compare")
    def compare(self) -> float:
        return get_compare_percent_with_weight([
            ComparePercentWithWeight(
                weight=self.settings.response_time_weight,
                percent=self.response_time.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.min_response_time_weight,
                percent=self.min_response_time.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.max_response_time_weight,
                percent=self.max_response_time.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.number_of_requests_weight,
                percent=self.number_of_requests.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.number_of_failures_weight,
                percent=self.number_of_failures.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.requests_per_second_weight,
                percent=self.requests_per_second.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.failures_per_second_weight,
                percent=self.failures_per_second.compare
            )
        ])


class MethodResultCompare(BaseCompare):
    method: str
    content_length: ContentLengthCompareMetric = Field(alias="contentLength")


class LoadTestResultCompare(BaseCompare):
    number_of_users: NumberOfUsersCompareMetric = Field(alias="numberOfUsers")
