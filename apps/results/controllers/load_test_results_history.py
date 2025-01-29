from apps.results.schema.results_history.base import GetResultsHistoryResponse, ResultsHistory
from apps.results.schema.results_history.load_test_results_history import GetLoadTestResultsHistoryQuery, \
    CreateLoadTestResultsHistoryRequest
from services.postgres.repositories.load_test_results_history import LoadTestResultsHistoryRepository, \
    CreateLoadTestResultsHistoryModelDict


async def get_load_test_results_history(
        query: GetLoadTestResultsHistoryQuery,
        load_test_results_history_repository: LoadTestResultsHistoryRepository
) -> GetResultsHistoryResponse:
    results = await load_test_results_history_repository.filter_by_load_test_result_id(
        query.load_test_result_id
    )

    return GetResultsHistoryResponse(
        results=[ResultsHistory.model_validate(result) for result in results]
    )


async def create_load_test_results_history(
        request: CreateLoadTestResultsHistoryRequest,
        load_test_results_history_repository: LoadTestResultsHistoryRepository
):
    await load_test_results_history_repository.create_multiple([
        CreateLoadTestResultsHistoryModelDict(
            **result.model_dump(),
            load_test_result_id=request.load_test_result_id
        )
        for result in request.results
    ])
