from uuid import uuid4

from pydantic import BaseModel, Field, RootModel, UUID4, field_validator

from utils.common.strings import snake_case_to_pascal_case
from utils.schema.database_model import DatabaseModel


class RatioResult(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    name: str
    ratio: float
    tasks: list['RatioResult']

    @field_validator('name')
    def validate_name(cls, name: str) -> str:
        return snake_case_to_pascal_case(name)


class RootRatioResult(RootModel):
    root: list[RatioResult] = []


class GetRatioResultResponse(DatabaseModel):
    ratio_total: RootRatioResult = Field(default=RootRatioResult(), alias="ratioTotal")
    ratio_per_class: RootRatioResult = Field(default=RootRatioResult(), alias="ratioPerClass")


class CreateRatioResultRequest(GetRatioResultResponse):
    load_test_results_id: int = Field(alias="loadTestResultId")
