from typing import Self

from pydantic import BaseModel, Field, model_validator

from utils.schema.database import DatabaseSchema
from utils.schema.metrics.base import MetricsSchema
from utils.schema.metrics.content_length import ContentLengthSchema
from utils.schema.metrics.number_of_users import NumberOfUsersSchema


class CompareSettingsWeights(MetricsSchema, ContentLengthSchema, NumberOfUsersSchema):
    @model_validator(mode='after')
    def validate_model(self) -> Self:
        if (weights := sum(self.model_dump().values())) > 1:
            raise ValueError(f'Sum of metrics weight must not be more than 1, got {weights}')

        return self


class CompareSettingsHighlightThreshold(DatabaseSchema):
    compare_with_average: float = Field(alias="compareWithAverage")
    compare_with_previous: float = Field(alias="compareWithPrevious")
    compare_result_with_results: float = Field(alias="compareResultWithResults")
    compare_result_with_averages: float = Field(alias="compareResultWithAverages")
    compare_result_with_scenario: float = Field(alias="compareResultWithScenario")
    compare_method_with_scenario: float = Field(alias="compareMethodWithScenario")
    compare_averages_with_scenario: float = Field(alias="compareAveragesWithScenario")


class CompareSettings(DatabaseSchema):
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
