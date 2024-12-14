from fastapi import APIRouter

from apps.compares.api.compare_settings import compare_settings_router
from apps.compares.api.compares import compares_router

compares_app_router = APIRouter()
compares_app_router.include_router(compares_router)
compares_app_router.include_router(compare_settings_router)
