from typing import Annotated

from fastapi import APIRouter, Depends

from apps.integrations.controllers.grafana import get_grafana_dashboard_url
from apps.integrations.schema.grafana import GetGrafanaDashboardURLResponse
from apps.integrations.schema.integrations import GetIntegrationURLQuery
from config import get_settings, Settings
from services.postgres.repositories.services import ServicesRepository, get_services_repository
from utils.routes import APIRoutes

grafana_router = APIRouter(
    prefix=APIRoutes.INTEGRATIONS_GRAFANA,
    tags=[APIRoutes.INTEGRATIONS_GRAFANA.as_tag()]
)


@grafana_router.get('/dashboard-url', response_model=GetGrafanaDashboardURLResponse)
async def get_grafana_dashboard_url_view(
        query: Annotated[GetIntegrationURLQuery, Depends(GetIntegrationURLQuery.as_query)],
        settings: Annotated[Settings, Depends(get_settings)],
        services_repository: Annotated[ServicesRepository, Depends(get_services_repository)]
):
    return await get_grafana_dashboard_url(query, settings, services_repository)
