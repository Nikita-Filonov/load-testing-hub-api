from typing import TypeVar

from pydantic import BaseModel

from apps.compares.schema.compares.compare_results_history.base import CompareResultsHistory

T = TypeVar('T', bound=BaseModel)


def normalize_compare_results_history(compares: list[CompareResultsHistory[T]]) -> list[CompareResultsHistory[T]]:
    min_compare_length = min(len(compare.results) for compare in compares)
    return [compare.slice_results(min_compare_length) for compare in compares]
