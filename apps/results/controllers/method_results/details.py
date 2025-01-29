from apps.results.controllers.method_results.compares import get_method_result_summary_compare
from apps.results.schema.method_results.results import GetMethodResultDetailsResponse, GetMethodResultDetailsQuery, \
    MethodResultDetails
from services.postgres.repositories.compare_settings import CompareSettingsRepository
from services.postgres.repositories.method_results import MethodResultsRepository


async def get_method_result_details(
        method_result_id: int,
        query: GetMethodResultDetailsQuery,
        method_results_repository: MethodResultsRepository,
        compare_settings_repository: CompareSettingsRepository,
) -> GetMethodResultDetailsResponse:
    result = await method_results_repository.get_by_id(method_result_id)
    previous_result = await method_results_repository.get_previous(
        method=result.method,
        service_id=result.service_id,
        scenario_id=query.scenario_id,
        method_result_id=method_result_id
    )

    compare_settings = await compare_settings_repository.get_or_create(result.service_id)
    method_result_averages = await method_results_repository.get_averages(
        method=result.method,
        service_id=result.service_id,
        scenario_id=query.scenario_id
    )

    details = MethodResultDetails.model_validate(result)
    details.compare = get_method_result_summary_compare(
        result=result,
        previous_result=previous_result,
        compare_settings=compare_settings,
        method_result_averages=method_result_averages
    )

    return GetMethodResultDetailsResponse(details=details)
