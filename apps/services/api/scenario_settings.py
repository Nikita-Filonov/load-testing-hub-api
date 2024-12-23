from typing import Annotated

from fastapi import APIRouter, Depends

from apps.services.controllers.scenario_settings import get_scenario_settings, update_scenario_settings
from apps.services.schema.scenario_settings import GetScenarioSettingsResponse, UpdateScenarioSettingsRequest
from services.postgres.repositories.scenario_settings import ScenarioSettingsRepository, \
    get_scenario_settings_repository
from utils.routes import APIRoutes

scenario_settings_router = APIRouter(
    prefix=APIRoutes.SCENARIO_SETTINGS,
    tags=[APIRoutes.SCENARIO_SETTINGS.as_tag()]
)


@scenario_settings_router.get('/{scenario_id}', response_model=GetScenarioSettingsResponse)
async def get_scenario_settings_view(
        scenario_id: int,
        scenario_settings_repository: Annotated[ScenarioSettingsRepository, Depends(get_scenario_settings_repository)],
):
    return await get_scenario_settings(scenario_id, scenario_settings_repository)


@scenario_settings_router.patch('/{scenario_id}', response_model=GetScenarioSettingsResponse)
async def update_scenario_settings_view(
        scenario_id: int,
        request: UpdateScenarioSettingsRequest,
        scenario_settings_repository: Annotated[ScenarioSettingsRepository, Depends(get_scenario_settings_repository)],
):
    return await update_scenario_settings(scenario_id, request, scenario_settings_repository)
