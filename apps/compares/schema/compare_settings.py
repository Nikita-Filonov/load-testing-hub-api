from typing import Self

from pydantic import BaseModel, Field, confloat, model_validator

from utils.schema.database_model import DatabaseModel

Weight = confloat(le=1.0)


class CompareSettingsWeights(DatabaseModel):
    response_time: float = Field(alias="responseTime")
    min_response_time: float = Field(alias="minResponseTime")
    max_response_time: float = Field(alias="maxResponseTime")
    number_of_requests: float = Field(alias="numberOfRequests")
    number_of_failures: float = Field(alias="numberOfFailures")
    requests_per_second: float = Field(alias="requestsPerSecond")
    failures_per_second: float = Field(alias="failuresPerSecond")

    @model_validator(mode='after')
    def validate_model(self) -> Self:
        weights = sum([
            self.response_time,
            self.min_response_time,
            self.max_response_time,
            self.number_of_requests,
            self.number_of_failures,
            self.requests_per_second,
            self.failures_per_second
        ])

        if weights > 1:
            raise ValueError(f'Sum of metrics weight must not be more than 1, got {weights}')

        return self


class CompareSettingsHighlightThreshold(DatabaseModel):
    compare_with_average: float = Field(alias="compareWithAverage")
    compare_with_previous: float = Field(alias="compareWithPrevious")
    compare_result_with_results: float = Field(alias="compareResultWithResults")
    compare_result_with_averages: float = Field(alias="compareResultWithAverages")
    compare_result_with_scenario: float = Field(alias="compareResultWithScenario")
    compare_method_with_scenario: float = Field(alias="compareMethodWithScenario")
    compare_averages_with_scenario: float = Field(alias="compareAveragesWithScenario")


class CompareSettings(DatabaseModel):
    service_id: int = Field(alias="serviceId")
    weights: CompareSettingsWeights
    highlight_threshold: CompareSettingsHighlightThreshold = Field(alias="highlightThreshold")


class UpdateCompareSettingsRequest(BaseModel):
    weights: CompareSettingsWeights | None = None
    highlight_threshold: CompareSettingsHighlightThreshold | None = Field(
        alias="highlightThreshold", default=None
    )


class GetCompareSettingsResponse(BaseModel):
    settings: CompareSettings
