from typing import Annotated

from fastapi import APIRouter, Depends

from apps.compares.controllers.compares.compare_method_with_scenario import get_compare_method_with_scenario
from apps.compares.schema.compares.compare_method_with_scenario import GetCompareMethodWithScenarioQuery, \
    GetCompareMethodWithScenarioResponse
from services.postgres.repositories.compare_settings import CompareSettingsRepository, get_compare_settings_repository
from services.postgres.repositories.method_results import MethodResultsRepository, get_method_results_repository
from services.postgres.repositories.scenario_settings import ScenarioSettingsRepository, \
    get_scenario_settings_repository
from utils.routes import APIRoutes

compare_method_with_scenario_router = APIRouter(
    prefix=APIRoutes.COMPARES,
    tags=[APIRoutes.COMPARES.as_tag()]
)


@compare_method_with_scenario_router.get(
    '/compare-method-with-scenario',
    response_model=GetCompareMethodWithScenarioResponse
)
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
