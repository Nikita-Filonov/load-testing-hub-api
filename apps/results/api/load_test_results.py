from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.load_test_results.compares import get_load_test_result_scenario_compare
from apps.results.controllers.load_test_results.controllers import create_load_test_result
from apps.results.controllers.load_test_results.details import get_load_test_result_details
from apps.results.controllers.load_test_results.results import get_load_test_results
from apps.results.schema.load_test_results.compares import GetLoadTestResultScenarioCompareQuery, \
    GetLoadTestResultScenarioCompareResponse
from apps.results.schema.load_test_results.results import GetLoadTestResultsQuery, GetLoadTestResultsResponse, \
    GetLoadTestResultDetailsResponse, CreateLoadTestResultRequest, GetLoadTestResultDetailsQuery
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

load_test_results_router = APIRouter(
    prefix=APIRoutes.LOAD_TEST_RESULTS,
    tags=[APIRoutes.LOAD_TEST_RESULTS.as_tag()]
)


@load_test_results_router.get('', response_model=GetLoadTestResultsResponse)
async def get_load_test_results_vew(
        query: Annotated[GetLoadTestResultsQuery, Depends(GetLoadTestResultsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_load_test_results(query, session)


@load_test_results_router.get(
    '/details',
    response_model=GetLoadTestResultDetailsResponse
)
async def get_load_test_result_details_view(
        query: Annotated[
            GetLoadTestResultDetailsQuery,
            Depends(GetLoadTestResultDetailsQuery.as_query)
        ],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_load_test_result_details(query, session)


@load_test_results_router.get(
    '/scenario-compare',
    response_model=GetLoadTestResultScenarioCompareResponse
)
async def get_load_test_result_scenario_compare_view(
        query: Annotated[
            GetLoadTestResultScenarioCompareQuery,
            Depends(GetLoadTestResultScenarioCompareQuery.as_query)
        ],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_load_test_result_scenario_compare(query, session)


@load_test_results_router.post('', response_model=GetLoadTestResultDetailsResponse)
async def crate_load_test_result_view(
        request: CreateLoadTestResultRequest,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await create_load_test_result(request, session)
