from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.method_results.compares import get_method_results_compares, \
    get_method_results_scenario_compares
from apps.results.controllers.method_results.results import get_method_results, create_method_results
from apps.results.schema.method_results.compares import GetMethodResultsComparesResponse, \
    GetMethodResultsScenarioComparesResponse, GetMethodResultsScenarioComparesQuery, GetMethodResultsComparesQuery
from apps.results.schema.method_results.results import GetMethodResultsQuery, GetMethodResultsResponse, \
    CreateMethodResultsRequest
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

method_results_router = APIRouter(
    prefix=APIRoutes.METHOD_RESULTS,
    tags=[APIRoutes.METHOD_RESULTS.as_tag()]
)


@method_results_router.get('', response_model=GetMethodResultsResponse)
async def get_method_results_view(
        query: Annotated[GetMethodResultsQuery, Depends(GetMethodResultsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_method_results(query, session)


@method_results_router.get('/compares', response_model=GetMethodResultsComparesResponse)
async def get_method_results_compares_view(
        query: Annotated[
            GetMethodResultsComparesQuery, Depends(GetMethodResultsComparesQuery.as_query)
        ],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_method_results_compares(query, session)


@method_results_router.get(
    '/scenario-compares',
    response_model=GetMethodResultsScenarioComparesResponse
)
async def get_method_results_scenario_compares_view(
        query: Annotated[
            GetMethodResultsScenarioComparesQuery,
            Depends(GetMethodResultsScenarioComparesQuery.as_query)
        ],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_method_results_scenario_compares(query, session)


@method_results_router.post('')
async def create_method_results_view(
        request: CreateMethodResultsRequest,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await create_method_results(request, session)
