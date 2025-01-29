from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import BuildMethodResultCompare
from apps.results.schema.method_results.compares import MethodResultSummaryCompare, MethodResultCompareSimple
from services.postgres.models import MethodResultsModel, CompareSettingsModel
from services.postgres.models.compare_settings import CompareSettingsContext
from services.postgres.repositories.method_results import MethodResultsAverages


def get_method_result_summary_compare(
        result: MethodResultsModel,
        previous_result: MethodResultsModel | None,
        compare_settings: CompareSettingsModel,
        method_result_averages: MethodResultsAverages,
) -> MethodResultSummaryCompare:
    settings = CompareSettings.model_validate(compare_settings)

    return MethodResultSummaryCompare(
        compare_with_average=MethodResultCompareSimple.build(
            BuildMethodResultCompare(
                method=result.method,
                context=CompareSettingsContext.COMPARE_WITH_AVERAGE,
                settings=settings,
                actual_instance=result,
                expected_instance=method_result_averages
            ),
        ),
        compare_with_previous=MethodResultCompareSimple.build(
            BuildMethodResultCompare(
                method=result.method,
                context=CompareSettingsContext.COMPARE_WITH_PREVIOUS,
                settings=settings,
                actual_instance=result,
                expected_instance=previous_result
            )
        ),
    )
