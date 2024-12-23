from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import ResponseTimeCompareMetric, MinResponseTimeCompareMetric, \
    MaxResponseTimeCompareMetric, NumberOfRequestsCompareMetric, NumberOfFailuresCompareMetric, \
    RequestsPerSecondCompareMetric, FailuresPerSecondCompareMetric
from apps.results.schema.load_test_results.compares import LoadTestResultSummaryCompare, \
    LoadTestResultCompareWithAverage, LoadTestResultCompareWithPrevious
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
        compare_with_average=LoadTestResultCompareWithAverage(
            settings=settings,
            response_time=ResponseTimeCompareMetric(
                actual=result.average_response_time,
                expected=load_test_result_averages.response_time
            ),
            min_response_time=MinResponseTimeCompareMetric(
                actual=result.min_response_time,
                expected=load_test_result_averages.min_response_time
            ),
            max_response_time=MaxResponseTimeCompareMetric(
                actual=result.max_response_time,
                expected=load_test_result_averages.max_response_time
            ),
            number_of_requests=NumberOfRequestsCompareMetric(
                actual=result.total_requests,
                expected=load_test_result_averages.total_requests
            ),
            number_of_failures=NumberOfFailuresCompareMetric(
                actual=result.total_failures,
                expected=load_test_result_averages.total_failures
            ),
            requests_per_second=RequestsPerSecondCompareMetric(
                actual=result.total_requests_per_second,
                expected=load_test_result_averages.total_requests_per_second
            ),
            failures_per_second=FailuresPerSecondCompareMetric(
                actual=result.total_failures_per_second,
                expected=load_test_result_averages.total_failures_per_second
            )
        ),
        compare_with_previous=LoadTestResultCompareWithPrevious(
            settings=settings,
            response_time=ResponseTimeCompareMetric(
                actual=result.average_response_time,
                expected=getattr(previous_result, 'average_response_time', 0.0)
            ),
            min_response_time=MinResponseTimeCompareMetric(
                actual=result.min_response_time,
                expected=getattr(previous_result, 'min_response_time', 0.0)
            ),
            max_response_time=MaxResponseTimeCompareMetric(
                actual=result.max_response_time,
                expected=getattr(previous_result, 'max_response_time', 0.0)
            ),
            number_of_requests=NumberOfRequestsCompareMetric(
                actual=result.total_requests,
                expected=getattr(previous_result, 'total_requests', 0.0)
            ),
            number_of_failures=NumberOfFailuresCompareMetric(
                actual=result.total_failures,
                expected=getattr(previous_result, 'total_failures', 0.0)
            ),
            requests_per_second=RequestsPerSecondCompareMetric(
                actual=result.total_requests_per_second,
                expected=getattr(previous_result, 'total_requests_per_second', 0.0)
            ),
            failures_per_second=FailuresPerSecondCompareMetric(
                actual=result.total_failures_per_second,
                expected=getattr(previous_result, 'total_failures_per_second', 0.0)
            )
        ),
    )
