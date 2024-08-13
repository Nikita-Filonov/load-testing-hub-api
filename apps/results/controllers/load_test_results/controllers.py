from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.load_test_results.details import get_load_test_result_details
from apps.results.schema.load_test_results.results import GetLoadTestResultDetailsResponse, \
    CreateLoadTestResultRequest, GetLoadTestResultDetailsQuery
from services.postgres.models import LoadTestResultsModel


async def create_load_test_result(
        request: CreateLoadTestResultRequest,
        session: AsyncSession
) -> GetLoadTestResultDetailsResponse:
    result = await LoadTestResultsModel.create(session, **request.model_dump())

    query = GetLoadTestResultDetailsQuery(
        scenario=result.scenario,
        load_test_result_id=result.id
    )
    return await get_load_test_result_details(query, session)
