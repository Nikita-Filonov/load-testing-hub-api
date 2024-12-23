from apps.services.schema.services import GetServicesResponse, Service, GetServiceResponse, \
    CreateServiceRequest, GetServiceDetailsResponse, ServiceDetails, UpdateServiceRequest, GetServicesQuery
from services.postgres.repositories.load_test_results import LoadTestResultsRepository
from services.postgres.repositories.method_results import MethodResultsRepository
from services.postgres.repositories.scenarios import ScenariosRepository
from services.postgres.repositories.services import ServicesRepository


async def get_service(service_id: int, services_repository: ServicesRepository) -> GetServiceResponse:
    service = await services_repository.get_by_id(service_id)

    return GetServiceResponse(service=Service.model_validate(service))


async def get_service_details(
        service_id: int,
        services_repository: ServicesRepository
) -> GetServiceDetailsResponse:
    service = await services_repository.get_by_id(service_id)

    return GetServiceDetailsResponse(details=ServiceDetails.model_validate(service))


async def create_service(
        request: CreateServiceRequest,
        services_repository: ServicesRepository
) -> GetServiceDetailsResponse:
    service = await services_repository.create(request.model_dump(mode='json'))

    return GetServiceDetailsResponse(details=ServiceDetails.model_validate(service))


async def update_service(
        service_id: int,
        request: UpdateServiceRequest,
        services_repository: ServicesRepository
) -> GetServiceDetailsResponse:
    service = await services_repository.update(
        service_id, request.model_dump(mode='json', exclude_unset=True)
    )

    return GetServiceDetailsResponse(details=ServiceDetails.model_validate(service))


async def delete_service(
        service_id: int,
        services_repository: ServicesRepository,
        scenarios_repository: ScenariosRepository,
        method_results_repository: MethodResultsRepository,
        load_test_results_repository: LoadTestResultsRepository
):
    await services_repository.delete(service_id)
    await scenarios_repository.delete(service_id=service_id)
    await method_results_repository.delete(service_id=service_id)
    await load_test_results_repository.delete(service_id=service_id)


async def get_services(
        query: GetServicesQuery,
        services_repository: ServicesRepository
) -> GetServicesResponse:
    services = await services_repository.filter(types=query.types)

    return GetServicesResponse(
        services=[Service.model_validate(service) for service in services]
    )
