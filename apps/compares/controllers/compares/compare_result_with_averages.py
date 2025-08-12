from apps.compares.constants.compare_settings.context import CompareSettingsContext
from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import (
    MethodResultCompare,
    LoadTestResultCompare,
    BuildBaseCompareParams,
    BuildMethodResultCompare
)
from apps.compares.schema.compares.compare_result_with_averages import (
    CompareResultWithAverages,
    GetCompareResultWithAveragesQuery,
    GetCompareResultWithAveragesResponse,
)
from services.postgres.models import MethodResultsModel, CompareSettingsModel
from services.postgres.repositories.compare_settings import CompareSettingsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository
from services.postgres.repositories.method_results import MethodResultsRepository, MethodResultsAverages


def get_method_result_compare(
        settings: CompareSettingsModel,
        method_result: MethodResultsModel,
        method_results_averages: MethodResultsAverages
) -> MethodResultCompare:
    return MethodResultCompare.build(
        BuildMethodResultCompare(
            method=method_result.method,
            context=CompareSettingsContext.COMPARE_RESULT_WITH_AVERAGES,
            settings=CompareSettings.model_validate(settings),
            protocol=method_result.protocol,
            actual_instance=method_result,
            expected_instance=method_results_averages
        ),
    )


async def get_compare_result_with_averages(
        query: GetCompareResultWithAveragesQuery,
        method_results_repository: MethodResultsRepository,
        compare_settings_repository: CompareSettingsRepository,
        load_test_results_repository: LoadTestResultsRepository
) -> GetCompareResultWithAveragesResponse:
    load_test_result = await load_test_results_repository.get_by_id(query.load_test_result_id)
    load_test_result_averages = await load_test_results_repository.get_averages(
        service_id=load_test_result.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    method_results = await method_results_repository.filter_by_load_test_result_id(query.load_test_result_id)
    method_results_averages = await method_results_repository.get_averages_for_method_results(
        results=method_results,
        service_id=load_test_result.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    compare_settings = await compare_settings_repository.get_or_create(load_test_result.service_id)

    return GetCompareResultWithAveragesResponse(
        compare=CompareResultWithAverages(
            method_result_compares=[
                get_method_result_compare(
                    settings=compare_settings,
                    method_result=method_result,
                    method_results_averages=method_results_averages[method_result]
                )
                for method_result in method_results
            ],
            load_test_result_compare=LoadTestResultCompare.build(
                BuildBaseCompareParams(
                    context=CompareSettingsContext.COMPARE_RESULT_WITH_AVERAGES,
                    settings=CompareSettings.model_validate(compare_settings),
                    actual_instance=load_test_result,
                    expected_instance=load_test_result_averages
                ),
            )
        )
    )
