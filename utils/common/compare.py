from enum import Enum
from typing import NamedTuple


class ComparePercentDirection(str, Enum):
    HIGHER_IS_BETTER = "HIGHER_IS_BETTER"
    LOWER_IS_BETTER = "LOWER_IS_BETTER"

    def get_percent(self, percent: float) -> float:
        match self:
            case self.LOWER_IS_BETTER:
                return -percent
            case self.HIGHER_IS_BETTER:
                return percent


class ComparePercentWithWeight(NamedTuple):
    weight: float
    percent: float

    def get_percent_with_weight(self) -> float:
        return self.weight * self.percent


def get_compare_percent(actual: float, expected: float, direction: ComparePercentDirection) -> float:
    if actual == 0.0 or expected == 0.0:
        return 0.0

    result = ((actual - expected) / expected) * 100

    return round(direction.get_percent(result), 2)


def get_compare_percent_with_weight(compares: list[ComparePercentWithWeight]) -> float:
    weights = sum([compare.weight for compare in compares])

    if abs(weights - 1) > 1e-6:
        raise ValueError(f'Sum of metrics weight must not be more than 1, got {weights}')

    return round(sum(compare.get_percent_with_weight() for compare in compares), 2)
