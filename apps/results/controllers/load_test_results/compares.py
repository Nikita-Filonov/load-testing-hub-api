from apps.compares.constants.compare_settings.context import CompareSettingsContext
from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import BuildBaseCompareParams
from apps.results.schema.load_test_results.compares import LoadTestResultSummaryCompare, LoadTestResultCompareSimple
from services.postgres.models import LoadTestResultsModel, CompareSettingsModel
from services.postgres.repositories.load_test_results import LoadTestResultsAverages


def get_load_test_result_summary_compare(
        result: LoadTestResultsModel,
        previous_result: LoadTestResultsModel | None,
        compare_settings: CompareSettingsModel,
        load_test_result_averages: LoadTestResultsAverages,
) -> LoadTestResultSummaryCompare:
    settings = CompareSettings.model_validate(compare_settings)

    return LoadTestResultSummaryCompare(
        previous_id=getattr(previous_result, 'id', None),
        compare_with_average=LoadTestResultCompareSimple.build(
            BuildBaseCompareParams(
                context=CompareSettingsContext.COMPARE_WITH_AVERAGE,
                settings=settings,
                actual_instance=result,
                expected_instance=load_test_result_averages
            ),
        ),
        compare_with_previous=LoadTestResultCompareSimple.build(
            BuildBaseCompareParams(
                context=CompareSettingsContext.COMPARE_WITH_PREVIOUS,
                settings=settings,
                actual_instance=result,
                expected_instance=previous_result
            )
        ),
    )
