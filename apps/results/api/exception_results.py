from typing import Annotated

from fastapi import APIRouter, Depends

from apps.results.controllers.exception_results import get_exception_results, get_exception_result_details, \
    create_exception_results
from apps.results.schema.exception_results import GetExceptionResultsQuery, GetExceptionResultsResponse, \
    GetExceptionResultDetailsResponse, CreateExceptionResultsRequest
from services.postgres.repositories.exception_results import ExceptionResultsRepository, \
    get_exception_results_repository
from utils.routes import APIRoutes

exception_results_router = APIRouter(
    prefix=APIRoutes.EXCEPTION_RESULTS,
    tags=[APIRoutes.EXCEPTION_RESULTS.as_tag()]
)


@exception_results_router.get('', response_model=GetExceptionResultsResponse)
async def get_exception_results_view(
        query: Annotated[GetExceptionResultsQuery, Depends(GetExceptionResultsQuery.as_query)],
        exception_results_repository: Annotated[ExceptionResultsRepository, Depends(get_exception_results_repository)]
):
    return await get_exception_results(query, exception_results_repository)


@exception_results_router.get(
    '/details/{exception_result_id}',
    response_model=GetExceptionResultDetailsResponse
)
async def get_exception_result_details_view(
        exception_result_id: int,
        exception_results_repository: Annotated[ExceptionResultsRepository, Depends(get_exception_results_repository)]
):
    return await get_exception_result_details(exception_result_id, exception_results_repository)


@exception_results_router.post('')
async def create_exception_results_view(
        request: CreateExceptionResultsRequest,
        exception_results_repository: Annotated[ExceptionResultsRepository, Depends(get_exception_results_repository)]
):
    return await create_exception_results(request, exception_results_repository)
