from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.history_results.results import get_history_results_with_filters
from apps.results.controllers.load_test_results.details import get_previous_load_test_result
from apps.results.schema.history_results.compares import HistoryResult, \
    GetHistoryResultsCompareResponse, HistoryResultsCompare
from apps.results.schema.history_results.results import GetHistoryResultsQuery
from services.postgres.models import LoadTestResultsModel


async def get_history_results_compare(
        query: GetHistoryResultsQuery,
        session: AsyncSession
) -> GetHistoryResultsCompareResponse:
    load_test_result = await LoadTestResultsModel.get(
        session, clause_filter=(LoadTestResultsModel.id == query.load_test_result_id,)
    )
    previous_load_test_result = await get_previous_load_test_result(
        session, query.load_test_result_id, load_test_result.service, load_test_result.scenario
    )

    if not previous_load_test_result:
        return GetHistoryResultsCompareResponse(compare=HistoryResultsCompare())

    results = await get_history_results_with_filters(query, session)

    previous_results_query = GetHistoryResultsQuery(
        load_test_result_id=previous_load_test_result.id
    )
    previous_results = await get_history_results_with_filters(previous_results_query, session)

    return GetHistoryResultsCompareResponse(
        compare=HistoryResultsCompare(
            current_results=[HistoryResult.model_validate(result) for result in results],
            previous_results=[HistoryResult.model_validate(result) for result in previous_results],
            current_trigger_ci_project_version=load_test_result.trigger_ci_project_version,
            previous_trigger_ci_project_version=previous_load_test_result.trigger_ci_project_version
        )
    )
