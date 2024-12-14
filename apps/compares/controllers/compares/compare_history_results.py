from apps.compares.schema.compares.compare_history_results import GetCompareHistoryResultsResponse, \
    CompareHistoryResults
from apps.compares.schema.compares.compare_result_with_results import GetCompareResultWithResultsQuery
from apps.results.schema.history_results import HistoryResult
from services.postgres.repositories.history_results import HistoryResultsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository


def normalize_compare_history_results(compares: list[CompareHistoryResults]) -> list[CompareHistoryResults]:
    min_compare_length = min(len(compare.results) for compare in compares)
    return [compare.slice_results(min_compare_length) for compare in compares]


async def get_compare_history_results(
        query: GetCompareResultWithResultsQuery,
        history_results_repository: HistoryResultsRepository,
        load_test_results_repository: LoadTestResultsRepository
) -> GetCompareHistoryResultsResponse:
    load_test_results = await load_test_results_repository.filter_by_ids_groped(
        query.compare_with_load_test_results
    )

    history_results = await history_results_repository.filter_by_load_test_result_id(query.load_test_result_id)
    compare_with_history_results = await history_results_repository.filter_by_load_test_result_ids_groped(
        query.compare_with_load_test_results
    )

    compares = [
        CompareHistoryResults(
            title='Current',
            results=[HistoryResult.model_validate(result) for result in history_results]
        ),
        *[
            CompareHistoryResults(
                title=load_test_results[load_test_result_id].get_compare_title(),
                results=[HistoryResult.model_validate(result) for result in history_results]
            )
            for load_test_result_id, history_results in compare_with_history_results.items()
        ]
    ]

    return GetCompareHistoryResultsResponse(compares=normalize_compare_history_results(compares))
