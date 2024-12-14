from apps.services.schema.scenarios import CreateScenarioRequest, GetScenariosQuery, GetScenariosResponse, Scenario, \
    GetScenarioDetailsResponse, ScenarioDetails, UpdateScenarioRequest, GetScenarioResponse
from services.postgres.repositories.load_test_results import LoadTestResultsRepository
from services.postgres.repositories.scenario_settings import ScenarioSettingsRepository
from services.postgres.repositories.scenarios import ScenariosRepository


async def get_scenario(
        scenario_id: int,
        scenarios_repository: ScenariosRepository
) -> GetScenarioResponse:
    scenario = await scenarios_repository.get_by_id(scenario_id)

    return GetScenarioResponse(scenario=Scenario.model_validate(scenario))


async def get_scenarios(
        query: GetScenariosQuery,
        scenarios_repository: ScenariosRepository
) -> GetScenariosResponse:
    scenarios = await scenarios_repository.filter(service_id=query.service_id)

    return GetScenariosResponse(
        scenarios=[Scenario.model_validate(scenario) for scenario in scenarios]
    )


async def create_scenario(
        request: CreateScenarioRequest,
        scenarios_repository: ScenariosRepository,
        scenario_settings_repository: ScenarioSettingsRepository
) -> GetScenarioDetailsResponse:
    scenario = await scenarios_repository.create(request.model_dump(mode='json'))
    await scenario_settings_repository.get_or_create(scenario.id)

    return GetScenarioDetailsResponse(details=ScenarioDetails.model_validate(scenario))


async def update_scenario(
        scenario_id: int,
        request: UpdateScenarioRequest,
        scenarios_repository: ScenariosRepository,
) -> GetScenarioDetailsResponse:
    scenario = await scenarios_repository.update(
        scenario_id, request.model_dump(mode='json', exclude_unset=True)
    )

    return GetScenarioDetailsResponse(details=ScenarioDetails.model_validate(scenario))


async def delete_scenario(
        scenario_id: int,
        scenarios_repository: ScenariosRepository,
        load_test_results_repository: LoadTestResultsRepository
):
    await scenarios_repository.delete(scenario_id=scenario_id)
    await load_test_results_repository.delete(scenario_id=scenario_id)


async def get_scenario_details(
        scenario_id: int,
        scenarios_repository: ScenariosRepository
) -> GetScenarioDetailsResponse:
    scenario = await scenarios_repository.get_by_id(scenario_id)

    return GetScenarioDetailsResponse(
        details=ScenarioDetails.model_validate(scenario)
    )
