from sqlalchemy.ext.asyncio import AsyncSession

from apps.services.schema.scenario_settings import GetScenarioSettingsResponse, \
    ScenarioSettings, UpdateScenarioSettingsRequest
from services.postgres.models import ScenarioSettingsModel


async def get_scenario_settings(
        scenario: str,
        session: AsyncSession
) -> GetScenarioSettingsResponse:
    settings = await ScenarioSettingsModel.get(
        session,
        clause_filter=(ScenarioSettingsModel.scenario == scenario,),
    )

    return GetScenarioSettingsResponse(settings=ScenarioSettings.model_validate(settings))


async def update_scenario_settings(
        request: UpdateScenarioSettingsRequest,
        session: AsyncSession
) -> GetScenarioSettingsResponse:
    settings = await ScenarioSettingsModel.update(
        session,
        clause_filter=(ScenarioSettingsModel.scenario == request.settings.scenario,),
        **request.settings.model_dump(exclude={'scenario'})
    )

    return GetScenarioSettingsResponse(settings=ScenarioSettings.model_validate(settings))
