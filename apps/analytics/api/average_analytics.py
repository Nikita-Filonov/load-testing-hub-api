from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.analytics.controllers.average_analytics import get_average_analytics, get_average_analytics_scenario_compare
from apps.analytics.schema.average_analytics import GetAverageAnalyticsResponse, \
    GetAverageAnalyticsScenarioCompareQuery, \
    GetAverageAnalyticsScenarioCompareResponse
from apps.analytics.schema.results_analytics import GetResultsAnalyticsQuery
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

average_analytics_router = APIRouter(
    prefix=APIRoutes.AVERAGE_ANALYTICS,
    tags=[APIRoutes.AVERAGE_ANALYTICS.as_tag()]
)


@average_analytics_router.get('', response_model=GetAverageAnalyticsResponse)
async def get_average_analytics_view(
        query: Annotated[GetResultsAnalyticsQuery, Depends(GetResultsAnalyticsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_average_analytics(query, session)


@average_analytics_router.get(
    '/scenario-compare',
    response_model=GetAverageAnalyticsScenarioCompareResponse
)
async def get_average_analytics_scenario_compare_view(
        query: Annotated[
            GetAverageAnalyticsScenarioCompareQuery,
            Depends(GetAverageAnalyticsScenarioCompareQuery.as_query)
        ],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_average_analytics_scenario_compare(query, session)
