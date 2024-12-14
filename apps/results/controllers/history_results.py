from apps.results.schema.history_results import GetHistoryResultsResponse, GetHistoryResultsQuery, \
    HistoryResult, CreateHistoryResultsRequest
from services.postgres.repositories.history_results import HistoryResultsRepository, CreateHistoryResultsModelDict


async def get_history_results(
        query: GetHistoryResultsQuery,
        history_results_repository: HistoryResultsRepository
) -> GetHistoryResultsResponse:
    results = await history_results_repository.filter_by_load_test_result_id(
        query.load_test_result_id
    )

    return GetHistoryResultsResponse(
        results=[HistoryResult.model_validate(result) for result in results]
    )


async def create_history_results(
        request: CreateHistoryResultsRequest,
        history_results_repository: HistoryResultsRepository
):
    await history_results_repository.create_multiple([
        CreateHistoryResultsModelDict(
            **result.model_dump(),
            load_test_result_id=request.load_test_result_id
        )
        for result in request.results
    ])
