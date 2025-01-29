from uuid import uuid4

from pydantic import BaseModel, Field, RootModel, UUID4, field_validator

from utils.base.strings import snake_case_to_pascal_case
from utils.schema.database import DatabaseSchema


class RatioResult(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    name: str
    ratio: float
    tasks: list['RatioResult']

    @field_validator('name')
    def validate_name(cls, name: str) -> str:
        return snake_case_to_pascal_case(name)


class RatioResultList(RootModel):
    root: list[RatioResult] = []


class GetRatioResultResponse(DatabaseSchema):
    ratio_total: RatioResultList = Field(default=RatioResultList(), alias="ratioTotal")
    ratio_per_class: RatioResultList = Field(default=RatioResultList(), alias="ratioPerClass")


class CreateRatioResultRequest(GetRatioResultResponse):
    load_test_result_id: int = Field(alias="loadTestResultId")
