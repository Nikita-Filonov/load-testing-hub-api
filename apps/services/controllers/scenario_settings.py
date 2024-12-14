from apps.services.schema.scenario_settings import GetScenarioSettingsResponse, \
    ScenarioSettings, UpdateScenarioSettingsRequest
from services.postgres.repositories.scenario_settings import ScenarioSettingsRepository


async def get_scenario_settings(
        scenario_id: int,
        scenario_settings_repository: ScenarioSettingsRepository,
) -> GetScenarioSettingsResponse:
    settings = await scenario_settings_repository.get_or_create(scenario_id)

    return GetScenarioSettingsResponse(settings=ScenarioSettings.model_validate(settings))


async def update_scenario_settings(
        scenario_id: int,
        request: UpdateScenarioSettingsRequest,
        scenario_settings_repository: ScenarioSettingsRepository,
) -> GetScenarioSettingsResponse:
    settings = await scenario_settings_repository.update(
        scenario_id, request.model_dump(exclude_unset=True)
    )

    return GetScenarioSettingsResponse(settings=ScenarioSettings.model_validate(settings))
