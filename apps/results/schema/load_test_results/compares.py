from pydantic import BaseModel, ConfigDict, Field

from apps.compares.schema.compares.compare import CompareMetric, LoadTestResultCompare


class LoadTestResultCompareSimple(LoadTestResultCompare):
    number_of_users: CompareMetric = Field(exclude=True)
    min_response_time: CompareMetric = Field(exclude=True)
    max_response_time: CompareMetric = Field(exclude=True)
    number_of_requests: CompareMetric = Field(exclude=True)
    number_of_failures: CompareMetric = Field(exclude=True)
    requests_per_second: CompareMetric = Field(exclude=True)
    failures_per_second: CompareMetric = Field(exclude=True)
    median_response_time: CompareMetric = Field(exclude=True)
    average_response_time: CompareMetric = Field(exclude=True)
    response_time_percentile_50: CompareMetric = Field(exclude=True)
    response_time_percentile_60: CompareMetric = Field(exclude=True)
    response_time_percentile_70: CompareMetric = Field(exclude=True)
    response_time_percentile_80: CompareMetric = Field(exclude=True)
    response_time_percentile_90: CompareMetric = Field(exclude=True)
    response_time_percentile_95: CompareMetric = Field(exclude=True)
    response_time_percentile_99: CompareMetric = Field(exclude=True)
    response_time_percentile_100: CompareMetric = Field(exclude=True)


class LoadTestResultSummaryCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    previous_id: int | None = Field(default=None, alias="previousId")
    compare_with_average: LoadTestResultCompareSimple = Field(alias="compareWithAverage")
    compare_with_previous: LoadTestResultCompareSimple = Field(alias="compareWithPrevious")
