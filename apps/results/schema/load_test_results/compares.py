from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field

from apps.compares.schema.compare_settings import CompareSettings
from utils.common.compare import get_compare_percent_with_weight, ComparePercentWithWeight, get_compare_percent, \
    ComparePercentDirection


class LoadTestResultSummaryCompareMetric(BaseModel):
    actual: float = Field(exclude=True)
    average: float = Field(exclude=True)
    previous: float = Field(exclude=True)
    direction: ComparePercentDirection = Field(exclude=True)

    @computed_field(alias="compareWithAverage")
    @property
    def compare_with_average(self) -> float:
        return get_compare_percent(
            actual=self.actual,
            expected=self.average,
            direction=self.direction
        )

    @computed_field(alias="compareWithPrevious")
    @property
    def compare_with_previous(self) -> float:
        return get_compare_percent(
            actual=self.actual,
            expected=self.previous,
            direction=self.direction
        )


class ResponseTimeLoadTestResultSummaryCompareMetric(LoadTestResultSummaryCompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.LOWER_IS_BETTER


class MinResponseTimeLoadTestResultSummaryCompareMetric(LoadTestResultSummaryCompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.LOWER_IS_BETTER


class MaxResponseTimeLoadTestResultSummaryCompareMetric(LoadTestResultSummaryCompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.LOWER_IS_BETTER


class NumberOfRequestsLoadTestResultSummaryCompareMetric(LoadTestResultSummaryCompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.HIGHER_IS_BETTER


class NumberOfFailuresLoadTestResultSummaryCompareMetric(LoadTestResultSummaryCompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.LOWER_IS_BETTER


class RequestsPerSecondLoadTestResultSummaryCompareMetric(LoadTestResultSummaryCompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.HIGHER_IS_BETTER


class FailuresPerSecondLoadTestResultSummaryCompareMetric(LoadTestResultSummaryCompareMetric):
    direction: ComparePercentDirection = ComparePercentDirection.LOWER_IS_BETTER


class LoadTestResultSummaryCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    settings: CompareSettings = Field(exclude=True)

    previous_id: int | None = Field(default=None, alias="previousId")
    response_time: ResponseTimeLoadTestResultSummaryCompareMetric = Field(exclude=True)
    min_response_time: MinResponseTimeLoadTestResultSummaryCompareMetric = Field(exclude=True)
    max_response_time: MaxResponseTimeLoadTestResultSummaryCompareMetric = Field(exclude=True)
    number_of_requests: NumberOfRequestsLoadTestResultSummaryCompareMetric = Field(exclude=True)
    number_of_failures: NumberOfFailuresLoadTestResultSummaryCompareMetric = Field(exclude=True)
    requests_per_second: RequestsPerSecondLoadTestResultSummaryCompareMetric = Field(exclude=True)
    failures_per_second: FailuresPerSecondLoadTestResultSummaryCompareMetric = Field(exclude=True)

    def get_compare_weights(
            self,
            compare_with: Literal['compare_with_average', 'compare_with_previous']
    ) -> list[ComparePercentWithWeight]:
        return [
            ComparePercentWithWeight(
                weight=self.settings.response_time_weight,
                percent=getattr(self.response_time, compare_with)
            ),
            ComparePercentWithWeight(
                weight=self.settings.min_response_time_weight,
                percent=getattr(self.min_response_time, compare_with)
            ),
            ComparePercentWithWeight(
                weight=self.settings.max_response_time_weight,
                percent=getattr(self.max_response_time, compare_with)
            ),
            ComparePercentWithWeight(
                weight=self.settings.number_of_requests_weight,
                percent=getattr(self.number_of_requests, compare_with)
            ),
            ComparePercentWithWeight(
                weight=self.settings.number_of_failures_weight,
                percent=getattr(self.number_of_failures, compare_with)
            ),
            ComparePercentWithWeight(
                weight=self.settings.requests_per_second_weight,
                percent=getattr(self.requests_per_second, compare_with)
            ),
            ComparePercentWithWeight(
                weight=self.settings.failures_per_second_weight,
                percent=getattr(self.failures_per_second, compare_with)
            )
        ]

    @computed_field(alias="compareWithAverage")
    def compare_with_average(self) -> float:
        return get_compare_percent_with_weight(self.get_compare_weights('compare_with_average'))

    @computed_field(alias="compareWithPrevious")
    def compare_with_previous(self) -> float:
        return get_compare_percent_with_weight(self.get_compare_weights('compare_with_previous'))
