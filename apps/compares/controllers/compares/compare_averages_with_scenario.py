from apps.compares.constants.compare_settings.context import CompareSettingsContext
from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import LoadTestResultCompare, BuildBaseCompareParams
from apps.compares.schema.compares.compare_averages_with_scenario import GetCompareAveragesWithScenarioQuery, \
    GetCompareAveragesWithScenarioResponse
from apps.services.schema.scenario_settings import ScenarioResultSettings
from services.postgres.repositories.compare_settings import CompareSettingsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository
from services.postgres.repositories.scenario_settings import ScenarioSettingsRepository


async def get_compare_averages_with_scenario(
        query: GetCompareAveragesWithScenarioQuery,
        compare_settings_repository: CompareSettingsRepository,
        load_test_results_repository: LoadTestResultsRepository,
        scenario_settings_repository: ScenarioSettingsRepository,
) -> GetCompareAveragesWithScenarioResponse:
    load_test_result_averages = await load_test_results_repository.get_averages(
        service_id=query.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    compare_settings = await compare_settings_repository.get_or_create(query.service_id)
    scenario_settings = await scenario_settings_repository.get_or_create(query.scenario_id)

    return GetCompareAveragesWithScenarioResponse(
        compare=LoadTestResultCompare.build(
            BuildBaseCompareParams(
                context=CompareSettingsContext.COMPARE_AVERAGES_WITH_SCENARIO,
                settings=CompareSettings.model_validate(compare_settings),
                actual_instance=load_test_result_averages,
                expected_instance=ScenarioResultSettings.model_validate(scenario_settings.result_settings)
            ),
        )
    )
