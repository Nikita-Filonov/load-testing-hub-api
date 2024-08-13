from fastapi import APIRouter

from apps.services.api.scenario_settings import scenario_settings_router
from apps.services.api.scenarios import scenarios_router
from apps.services.api.services import services_router

services_app_router = APIRouter()
services_app_router.include_router(services_router)
services_app_router.include_router(scenarios_router)
services_app_router.include_router(scenario_settings_router)
