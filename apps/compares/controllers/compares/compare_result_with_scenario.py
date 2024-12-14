from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import MethodResultCompare, LoadTestResultCompare, \
    ResponseTimeCompareMetric, ContentLengthCompareMetric, MinResponseTimeCompareMetric, MaxResponseTimeCompareMetric, \
    NumberOfRequestsCompareMetric, NumberOfFailuresCompareMetric, RequestsPerSecondCompareMetric, \
    FailuresPerSecondCompareMetric, NumberOfUsersCompareMetric
from apps.compares.schema.compares.compare_result_with_scenario import GetCompareResultWithScenarioQuery, \
    GetCompareResultWithScenarioResponse, CompareResultWithScenario
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
    method_settings = scenario_settings.get_method_settings_or_default(method_result.method)

    return MethodResultCompare(
        method=method_result.method,
        settings=CompareSettings.model_validate(compare_settings),
        response_time=ResponseTimeCompareMetric(
            actual=method_result.average_response_time,
            expected=method_settings.get('response_time', 0.0)
        ),
        content_length=ContentLengthCompareMetric(
            actual=method_result.average_content_length,
            expected=method_settings.get('content_length', 0.0)
        ),
        min_response_time=MinResponseTimeCompareMetric(
            actual=method_result.min_response_time,
            expected=method_settings.get('min_response_time', 0.0)
        ),
        max_response_time=MaxResponseTimeCompareMetric(
            actual=method_result.max_response_time,
            expected=method_settings.get('max_response_time', 0.0)
        ),
        number_of_requests=NumberOfRequestsCompareMetric(
            actual=method_result.number_of_requests,
            expected=method_settings.get('number_of_requests', 0.0)
        ),
        number_of_failures=NumberOfFailuresCompareMetric(
            actual=method_result.number_of_failures,
            expected=method_settings.get('number_of_failures', 0.0)
        ),
        requests_per_second=RequestsPerSecondCompareMetric(
            actual=method_result.requests_per_second,
            expected=method_settings.get('requests_per_second', 0.0)
        ),
        failures_per_second=FailuresPerSecondCompareMetric(
            actual=method_result.failures_per_second,
            expected=method_settings.get('failures_per_second', 0.0)
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
            load_test_result_compare=LoadTestResultCompare(
                settings=CompareSettings.model_validate(compare_settings),
                response_time=ResponseTimeCompareMetric(
                    actual=load_test_result.average_response_time,
                    expected=scenario_settings.response_time
                ),
                number_of_users=NumberOfUsersCompareMetric(
                    actual=load_test_result.number_of_users,
                    expected=scenario_settings.number_of_users
                ),
                min_response_time=MinResponseTimeCompareMetric(
                    actual=load_test_result.min_response_time,
                    expected=scenario_settings.min_response_time
                ),
                max_response_time=MaxResponseTimeCompareMetric(
                    actual=load_test_result.max_response_time,
                    expected=scenario_settings.max_response_time
                ),
                number_of_requests=NumberOfRequestsCompareMetric(
                    actual=load_test_result.total_requests,
                    expected=scenario_settings.number_of_requests
                ),
                number_of_failures=NumberOfFailuresCompareMetric(
                    actual=load_test_result.total_failures,
                    expected=scenario_settings.number_of_failures
                ),
                failures_per_second=FailuresPerSecondCompareMetric(
                    actual=load_test_result.total_failures_per_second,
                    expected=scenario_settings.failures_per_second
                ),
                requests_per_second=RequestsPerSecondCompareMetric(
                    actual=load_test_result.total_requests_per_second,
                    expected=scenario_settings.requests_per_second
                )
            )
        )
    )
