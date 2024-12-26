from fastapi import APIRouter

from apps.integrations.api.integrations import integrations_router

integrations_app_router = APIRouter()
integrations_app_router.include_router(integrations_router)
