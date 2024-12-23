from typing import Annotated

from fastapi import APIRouter, Depends

from apps.results.controllers.load_test_results.controllers import create_load_test_result, \
    delete_load_test_result, update_load_test_result
from apps.results.controllers.load_test_results.details import get_load_test_result_details
from apps.results.controllers.load_test_results.results import get_load_test_results
from apps.results.schema.load_test_results.results import GetLoadTestResultsQuery, GetLoadTestResultsResponse, \
    GetLoadTestResultDetailsResponse, CreateLoadTestResultRequest, UpdateLoadTestResultRequest, \
    GetLoadTestResultDetailsQuery, UpdateLoadTestResultQuery
from services.postgres.repositories.compare_settings import CompareSettingsRepository, get_compare_settings_repository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository, get_load_test_results_repository
from services.postgres.repositories.method_results import MethodResultsRepository, get_method_results_repository
from utils.routes import APIRoutes

load_test_results_router = APIRouter(
    prefix=APIRoutes.LOAD_TEST_RESULTS,
    tags=[APIRoutes.LOAD_TEST_RESULTS.as_tag()]
)


@load_test_results_router.get('', response_model=GetLoadTestResultsResponse)
async def get_load_test_results_view(
        query: Annotated[GetLoadTestResultsQuery, Depends(GetLoadTestResultsQuery.as_query)],
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)]
):
    return await get_load_test_results(
        query,
        compare_settings_repository=compare_settings_repository,
        load_test_results_repository=load_test_results_repository
    )


@load_test_results_router.get(
    '/details/{load_test_result_id}',
    response_model=GetLoadTestResultDetailsResponse
)
async def get_load_test_result_details_view(
        load_test_result_id: int,
        query: Annotated[GetLoadTestResultDetailsQuery, Depends(GetLoadTestResultDetailsQuery.as_query)],
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)]
):
    return await get_load_test_result_details(
        query=query,
        load_test_result_id=load_test_result_id,
        compare_settings_repository=compare_settings_repository,
        load_test_results_repository=load_test_results_repository
    )


@load_test_results_router.post('', response_model=GetLoadTestResultDetailsResponse)
async def create_load_test_result_view(
        request: CreateLoadTestResultRequest,
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
):
    return await create_load_test_result(
        request,
        compare_settings_repository=compare_settings_repository,
        load_test_results_repository=load_test_results_repository
    )


@load_test_results_router.patch(
    '/{load_test_result_id}',
    response_model=GetLoadTestResultDetailsResponse
)
async def update_load_test_result_view(
        load_test_result_id: int,
        request: UpdateLoadTestResultRequest,
        query: Annotated[UpdateLoadTestResultQuery, Depends(UpdateLoadTestResultQuery.as_query)],
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
):
    return await update_load_test_result(
        query=query,
        request=request,
        load_test_result_id=load_test_result_id,
        compare_settings_repository=compare_settings_repository,
        load_test_results_repository=load_test_results_repository
    )


@load_test_results_router.delete('/{load_test_result_id}')
async def delete_load_test_result_view(
        load_test_result_id: int,
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
):
    return await delete_load_test_result(
        load_test_result_id,
        method_results_repository=method_results_repository,
        load_test_results_repository=load_test_results_repository
    )
