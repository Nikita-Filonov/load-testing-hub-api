from dataclasses import dataclass
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, computed_field

from apps.compares.constants.compare_settings.context import CompareSettingsContext
from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare_explanation import CompareExplanationSummary, CompareExplanation
from apps.compares.schema.compares.compare_metric import CompareMetric, MAP_METRIC_KEY_TO_COMPARE_PERCENT_DIRECTION
from apps.results.constants.method_results.protocol import ProtocolType
from services.postgres.models.base.metrics import MetricsModel, MetricsModelAverages
from utils.base.compare import get_compare_percent_with_weight, ComparePercentWithWeight
from utils.schema.metrics.base import MetricKey, MetricsSchema, MetricName


@dataclass
class GetCompareMetricsParams:
    actual_instance: MetricsModel | MetricsModelAverages | MetricsSchema | None
    expected_instance: MetricsModel | MetricsModelAverages | MetricsSchema | None

    @property
    def actual_fallback(self) -> float | None:
        return None if self.actual_instance else 0.0

    @property
    def expected_fallback(self) -> float | None:
        return None if self.expected_instance else 0.0


@dataclass
class BuildBaseCompareParams(GetCompareMetricsParams):
    context: CompareSettingsContext
    settings: CompareSettings


class BaseCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    context: CompareSettingsContext = Field(exclude=True)
    settings: CompareSettings = Field(exclude=True)

    min_response_time: CompareMetric = Field(alias="minResponseTime")
    max_response_time: CompareMetric = Field(alias="maxResponseTime")
    number_of_requests: CompareMetric = Field(alias="numberOfRequests")
    number_of_failures: CompareMetric = Field(alias="numberOfFailures")
    requests_per_second: CompareMetric = Field(alias="requestsPerSecond")
    failures_per_second: CompareMetric = Field(alias="failuresPerSecond")
    median_response_time: CompareMetric = Field(alias="medianResponseTime")
    average_response_time: CompareMetric = Field(alias="averageResponseTime")
    response_time_percentile_50: CompareMetric = Field(alias="responseTimePercentile50")
    response_time_percentile_60: CompareMetric = Field(alias="responseTimePercentile60")
    response_time_percentile_70: CompareMetric = Field(alias="responseTimePercentile70")
    response_time_percentile_80: CompareMetric = Field(alias="responseTimePercentile80")
    response_time_percentile_90: CompareMetric = Field(alias="responseTimePercentile90")
    response_time_percentile_95: CompareMetric = Field(alias="responseTimePercentile95")
    response_time_percentile_99: CompareMetric = Field(alias="responseTimePercentile99")
    response_time_percentile_100: CompareMetric = Field(alias="responseTimePercentile100")

    @classmethod
    def get_metric_keys(cls) -> list[MetricKey]:
        return MetricKey.to_list(
            exclude=[
                MetricKey.NUMBER_OF_USERS,
                MetricKey.AVERAGE_CONTENT_LENGTH
            ]
        )

    @classmethod
    def get_compare_metrics(cls, params: GetCompareMetricsParams) -> dict[str, CompareMetric]:
        return {
            metric_key.value: CompareMetric(
                actual=getattr(params.actual_instance, metric_key.value, params.actual_fallback),
                expected=getattr(params.expected_instance, metric_key.value, params.expected_fallback),
                direction=MAP_METRIC_KEY_TO_COMPARE_PERCENT_DIRECTION[metric_key]
            )
            for metric_key in cls.get_metric_keys()
        }

    @classmethod
    def build(cls, params: BuildBaseCompareParams) -> Self:
        compare_metrics = cls.get_compare_metrics(params)
        return cls(context=params.context, settings=params.settings, **compare_metrics)

    @computed_field(alias="compare")
    @property
    def compare(self) -> float:
        return get_compare_percent_with_weight([
            ComparePercentWithWeight(
                weight=getattr(self.settings.weights, metric_key.value),
                percent=getattr(self, metric_key.value).compare
            )
            for metric_key in self.get_metric_keys()
        ])

    @computed_field(alias='explanation')
    @property
    def explanation(self) -> CompareExplanationSummary:
        return CompareExplanationSummary(
            compare=self.compare,
            explanations=[
                CompareExplanation(
                    metric=MetricName[metric_key.name],
                    weight=weight,
                    compare=getattr(self, metric_key.value).compare,
                )
                for metric_key in self.get_metric_keys()
                if (weight := getattr(self.settings.weights, metric_key.value))
            ]
        )

    @computed_field(alias="highlight")
    @property
    def highlight(self) -> bool:
        return self.compare <= getattr(self.settings.highlight_threshold, self.context)


@dataclass
class BuildMethodResultCompare(BuildBaseCompareParams):
    method: str
    protocol: ProtocolType


class MethodResultCompare(BaseCompare):
    method: str
    protocol: ProtocolType
    average_content_length: CompareMetric = Field(alias="averageContentLength")

    @classmethod
    def get_metric_keys(cls) -> list[MetricKey]:
        return [*super().get_metric_keys(), MetricKey.AVERAGE_CONTENT_LENGTH]

    @classmethod
    def build(cls, params: BuildMethodResultCompare) -> Self:
        compare_metrics = cls.get_compare_metrics(params)
        return cls(
            method=params.method,
            context=params.context,
            settings=params.settings,
            protocol=params.protocol,
            **compare_metrics
        )


class LoadTestResultCompare(BaseCompare):
    number_of_users: CompareMetric = Field(alias="numberOfUsers")

    @classmethod
    def get_metric_keys(cls) -> list[MetricKey]:
        return [*super().get_metric_keys(), MetricKey.NUMBER_OF_USERS]
