from typing import Annotated

from fastapi import APIRouter, Depends

from apps.services.controllers.services import get_services, get_service, create_service, update_service, \
    get_service_details, delete_service
from apps.services.schema.services import GetServicesResponse, GetServiceResponse, \
    CreateServiceRequest, GetServiceDetailsResponse, UpdateServiceRequest, GetServicesQuery
from services.postgres.repositories.load_test_results import LoadTestResultsRepository, get_load_test_results_repository
from services.postgres.repositories.method_results import MethodResultsRepository, get_method_results_repository
from services.postgres.repositories.scenarios import ScenariosRepository, get_scenarios_repository
from services.postgres.repositories.services import ServicesRepository, get_services_repository
from utils.routes import APIRoutes

services_router = APIRouter(
    prefix=APIRoutes.SERVICES,
    tags=[APIRoutes.SERVICES.as_tag()]
)


@services_router.get('/{service_id}', response_model=GetServiceResponse)
async def get_service_view(
        service_id: int,
        services_repository: Annotated[ServicesRepository, Depends(get_services_repository)]
):
    return await get_service(service_id, services_repository)


@services_router.get('/details/{service_id}', response_model=GetServiceDetailsResponse)
async def get_service_details_view(
        service_id: int,
        services_repository: Annotated[ServicesRepository, Depends(get_services_repository)]
):
    return await get_service_details(service_id, services_repository)


@services_router.get('', response_model=GetServicesResponse)
async def get_services_view(
        query: Annotated[GetServicesQuery, Depends(GetServicesQuery.as_query)],
        services_repository: Annotated[ServicesRepository, Depends(get_services_repository)]
):
    return await get_services(query, services_repository)


@services_router.post('', response_model=GetServiceDetailsResponse)
async def create_service_view(
        request: CreateServiceRequest,
        services_repository: Annotated[ServicesRepository, Depends(get_services_repository)]
):
    return await create_service(request, services_repository)


@services_router.patch('/{service_id}', response_model=GetServiceDetailsResponse)
async def update_service_view(
        service_id: int,
        request: UpdateServiceRequest,
        services_repository: Annotated[ServicesRepository, Depends(get_services_repository)]
):
    return await update_service(service_id, request, services_repository)


@services_router.delete('/{service_id}')
async def delete_service_view(
        service_id: int,
        services_repository: Annotated[ServicesRepository, Depends(get_services_repository)],
        scenarios_repository: Annotated[ScenariosRepository, Depends(get_scenarios_repository)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
):
    return await delete_service(
        service_id,
        services_repository=services_repository,
        scenarios_repository=scenarios_repository,
        method_results_repository=method_results_repository,
        load_test_results_repository=load_test_results_repository
    )
