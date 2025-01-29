from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import MethodResultCompare, BuildMethodResultCompare
from apps.compares.schema.compares.compare_method_with_scenario import GetCompareMethodWithScenarioQuery, \
    GetCompareMethodWithScenarioResponse
from apps.services.schema.scenario_settings import ScenarioMethodSettings
from services.postgres.models.compare_settings import CompareSettingsContext
from services.postgres.repositories.compare_settings import CompareSettingsRepository
from services.postgres.repositories.method_results import MethodResultsRepository
from services.postgres.repositories.scenario_settings import ScenarioSettingsRepository


async def get_compare_method_with_scenario(
        query: GetCompareMethodWithScenarioQuery,
        method_results_repository: MethodResultsRepository,
        compare_settings_repository: CompareSettingsRepository,
        scenario_settings_repository: ScenarioSettingsRepository,
) -> GetCompareMethodWithScenarioResponse:
    method_result_averages = await method_results_repository.get_averages(
        method=query.method,
        service_id=query.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    compare_settings = await compare_settings_repository.get_or_create(query.service_id)
    scenario_settings = await scenario_settings_repository.get_or_create(query.scenario_id)
    method_settings = scenario_settings.get_method_settings_or_default(query.method)

    return GetCompareMethodWithScenarioResponse(
        compare=MethodResultCompare.build(
            BuildMethodResultCompare(
                method=query.method,
                context=CompareSettingsContext.COMPARE_METHOD_WITH_SCENARIO,
                settings=CompareSettings.model_validate(compare_settings),
                actual_instance=method_result_averages,
                expected_instance=ScenarioMethodSettings.model_validate(method_settings)
            ),
        )
    )
