from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles

from apps.analytics.api import analytics_app_router
from apps.integrations.api import integrations_app_router
from apps.results.api import results_app_router
from apps.services.api import services_app_router
from config import Settings, get_settings

app = FastAPI(title="Load testing hub API", docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(results_app_router, prefix="/api/v1")
app.include_router(services_app_router, prefix="/api/v1")
app.include_router(analytics_app_router, prefix="/api/v1")
app.include_router(integrations_app_router, prefix="/api/v1")


@app.get("/docs", include_in_schema=False)
def docs_view(settings: Annotated[Settings, Depends(get_settings)]):
    return get_swagger_ui_html(
        title=settings.app_name,
        openapi_url="/openapi.json",
        swagger_favicon_url=settings.app_logo_path
    )


@app.get("/redoc", include_in_schema=False)
def redoc_view(settings: Annotated[Settings, Depends(get_settings)]):
    return get_redoc_html(
        title=settings.app_name,
        openapi_url="/openapi.json",
        redoc_favicon_url=settings.app_logo_path
    )
