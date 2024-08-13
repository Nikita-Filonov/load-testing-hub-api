from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.services.controllers.scenario_settings import get_scenario_settings, update_scenario_settings
from apps.services.schema.scenario_settings import GetScenarioSettingsResponse, UpdateScenarioSettingsRequest
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

scenario_settings_router = APIRouter(
    prefix=APIRoutes.SCENARIO_SETTINGS,
    tags=[APIRoutes.SCENARIO_SETTINGS.as_tag()]
)


@scenario_settings_router.get('/{scenario}', response_model=GetScenarioSettingsResponse)
async def get_scenario_settings_view(
        scenario: str,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_scenario_settings(scenario, session)


@scenario_settings_router.post('', response_model=GetScenarioSettingsResponse)
async def update_scenario_settings_view(
        request: UpdateScenarioSettingsRequest,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await update_scenario_settings(request, session)
