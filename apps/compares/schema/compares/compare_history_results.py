from typing import Self

from pydantic import BaseModel

from apps.results.schema.history_results import HistoryResult


class CompareHistoryResults(BaseModel):
    title: str
    results: list[HistoryResult]

    def slice_results(self, length: int) -> Self:
        self.results = self.results[:length]
        return self


class GetCompareHistoryResultsResponse(BaseModel):
    compares: list[CompareHistoryResults]
