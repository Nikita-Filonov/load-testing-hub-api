from pydantic import BaseModel, computed_field, Field

from utils.schema.metrics.base import MetricName


class CompareExplanation(BaseModel):
    metric: MetricName
    weight: float
    compare: float


class CompareExplanationSummary(BaseModel):
    compare: float = Field(exclude=True)
    explanations: list[CompareExplanation]

    @computed_field(alias='formula')
    def formula(self) -> str:
        explanations = ' + '.join([
            f'({explanation.weight} ⋅ {explanation.compare}%)'
            for explanation in self.explanations
        ])
        return f"{explanations} = {self.compare}%"
