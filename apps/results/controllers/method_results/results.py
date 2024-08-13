from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.schema.method_results.results import GetMethodResultsQuery, GetMethodResultsResponse, MethodResult, \
    CreateMethodResultsRequest
from services.postgres.models import MethodResultsModel


async def get_method_results(
        query: GetMethodResultsQuery,
        session: AsyncSession
) -> GetMethodResultsResponse:
    results = await MethodResultsModel.filter(
        session,
        clause_filter=(MethodResultsModel.load_test_results_id == query.load_test_result_id,)
    )

    return GetMethodResultsResponse(
        results=[MethodResult.model_validate(result) for result in results]
    )


async def create_method_results(request: CreateMethodResultsRequest, session: AsyncSession):
    for result in request.results:
        await MethodResultsModel.create(
            session, **result.model_dump(), load_test_results_id=request.load_test_results_id
        )
