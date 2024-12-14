from typing import Annotated

from fastapi import APIRouter, Depends

from apps.analytics.controllers.average_analytics import get_average_analytics
from apps.analytics.schema.average_analytics import GetAverageAnalyticsResponse
from apps.analytics.schema.results_analytics import GetResultsAnalyticsQuery
from services.postgres.repositories.load_test_results import LoadTestResultsRepository, get_load_test_results_repository
from utils.routes import APIRoutes

average_analytics_router = APIRouter(
    prefix=APIRoutes.AVERAGE_ANALYTICS,
    tags=[APIRoutes.AVERAGE_ANALYTICS.as_tag()]
)


@average_analytics_router.get('', response_model=GetAverageAnalyticsResponse)
async def get_average_analytics_view(
        query: Annotated[GetResultsAnalyticsQuery, Depends(GetResultsAnalyticsQuery.as_query)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)]
):
    return await get_average_analytics(query, load_test_results_repository)
