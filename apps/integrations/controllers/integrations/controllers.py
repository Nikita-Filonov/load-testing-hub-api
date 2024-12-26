from apps.integrations.schema.integrations.controllers import GetIntegrationResponse, Integration, GetIntegrationsQuery, \
    GetIntegrationsResponse, CreateIntegrationRequest, UpdateIntegrationRequest
from services.postgres.repositories.integrations import IntegrationsRepository


async def get_integration(
        integration_id: int,
        integrations_repository: IntegrationsRepository
) -> GetIntegrationResponse:
    integration = await integrations_repository.get_by_id(integration_id)

    return GetIntegrationResponse(integration=Integration.model_validate(integration))


async def get_integrations(
        query: GetIntegrationsQuery,
        integrations_repository: IntegrationsRepository
) -> GetIntegrationsResponse:
    integrations = await integrations_repository.filter(service_id=query.service_id)

    return GetIntegrationsResponse(
        integrations=[Integration.model_validate(integration) for integration in integrations]
    )


async def create_integration(
        request: CreateIntegrationRequest,
        integrations_repository: IntegrationsRepository
) -> GetIntegrationResponse:
    integration = await integrations_repository.create(request.model_dump(mode='json'))

    return GetIntegrationResponse(integration=Integration.model_validate(integration))


async def update_integration(
        integration_id: int,
        request: UpdateIntegrationRequest,
        integrations_repository: IntegrationsRepository
):
    integration = await integrations_repository.update(
        integration_id, request.model_dump(exclude_unset=True)
    )

    return GetIntegrationResponse(integration=Integration.model_validate(integration))


async def delete_integration(integration_id: int, integrations_repository: IntegrationsRepository):
    await integrations_repository.delete(integration_id=integration_id)
