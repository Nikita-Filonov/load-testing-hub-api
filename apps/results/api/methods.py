from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.methods.compares import get_method_scenario_compare
from apps.results.controllers.methods.controllers import get_methods, get_short_methods, get_method_details
from apps.results.schema.methods.compares import GetMethodScenarioCompareResponse, GetMethodScenarioCompareQuery
from apps.results.schema.methods.schema import GetMethodsQuery, GetMethodsResponse, GetShortMethodsResponse, \
    GetShortMethodsQuery, GetMethodDetailsQuery, GetMethodDetailsResponse
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

methods_router = APIRouter(
    prefix=APIRoutes.METHODS,
    tags=[APIRoutes.METHODS.as_tag()]
)


@methods_router.get('', response_model=GetMethodsResponse)
async def get_methods_view(
        query: Annotated[GetMethodsQuery, Depends(GetMethodsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_methods(query, session)


@methods_router.get('/short', response_model=GetShortMethodsResponse)
async def get_short_methods_view(
        query: Annotated[GetShortMethodsQuery, Depends(GetShortMethodsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_short_methods(query, session)


@methods_router.get('/details', response_model=GetMethodDetailsResponse)
async def get_method_details_view(
        query: Annotated[GetMethodDetailsQuery, Depends(GetMethodDetailsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_method_details(query, session)


@methods_router.get(
    '/scenario-compare',
    response_model=GetMethodScenarioCompareResponse
)
async def get_method_scenario_compare_view(
        query: Annotated[
            GetMethodScenarioCompareQuery, Depends(GetMethodScenarioCompareQuery.as_query)
        ],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_method_scenario_compare(query, session)
