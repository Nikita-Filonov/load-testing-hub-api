from typing import Self

from pydantic import BaseModel, Field, confloat, model_validator

from utils.schema.database_model import DatabaseModel

Weight = confloat(le=1.0)


class CompareSettings(DatabaseModel):
    service_id: int = Field(alias="serviceId")
    response_time_weight: Weight = Field(alias="responseTimeWeight")
    min_response_time_weight: Weight = Field(alias="minResponseTimeWeight")
    max_response_time_weight: Weight = Field(alias="maxResponseTimeWeight")
    number_of_requests_weight: Weight = Field(alias="numberOfRequestsWeight")
    number_of_failures_weight: Weight = Field(alias="numberOfFailuresWeight")
    requests_per_second_weight: Weight = Field(alias="requestsPerSecondWeight")
    failures_per_second_weight: Weight = Field(alias="failuresPerSecondWeight")

    @model_validator(mode='after')
    def validate_model(self) -> Self:
        weights = sum([
            self.response_time_weight,
            self.min_response_time_weight,
            self.max_response_time_weight,
            self.number_of_requests_weight,
            self.number_of_failures_weight,
            self.requests_per_second_weight,
            self.failures_per_second_weight
        ])

        if weights > 1:
            raise ValueError(f'Sum of metrics weight must not be more than 1, got {weights}')

        return self


class UpdateCompareSettingsRequest(BaseModel):
    response_time_weight: Weight | None = Field(alias="responseTimeWeight", default=None)
    min_response_time_weight: Weight | None = Field(alias="minResponseTimeWeight", default=None)
    max_response_time_weight: Weight | None = Field(alias="maxResponseTimeWeight", default=None)
    number_of_requests_weight: Weight | None = Field(alias="numberOfRequestsWeight", default=None)
    number_of_failures_weight: Weight | None = Field(alias="numberOfFailuresWeight", default=None)
    requests_per_second_weight: Weight | None = Field(alias="requestsPerSecondWeight", default=None)
    failures_per_second_weight: Weight | None = Field(alias="failuresPerSecondWeight", default=None)


class GetCompareSettingsResponse(BaseModel):
    settings: CompareSettings
