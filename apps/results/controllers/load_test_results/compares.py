from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.schema.load_test_results.compares import LoadTestResultCompare, LoadTestResultScenarioCompare, \
    GetLoadTestResultScenarioCompareResponse, GetLoadTestResultScenarioCompareQuery
from services.postgres.models.load_test_results import LoadTestResultsModel
from services.postgres.models.scenario_settings import ScenarioSettingsModel


async def get_load_test_result_compare(
        session: AsyncSession,
        scenario: str | None,
        result: LoadTestResultsModel,
        previous_result: LoadTestResultsModel | None
) -> LoadTestResultCompare:
    average_total_requests_per_second = await (
        LoadTestResultsModel.get_average_total_requests_per_second_cached(
            session, service=result.service, scenario=scenario
        )
    )

    previous_id: int | None = None
    previous_total_requests_per_second: float = 0.0
    if previous_result:
        previous_id = previous_result.id
        previous_total_requests_per_second = previous_result.total_requests_per_second

    return LoadTestResultCompare(
        previous_id=previous_id,
        current_total_requests_per_second=result.total_requests_per_second,
        average_total_requests_per_second=average_total_requests_per_second,
        previous_total_requests_per_second=previous_total_requests_per_second
    )


async def get_load_test_result_scenario_compare(
        query: GetLoadTestResultScenarioCompareQuery,
        session: AsyncSession,
) -> GetLoadTestResultScenarioCompareResponse:
    result = await LoadTestResultsModel.get(
        session, clause_filter=(LoadTestResultsModel.id == query.load_test_result_id,)
    )
    settings = await ScenarioSettingsModel.get(
        session, clause_filter=(ScenarioSettingsModel.scenario == result.scenario,)
    )

    return GetLoadTestResultScenarioCompareResponse(
        compare=LoadTestResultScenarioCompare(
            current_requests_per_second=result.total_requests_per_second,
            scenario_requests_per_second=settings.requests_per_second,
        )
    )
