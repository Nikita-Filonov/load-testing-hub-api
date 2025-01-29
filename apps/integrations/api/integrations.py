from typing import Annotated

from fastapi import APIRouter, Depends

from apps.integrations.controllers.integrations.builders import build_integration_url
from apps.integrations.controllers.integrations.controllers import get_integration, get_integrations, \
    create_integration, update_integration, delete_integration, get_short_integrations
from apps.integrations.schema.integrations.builders import BuildIntegrationURLRequest, BuildIntegrationURLResponse
from apps.integrations.schema.integrations.controllers import GetIntegrationResponse, GetIntegrationsQuery, \
    GetIntegrationsResponse, CreateIntegrationRequest, UpdateIntegrationRequest, GetShortIntegrationsResponse
from config import Settings, get_settings
from services.postgres.repositories.integrations import IntegrationsRepository, get_integrations_repository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository, get_load_test_results_repository
from utils.routes import APIRoutes

integrations_router = APIRouter(
    prefix=APIRoutes.INTEGRATIONS,
    tags=[APIRoutes.INTEGRATIONS.as_tag()]
)


@integrations_router.get('', response_model=GetIntegrationsResponse)
async def get_integrations_view(
        query: Annotated[GetIntegrationsQuery, Depends(GetIntegrationsQuery.as_query)],
        integrations_repository: Annotated[IntegrationsRepository, Depends(get_integrations_repository)],
):
    return await get_integrations(query, integrations_repository)


@integrations_router.get('/short', response_model=GetShortIntegrationsResponse)
async def get_short_integrations_view(
        query: Annotated[GetIntegrationsQuery, Depends(GetIntegrationsQuery.as_query)],
        integrations_repository: Annotated[IntegrationsRepository, Depends(get_integrations_repository)],
):
    return await get_short_integrations(query, integrations_repository)


@integrations_router.get('/{integration_id}', response_model=GetIntegrationResponse)
async def get_integration_view(
        integration_id: int,
        integrations_repository: Annotated[IntegrationsRepository, Depends(get_integrations_repository)],
):
    return await get_integration(integration_id, integrations_repository)


@integrations_router.post('', response_model=GetIntegrationResponse)
async def create_integration_view(
        request: CreateIntegrationRequest,
        integrations_repository: Annotated[IntegrationsRepository, Depends(get_integrations_repository)],
):
    return await create_integration(request, integrations_repository)


@integrations_router.patch('/{integration_id}', response_model=GetIntegrationResponse)
async def update_integration_view(
        integration_id: int,
        request: UpdateIntegrationRequest,
        integrations_repository: Annotated[IntegrationsRepository, Depends(get_integrations_repository)],
):
    return await update_integration(integration_id, request, integrations_repository)


@integrations_router.delete('/{integration_id}')
async def delete_integration_view(
        integration_id: int,
        integrations_repository: Annotated[IntegrationsRepository, Depends(get_integrations_repository)],
):
    return await delete_integration(integration_id, integrations_repository)


@integrations_router.post('/build-integration-url', response_model=BuildIntegrationURLResponse)
async def build_integration_url_view(
        request: BuildIntegrationURLRequest,
        settings: Annotated[Settings, Depends(get_settings)],
        integrations_repository: Annotated[IntegrationsRepository, Depends(get_integrations_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],

):
    return await build_integration_url(
        request=request,
        settings=settings,
        integrations_repository=integrations_repository,
        load_test_results_repository=load_test_results_repository,
    )
