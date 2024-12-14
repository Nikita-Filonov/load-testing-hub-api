from apps.results.schema.exception_results import CreateExceptionResultsRequest, GetExceptionResultsQuery, \
    GetExceptionResultsResponse, ExceptionResult, GetExceptionResultDetailsResponse, ExceptionResultDetails
from services.postgres.repositories.exception_results import ExceptionResultsRepository, \
    CreateExceptionResultsModelDict


async def get_exception_results(
        query: GetExceptionResultsQuery,
        exception_results_repository: ExceptionResultsRepository
) -> GetExceptionResultsResponse:
    results = await exception_results_repository.filter_by_load_test_result_id(
        query.load_test_result_id
    )

    return GetExceptionResultsResponse(
        results=[ExceptionResult.model_validate(result) for result in results]
    )


async def get_exception_result_details(
        exception_result_id: int,
        exception_results_repository: ExceptionResultsRepository
) -> GetExceptionResultDetailsResponse:
    result = await exception_results_repository.get_by_id(exception_result_id)

    return GetExceptionResultDetailsResponse(details=ExceptionResultDetails.model_validate(result))


async def create_exception_results(
        request: CreateExceptionResultsRequest,
        exception_results_repository: ExceptionResultsRepository
):
    await exception_results_repository.create_multiple([
        CreateExceptionResultsModelDict(
            **result.model_dump(),
            load_test_result_id=request.load_test_result_id
        )
        for result in request.results
    ])
