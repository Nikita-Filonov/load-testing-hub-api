from typing import Annotated

from fastapi import APIRouter, Depends

from apps.integrations.controllers.kibana import get_kibana_discover_url
from apps.integrations.schema.integrations import GetIntegrationURLQuery
from apps.integrations.schema.kibana import GetKibanaDiscoverURLResponse
from config import get_settings, Settings
from services.postgres.repositories.services import ServicesRepository, get_services_repository
from utils.routes import APIRoutes

kibana_router = APIRouter(
    prefix=APIRoutes.INTEGRATIONS_KIBANA,
    tags=[APIRoutes.INTEGRATIONS_KIBANA.as_tag()]
)


@kibana_router.get('/discover-url', response_model=GetKibanaDiscoverURLResponse)
async def get_kibana_discover_url_view(
        query: Annotated[GetIntegrationURLQuery, Depends(GetIntegrationURLQuery.as_query)],
        settings: Annotated[Settings, Depends(get_settings)],
        services_repository: Annotated[ServicesRepository, Depends(get_services_repository)]
):
    return await get_kibana_discover_url(query, settings, services_repository)
