from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from apps.compares.schema.compare_settings import CompareSettings
from services.postgres.models.compare_settings import CompareSettingsContext
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
    direction: ComparePercentDirection = Field(
        default=ComparePercentDirection.LOWER_IS_BETTER,
        exclude=True
    )


class MinResponseTimeCompareMetric(CompareMetric):
    direction: ComparePercentDirection = Field(
        default=ComparePercentDirection.LOWER_IS_BETTER,
        exclude=True
    )


class MaxResponseTimeCompareMetric(CompareMetric):
    direction: ComparePercentDirection = Field(
        default=ComparePercentDirection.LOWER_IS_BETTER,
        exclude=True
    )


class NumberOfRequestsCompareMetric(CompareMetric):
    direction: ComparePercentDirection = Field(
        default=ComparePercentDirection.HIGHER_IS_BETTER,
        exclude=True
    )


class NumberOfFailuresCompareMetric(CompareMetric):
    direction: ComparePercentDirection = Field(
        default=ComparePercentDirection.LOWER_IS_BETTER,
        exclude=True
    )


class RequestsPerSecondCompareMetric(CompareMetric):
    direction: ComparePercentDirection = Field(
        default=ComparePercentDirection.HIGHER_IS_BETTER,
        exclude=True
    )


class FailuresPerSecondCompareMetric(CompareMetric):
    direction: ComparePercentDirection = Field(
        default=ComparePercentDirection.LOWER_IS_BETTER,
        exclude=True
    )


class ContentLengthCompareMetric(CompareMetric):
    direction: ComparePercentDirection = Field(
        default=ComparePercentDirection.HIGHER_IS_BETTER,
        exclude=True
    )


class NumberOfUsersCompareMetric(CompareMetric):
    direction: ComparePercentDirection = Field(
        default=ComparePercentDirection.HIGHER_IS_BETTER,
        exclude=True
    )


class BaseCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    context: CompareSettingsContext = Field(exclude=True)
    settings: CompareSettings = Field(exclude=True)

    response_time: ResponseTimeCompareMetric = Field(alias="responseTime")
    min_response_time: MinResponseTimeCompareMetric = Field(alias="minResponseTime")
    max_response_time: MaxResponseTimeCompareMetric = Field(alias="maxResponseTime")
    number_of_requests: NumberOfRequestsCompareMetric = Field(alias="numberOfRequests")
    number_of_failures: NumberOfFailuresCompareMetric = Field(alias="numberOfFailures")
    requests_per_second: RequestsPerSecondCompareMetric = Field(alias="requestsPerSecond")
    failures_per_second: FailuresPerSecondCompareMetric = Field(alias="failuresPerSecond")

    @computed_field(alias="compare")
    @property
    def compare(self) -> float:
        return get_compare_percent_with_weight([
            ComparePercentWithWeight(
                weight=self.settings.weights.response_time,
                percent=self.response_time.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.weights.min_response_time,
                percent=self.min_response_time.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.weights.max_response_time,
                percent=self.max_response_time.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.weights.number_of_requests,
                percent=self.number_of_requests.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.weights.number_of_failures,
                percent=self.number_of_failures.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.weights.requests_per_second,
                percent=self.requests_per_second.compare
            ),
            ComparePercentWithWeight(
                weight=self.settings.weights.failures_per_second,
                percent=self.failures_per_second.compare
            )
        ])

    @computed_field(alias="highlight")
    @property
    def highlight(self) -> bool:
        return self.compare <= getattr(self.settings.highlight_threshold, self.context)


class MethodResultCompare(BaseCompare):
    method: str
    content_length: ContentLengthCompareMetric = Field(alias="contentLength")


class LoadTestResultCompare(BaseCompare):
    number_of_users: NumberOfUsersCompareMetric = Field(alias="numberOfUsers")
