from typing import Annotated

from fastapi import APIRouter, Depends

from apps.services.controllers.scenarios import get_scenarios, create_scenario, get_scenario_details, update_scenario, \
    delete_scenario, get_scenario
from apps.services.schema.scenarios import GetScenariosResponse, GetScenariosQuery, CreateScenarioRequest, \
    GetScenarioDetailsResponse, UpdateScenarioRequest, GetScenarioResponse
from services.postgres.repositories.load_test_results import LoadTestResultsRepository, get_load_test_results_repository
from services.postgres.repositories.scenario_settings import ScenarioSettingsRepository, \
    get_scenario_settings_repository
from services.postgres.repositories.scenarios import ScenariosRepository, get_scenarios_repository
from utils.routes import APIRoutes

scenarios_router = APIRouter(
    prefix=APIRoutes.SCENARIOS,
    tags=[APIRoutes.SCENARIOS.as_tag()]
)


@scenarios_router.get('/{scenario_id}', response_model=GetScenarioResponse)
async def get_scenario_view(
        scenario_id: int,
        scenarios_repository: Annotated[ScenariosRepository, Depends(get_scenarios_repository)]
):
    return await get_scenario(scenario_id, scenarios_repository)


@scenarios_router.get('', response_model=GetScenariosResponse)
async def get_scenarios_view(
        query: Annotated[GetScenariosQuery, Depends(GetScenariosQuery.as_query)],
        scenarios_repository: Annotated[ScenariosRepository, Depends(get_scenarios_repository)]
):
    return await get_scenarios(query, scenarios_repository)


@scenarios_router.get('/details/{scenario_id}', response_model=GetScenarioDetailsResponse)
async def get_scenario_details_view(
        scenario_id: int,
        scenarios_repository: Annotated[ScenariosRepository, Depends(get_scenarios_repository)]
):
    return await get_scenario_details(scenario_id, scenarios_repository)


@scenarios_router.post('', response_model=GetScenarioDetailsResponse)
async def create_scenario_view(
        request: CreateScenarioRequest,
        scenarios_repository: Annotated[ScenariosRepository, Depends(get_scenarios_repository)],
        scenario_settings_repository: Annotated[ScenarioSettingsRepository, Depends(get_scenario_settings_repository)]
):
    return await create_scenario(
        request,
        scenarios_repository=scenarios_repository,
        scenario_settings_repository=scenario_settings_repository
    )


@scenarios_router.patch('/{scenario_id}', response_model=GetScenarioDetailsResponse)
async def update_scenario_view(
        scenario_id: int,
        request: UpdateScenarioRequest,
        scenarios_repository: Annotated[ScenariosRepository, Depends(get_scenarios_repository)],
):
    return await update_scenario(scenario_id, request, scenarios_repository)


@scenarios_router.delete('/{scenario_id}')
async def delete_scenario_view(
        scenario_id: int,
        scenarios_repository: Annotated[ScenariosRepository, Depends(get_scenarios_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
):
    return await delete_scenario(
        scenario_id,
        scenarios_repository=scenarios_repository,
        load_test_results_repository=load_test_results_repository
    )
