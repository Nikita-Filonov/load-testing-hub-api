from pydantic import BaseModel, Field

from apps.results.schema.history_results.results import HistoryResult
from utils.schema.database_model import DatabaseModel


class HistoryResultsCompare(DatabaseModel):
    current_results: list[HistoryResult] = Field(default=[], alias="currentResults")
    previous_results: list[HistoryResult] = Field(default=[], alias="previousResults")
    current_trigger_ci_project_version: str | None = Field(
        default=None, alias="currentTriggerCIProjectVersion"
    )
    previous_trigger_ci_project_version: str | None = Field(
        default=None, alias="previousTriggerCIProjectVersion"
    )


class GetHistoryResultsCompareResponse(BaseModel):
    compare: HistoryResultsCompare
