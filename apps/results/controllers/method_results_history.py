from apps.results.schema.results_history.base import GetResultsHistoryResponse, ResultsHistory
from apps.results.schema.results_history.method_results_history import GetMethodResultsHistoryQuery, \
    CreateMethodResultsHistoryRequest
from services.postgres.repositories.method_results_history import MethodResultsHistoryRepository, \
    CreateMethodResultsHistoryModelDict


async def get_method_results_history(
        query: GetMethodResultsHistoryQuery,
        method_results_history_repository: MethodResultsHistoryRepository
) -> GetResultsHistoryResponse:
    results = await method_results_history_repository.filter_by_method_result_id(
        query.method_result_id
    )

    return GetResultsHistoryResponse(
        results=[ResultsHistory.model_validate(result) for result in results]
    )


async def create_method_results_history(
        request: CreateMethodResultsHistoryRequest,
        method_results_history_repository: MethodResultsHistoryRepository
):
    await method_results_history_repository.create_multiple([
        CreateMethodResultsHistoryModelDict(
            **result.model_dump(),
            method_result_id=request.method_result_id
        )
        for result in request.results
    ])
