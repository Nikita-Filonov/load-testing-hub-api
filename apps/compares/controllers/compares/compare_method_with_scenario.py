from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import MethodResultCompare, ResponseTimeCompareMetric, \
    ContentLengthCompareMetric, MinResponseTimeCompareMetric, MaxResponseTimeCompareMetric, \
    NumberOfRequestsCompareMetric, NumberOfFailuresCompareMetric, RequestsPerSecondCompareMetric, \
    FailuresPerSecondCompareMetric
from apps.compares.schema.compares.compare_method_with_scenario import GetCompareMethodWithScenarioQuery, \
    GetCompareMethodWithScenarioResponse
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
        compare=MethodResultCompare(
            method=query.method,
            context=CompareSettingsContext.COMPARE_METHOD_WITH_SCENARIO,
            settings=CompareSettings.model_validate(compare_settings),
            response_time=ResponseTimeCompareMetric(
                actual=method_result_averages.response_time,
                expected=method_settings.get('response_time', 0.0)
            ),
            content_length=ContentLengthCompareMetric(
                actual=method_result_averages.content_length,
                expected=method_settings.get('content_length', 0.0)
            ),
            min_response_time=MinResponseTimeCompareMetric(
                actual=method_result_averages.min_response_time,
                expected=method_settings.get('min_response_time', 0.0)
            ),
            max_response_time=MaxResponseTimeCompareMetric(
                actual=method_result_averages.max_response_time,
                expected=method_settings.get('max_response_time', 0.0)
            ),
            number_of_requests=NumberOfRequestsCompareMetric(
                actual=method_result_averages.number_of_requests,
                expected=method_settings.get('number_of_requests', 0.0)
            ),
            number_of_failures=NumberOfFailuresCompareMetric(
                actual=method_result_averages.number_of_failures,
                expected=method_settings.get('number_of_failures', 0.0)
            ),
            requests_per_second=RequestsPerSecondCompareMetric(
                actual=method_result_averages.requests_per_second,
                expected=method_settings.get('requests_per_second', 0.0)
            ),
            failures_per_second=FailuresPerSecondCompareMetric(
                actual=method_result_averages.failures_per_second,
                expected=method_settings.get('failures_per_second', 0.0)
            ),
        )
    )
