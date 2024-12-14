from typing import Annotated

from fastapi import APIRouter, Depends

from apps.compares.controllers.compares.compare_averages_with_scenario import get_compare_averages_with_scenario
from apps.compares.controllers.compares.compare_history_results import get_compare_history_results
from apps.compares.controllers.compares.compare_method_with_scenario import get_compare_method_with_scenario
from apps.compares.controllers.compares.compare_result_with_averages import get_compare_result_with_averages
from apps.compares.controllers.compares.compare_result_with_results.compares import get_compare_result_with_results
from apps.compares.controllers.compares.compare_result_with_scenario import get_compare_result_with_scenario
from apps.compares.schema.compares.compare_averages_with_scenario import GetCompareAveragesWithScenarioQuery, \
    GetCompareAveragesWithScenarioResponse
from apps.compares.schema.compares.compare_history_results import GetCompareHistoryResultsResponse
from apps.compares.schema.compares.compare_method_with_scenario import GetCompareMethodWithScenarioQuery, \
    GetCompareMethodWithScenarioResponse
from apps.compares.schema.compares.compare_result_with_averages import GetCompareResultWithAveragesResponse, \
    GetCompareResultWithAveragesQuery
from apps.compares.schema.compares.compare_result_with_results import GetCompareResultWithResultsQuery, \
    GetCompareResultWithResultsResponse
from apps.compares.schema.compares.compare_result_with_scenario import GetCompareResultWithScenarioQuery, \
    GetCompareResultWithScenarioResponse
from services.postgres.repositories.compare_settings import CompareSettingsRepository, get_compare_settings_repository
from services.postgres.repositories.history_results import HistoryResultsRepository, get_history_results_repository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository, get_load_test_results_repository
from services.postgres.repositories.method_results import MethodResultsRepository, get_method_results_repository
from services.postgres.repositories.scenario_settings import ScenarioSettingsRepository, \
    get_scenario_settings_repository
from utils.routes import APIRoutes

compares_router = APIRouter(
    prefix=APIRoutes.COMPARES,
    tags=[APIRoutes.COMPARES.as_tag()]
)


@compares_router.get('/compare-result-with-results', response_model=GetCompareResultWithResultsResponse)
async def get_compare_result_with_results_view(
        query: Annotated[GetCompareResultWithResultsQuery, Depends(GetCompareResultWithResultsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)]
):
    return await get_compare_result_with_results(
        query,
        method_results_repository=method_results_repository,
        compare_settings_repository=compare_settings_repository,
        load_test_results_repository=load_test_results_repository
    )


@compares_router.get('/compare-result-with-scenario', response_model=GetCompareResultWithScenarioResponse)
async def get_compare_result_with_scenario_view(
        query: Annotated[GetCompareResultWithScenarioQuery, Depends(GetCompareResultWithScenarioQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
        scenario_settings_repository: Annotated[ScenarioSettingsRepository, Depends(get_scenario_settings_repository)],
):
    return await get_compare_result_with_scenario(
        query,
        method_results_repository=method_results_repository,
        compare_settings_repository=compare_settings_repository,
        load_test_results_repository=load_test_results_repository,
        scenario_settings_repository=scenario_settings_repository
    )


@compares_router.get('/compare-result-with-averages', response_model=GetCompareResultWithAveragesResponse)
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


@compares_router.get('/compare-history-results', response_model=GetCompareHistoryResultsResponse)
async def get_compare_history_results_view(
        query: Annotated[GetCompareResultWithResultsQuery, Depends(GetCompareResultWithResultsQuery.as_query)],
        history_results_repository: Annotated[HistoryResultsRepository, Depends(get_history_results_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)]
):
    return await get_compare_history_results(
        query,
        history_results_repository=history_results_repository,
        load_test_results_repository=load_test_results_repository
    )


@compares_router.get('/compare-method-with-scenario', response_model=GetCompareMethodWithScenarioResponse)
async def get_compare_method_with_scenario_view(
        query: Annotated[GetCompareMethodWithScenarioQuery, Depends(GetCompareMethodWithScenarioQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)],
        scenario_settings_repository: Annotated[ScenarioSettingsRepository, Depends(get_scenario_settings_repository)],
):
    return await get_compare_method_with_scenario(
        query,
        method_results_repository=method_results_repository,
        compare_settings_repository=compare_settings_repository,
        scenario_settings_repository=scenario_settings_repository
    )


@compares_router.get('/compare-averages-with-scenario', response_model=GetCompareAveragesWithScenarioResponse)
async def get_compare_averages_with_scenario_view(
        query: Annotated[GetCompareAveragesWithScenarioQuery, Depends(GetCompareAveragesWithScenarioQuery.as_query)],
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
        scenario_settings_repository: Annotated[ScenarioSettingsRepository, Depends(get_scenario_settings_repository)],
):
    return await get_compare_averages_with_scenario(
        query,
        compare_settings_repository=compare_settings_repository,
        load_test_results_repository=load_test_results_repository,
        scenario_settings_repository=scenario_settings_repository
    )
