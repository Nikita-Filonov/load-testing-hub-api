from typing import Annotated

from fastapi import APIRouter, Depends

from apps.results.controllers.method_results.details import get_method_result_details
from apps.results.controllers.method_results.results import get_method_results, create_method_results
from apps.results.schema.method_results.results import GetMethodResultDetailsQuery, GetMethodResultDetailsResponse
from apps.results.schema.method_results.results import GetMethodResultsQuery, GetMethodResultsResponse, \
    CreateMethodResultsRequest, CreateMethodResultsResponse
from services.postgres.repositories.compare_settings import CompareSettingsRepository, get_compare_settings_repository
from services.postgres.repositories.method_results import MethodResultsRepository, get_method_results_repository
from utils.routes import APIRoutes

method_results_router = APIRouter(
    prefix=APIRoutes.METHOD_RESULTS,
    tags=[APIRoutes.METHOD_RESULTS.as_tag()]
)


@method_results_router.get('', response_model=GetMethodResultsResponse)
async def get_method_results_view(
        query: Annotated[GetMethodResultsQuery, Depends(GetMethodResultsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
):
    return await get_method_results(query, method_results_repository)


@method_results_router.get('/details/{method_result_id}', response_model=GetMethodResultDetailsResponse)
async def get_method_result_details_view(
        method_result_id: int,
        query: Annotated[GetMethodResultDetailsQuery, Depends(GetMethodResultDetailsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)],
):
    return await get_method_result_details(
        query=query,
        method_result_id=method_result_id,
        method_results_repository=method_results_repository,
        compare_settings_repository=compare_settings_repository
    )


@method_results_router.post('', response_model=CreateMethodResultsResponse)
async def create_method_results_view(
        request: CreateMethodResultsRequest,
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
):
    return await create_method_results(request, method_results_repository)
