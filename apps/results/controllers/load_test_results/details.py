from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.load_test_results.compares import get_load_test_result_compare
from apps.results.schema.load_test_results.results import LoadTestResultDetails, GetLoadTestResultDetailsResponse, \
    GetLoadTestResultDetailsQuery
from services.postgres.models.load_test_results import LoadTestResultsModel


async def get_previous_load_test_result(
        session: AsyncSession,
        load_test_result_id: int,
        service: str,
        scenario: str | None,
) -> LoadTestResultsModel | None:
    filters = (
        LoadTestResultsModel.id < load_test_result_id,
        LoadTestResultsModel.service == service
    )
    if scenario:
        filters += (LoadTestResultsModel.scenario == scenario,)

    previous_results = await LoadTestResultsModel.filter(
        session,
        limit=1,
        order_by=(LoadTestResultsModel.id.desc(),),
        clause_filter=filters
    )

    return previous_results[0] if len(previous_results) > 0 else None


async def get_load_test_result_details(
        query: GetLoadTestResultDetailsQuery,
        session: AsyncSession
) -> GetLoadTestResultDetailsResponse:
    result = await LoadTestResultsModel.get(
        session,
        clause_filter=(LoadTestResultsModel.id == query.load_test_result_id,)
    )
    previous_result = await get_previous_load_test_result(
        session, query.load_test_result_id, result.service, query.scenario
    )

    details = LoadTestResultDetails.model_validate(result)
    details.compare = await get_load_test_result_compare(
        session, query.scenario, result, previous_result
    )

    return GetLoadTestResultDetailsResponse(details=details)
