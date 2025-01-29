from apps.results.schema.method_results.results import GetMethodResultsQuery, GetMethodResultsResponse, MethodResult, \
    CreateMethodResultsRequest, CreateMethodResultsResponse, ShortMethodResult
from services.postgres.repositories.method_results import MethodResultsRepository, CreateMethodResultsModelDict


async def get_method_results(
        query: GetMethodResultsQuery,
        method_results_repository: MethodResultsRepository
) -> GetMethodResultsResponse:
    results = await method_results_repository.filter_by_load_test_result_id(query.load_test_result_id)

    return GetMethodResultsResponse(
        results=[MethodResult.model_validate(result) for result in results]
    )


async def create_method_results(
        request: CreateMethodResultsRequest,
        method_results_repository: MethodResultsRepository
) -> CreateMethodResultsResponse:
    await method_results_repository.create_multiple([
        CreateMethodResultsModelDict(
            **result.model_dump(),
            load_test_result_id=request.load_test_result_id
        )
        for result in request.results
    ])

    results = await method_results_repository.filter_by_load_test_result_id(
        request.load_test_result_id
    )

    return CreateMethodResultsResponse(
        results=[ShortMethodResult.model_validate(result) for result in results]
    )
