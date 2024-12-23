from pydantic import BaseModel, ConfigDict, Field

from apps.compares.schema.compares.compare import BaseCompare, ResponseTimeCompareMetric, MinResponseTimeCompareMetric, \
    MaxResponseTimeCompareMetric, NumberOfRequestsCompareMetric, NumberOfFailuresCompareMetric, \
    RequestsPerSecondCompareMetric, FailuresPerSecondCompareMetric
from services.postgres.models.compare_settings import CompareSettingsContext


class LoadTestResultCompare(BaseCompare):
    response_time: ResponseTimeCompareMetric = Field(exclude=True)
    min_response_time: MinResponseTimeCompareMetric = Field(exclude=True)
    max_response_time: MaxResponseTimeCompareMetric = Field(exclude=True)
    number_of_requests: NumberOfRequestsCompareMetric = Field(exclude=True)
    number_of_failures: NumberOfFailuresCompareMetric = Field(exclude=True)
    requests_per_second: RequestsPerSecondCompareMetric = Field(exclude=True)
    failures_per_second: FailuresPerSecondCompareMetric = Field(exclude=True)


class LoadTestResultCompareWithAverage(LoadTestResultCompare):
    context: CompareSettingsContext = Field(
        default=CompareSettingsContext.COMPARE_WITH_AVERAGE,
        exclude=True
    )


class LoadTestResultCompareWithPrevious(LoadTestResultCompare):
    context: CompareSettingsContext = Field(
        default=CompareSettingsContext.COMPARE_WITH_PREVIOUS,
        exclude=True
    )


class LoadTestResultSummaryCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    previous_id: int | None = Field(default=None, alias="previousId")
    compare_with_average: LoadTestResultCompareWithAverage = Field(alias="compareWithAverage")
    compare_with_previous: LoadTestResultCompareWithPrevious = Field(alias="compareWithPrevious")
