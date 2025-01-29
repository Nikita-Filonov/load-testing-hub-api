from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from utils.base.compare import get_compare_percent, ComparePercentDirection
from utils.schema.metrics.base import MetricKey


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


MAP_METRIC_KEY_TO_COMPARE_PERCENT_DIRECTION: dict[MetricKey, ComparePercentDirection] = {
    MetricKey.NUMBER_OF_USERS: ComparePercentDirection.HIGHER_IS_BETTER,
    MetricKey.MIN_RESPONSE_TIME: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.MAX_RESPONSE_TIME: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.NUMBER_OF_REQUESTS: ComparePercentDirection.HIGHER_IS_BETTER,
    MetricKey.NUMBER_OF_FAILURES: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.REQUESTS_PER_SECOND: ComparePercentDirection.HIGHER_IS_BETTER,
    MetricKey.FAILURES_PER_SECOND: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.MEDIAN_RESPONSE_TIME: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.AVERAGE_RESPONSE_TIME: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.AVERAGE_CONTENT_LENGTH: ComparePercentDirection.HIGHER_IS_BETTER,
    MetricKey.RESPONSE_TIME_PERCENTILE_50: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.RESPONSE_TIME_PERCENTILE_60: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.RESPONSE_TIME_PERCENTILE_70: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.RESPONSE_TIME_PERCENTILE_80: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.RESPONSE_TIME_PERCENTILE_90: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.RESPONSE_TIME_PERCENTILE_95: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.RESPONSE_TIME_PERCENTILE_99: ComparePercentDirection.LOWER_IS_BETTER,
    MetricKey.RESPONSE_TIME_PERCENTILE_100: ComparePercentDirection.LOWER_IS_BETTER,
}
