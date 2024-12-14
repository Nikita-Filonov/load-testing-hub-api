from apps.compares.schema.compare_settings import CompareSettings
from apps.results.schema.load_test_results.compares import LoadTestResultSummaryCompare, \
    ResponseTimeLoadTestResultSummaryCompareMetric, \
    MinResponseTimeLoadTestResultSummaryCompareMetric, MaxResponseTimeLoadTestResultSummaryCompareMetric, \
    NumberOfRequestsLoadTestResultSummaryCompareMetric, NumberOfFailuresLoadTestResultSummaryCompareMetric, \
    RequestsPerSecondLoadTestResultSummaryCompareMetric, FailuresPerSecondLoadTestResultSummaryCompareMetric
from services.postgres.models import LoadTestResultsModel, CompareSettingsModel
from services.postgres.repositories.load_test_results import LoadTestResultsAverages


def get_load_test_result_summary_compare(
        result: LoadTestResultsModel,
        previous_result: LoadTestResultsModel | None,
        compare_settings: CompareSettingsModel,
        load_test_result_averages: LoadTestResultsAverages,
) -> LoadTestResultSummaryCompare:
    return LoadTestResultSummaryCompare(
        settings=CompareSettings.model_validate(compare_settings),
        previous_id=getattr(previous_result, 'id', None),
        response_time=ResponseTimeLoadTestResultSummaryCompareMetric(
            actual=result.average_response_time,
            average=load_test_result_averages.response_time,
            previous=getattr(previous_result, 'average_response_time', 0.0)
        ),
        min_response_time=MinResponseTimeLoadTestResultSummaryCompareMetric(
            actual=result.min_response_time,
            average=load_test_result_averages.min_response_time,
            previous=getattr(previous_result, 'min_response_time', 0.0)
        ),
        max_response_time=MaxResponseTimeLoadTestResultSummaryCompareMetric(
            actual=result.max_response_time,
            average=load_test_result_averages.max_response_time,
            previous=getattr(previous_result, 'max_response_time', 0.0)
        ),
        number_of_requests=NumberOfRequestsLoadTestResultSummaryCompareMetric(
            actual=result.total_requests,
            average=load_test_result_averages.total_requests,
            previous=getattr(previous_result, 'total_requests', 0.0)
        ),
        number_of_failures=NumberOfFailuresLoadTestResultSummaryCompareMetric(
            actual=result.total_failures,
            average=load_test_result_averages.total_failures,
            previous=getattr(previous_result, 'total_failures', 0.0)
        ),
        requests_per_second=RequestsPerSecondLoadTestResultSummaryCompareMetric(
            actual=result.total_requests_per_second,
            average=load_test_result_averages.total_requests_per_second,
            previous=getattr(previous_result, 'total_requests_per_second', 0.0)
        ),
        failures_per_second=FailuresPerSecondLoadTestResultSummaryCompareMetric(
            actual=result.total_failures_per_second,
            average=load_test_result_averages.total_failures_per_second,
            previous=getattr(previous_result, 'total_failures_per_second', 0.0)
        ),
    )
