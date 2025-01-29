from fastapi import APIRouter

from apps.methods.api.methods import methods_router

methods_app_router = APIRouter()
methods_app_router.include_router(methods_router)
