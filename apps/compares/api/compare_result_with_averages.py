from typing import Annotated

from fastapi import APIRouter, Depends

from apps.compares.controllers.compares.compare_result_with_averages import get_compare_result_with_averages
from apps.compares.schema.compares.compare_result_with_averages import GetCompareResultWithAveragesResponse, \
    GetCompareResultWithAveragesQuery
from services.postgres.repositories.compare_settings import CompareSettingsRepository, get_compare_settings_repository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository, get_load_test_results_repository
from services.postgres.repositories.method_results import MethodResultsRepository, get_method_results_repository
from utils.routes import APIRoutes

compare_result_with_averages_router = APIRouter(
    prefix=APIRoutes.COMPARES,
    tags=[APIRoutes.COMPARES.as_tag()]
)


@compare_result_with_averages_router.get(
    '/compare-result-with-averages',
    response_model=GetCompareResultWithAveragesResponse
)
async def get_compare_result_with_averages_view(
        query: Annotated[GetCompareResultWithAveragesQuery, Depends(GetCompareResultWithAveragesQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
):
    return await get_compare_result_with_averages(
        query,
        method_results_repository=method_results_repository,
        compare_settings_repository=compare_settings_repository,
        load_test_results_repository=load_test_results_repository,
    )
