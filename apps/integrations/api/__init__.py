from fastapi import APIRouter

from apps.integrations.api.grafana import grafana_router
from apps.integrations.api.kibana import kibana_router

integrations_app_router = APIRouter()
integrations_app_router.include_router(kibana_router)
integrations_app_router.include_router(grafana_router)
