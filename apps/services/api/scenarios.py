from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.services.controllers.scenarios import get_scenarios, create_scenario, get_scenario_details, get_scenario
from apps.services.schema.scenarios import GetScenariosResponse, GetScenariosQuery, CreateScenarioRequest, \
    GetScenarioDetailsResponse, GetScenarioResponse
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

scenarios_router = APIRouter(
    prefix=APIRoutes.SCENARIOS,
    tags=[APIRoutes.SCENARIOS.as_tag()]
)


@scenarios_router.get('/{name}', response_model=GetScenarioResponse)
async def get_scenario_view(
        name: str,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_scenario(name, session)


@scenarios_router.get('', response_model=GetScenariosResponse)
async def get_scenarios_view(
        query: Annotated[GetScenariosQuery, Depends(GetScenariosQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_scenarios(query, session)


@scenarios_router.get('/details/{name}', response_model=GetScenarioDetailsResponse)
async def get_scenario_details_view(
        name: str,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_scenario_details(name, session)


@scenarios_router.post('')
async def create_scenario_view(
        request: CreateScenarioRequest,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await create_scenario(request, session)
