from apps.compares.constants.compare_settings.context import CompareSettingsContext
from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import (
    MethodResultCompare,
    LoadTestResultCompare,
    BuildBaseCompareParams,
    BuildMethodResultCompare
)
from apps.compares.schema.compares.compare_result_with_scenario import (
    CompareResultWithScenario,
    GetCompareResultWithScenarioQuery,
    GetCompareResultWithScenarioResponse,
)
from apps.services.schema.scenario_settings import ScenarioMethodSettings, ScenarioResultSettings
from services.postgres.models import MethodResultsModel, CompareSettingsModel, ScenarioSettingsModel
from services.postgres.repositories.compare_settings import CompareSettingsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository
from services.postgres.repositories.method_results import MethodResultsRepository
from services.postgres.repositories.scenario_settings import ScenarioSettingsRepository


def get_method_result_compare(
        method_result: MethodResultsModel,
        compare_settings: CompareSettingsModel,
        scenario_settings: ScenarioSettingsModel,
) -> MethodResultCompare:
    method_settings = scenario_settings.get_method_settings_or_default(
        method=method_result.method,
        protocol=method_result.protocol
    )

    return MethodResultCompare.build(
        BuildMethodResultCompare(
            method=method_result.method,
            context=CompareSettingsContext.COMPARE_RESULT_WITH_SCENARIO,
            settings=CompareSettings.model_validate(compare_settings),
            protocol=method_result.protocol,
            actual_instance=method_result,
            expected_instance=ScenarioMethodSettings.model_validate(method_settings)
        ),
    )


async def get_compare_result_with_scenario(
        query: GetCompareResultWithScenarioQuery,
        method_results_repository: MethodResultsRepository,
        compare_settings_repository: CompareSettingsRepository,
        scenario_settings_repository: ScenarioSettingsRepository,
        load_test_results_repository: LoadTestResultsRepository,
) -> GetCompareResultWithScenarioResponse:
    load_test_result = await load_test_results_repository.get_by_id(query.load_test_result_id)
    method_results = await method_results_repository.filter_by_load_test_result_id(query.load_test_result_id)

    compare_settings = await compare_settings_repository.get_or_create(load_test_result.service_id)
    scenario_settings = await scenario_settings_repository.get_or_create(load_test_result.scenario_id)

    return GetCompareResultWithScenarioResponse(
        compare=CompareResultWithScenario(
            scenario=load_test_result.scenario,
            method_result_compares=[
                get_method_result_compare(
                    method_result=method_result,
                    compare_settings=compare_settings,
                    scenario_settings=scenario_settings
                )
                for method_result in method_results
            ],
            load_test_result_compare=LoadTestResultCompare.build(
                BuildBaseCompareParams(
                    context=CompareSettingsContext.COMPARE_RESULT_WITH_SCENARIO,
                    settings=CompareSettings.model_validate(compare_settings),
                    actual_instance=load_test_result,
                    expected_instance=ScenarioResultSettings.model_validate(scenario_settings.result_settings)
                )
            )
        )
    )
