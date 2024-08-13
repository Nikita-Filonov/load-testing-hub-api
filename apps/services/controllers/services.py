from sqlalchemy.ext.asyncio import AsyncSession

from apps.services.schema.services import GetServicesResponse, Service, GetServicesQuery, GetServiceResponse
from services.postgres.models import ServicesModel


async def get_service(name: str, session: AsyncSession) -> GetServiceResponse:
    service = await ServicesModel.get(session, name=name)

    return GetServiceResponse(
        service=Service.model_validate(service)
    )


async def get_services(query: GetServicesQuery, session: AsyncSession) -> GetServicesResponse:
    filters = (ServicesModel.is_internal.is_(False),)
    if query.with_internal:
        filters = ()

    services = await ServicesModel.filter(session, clause_filter=filters)

    return GetServicesResponse(
        services=[Service.model_validate(service) for service in services]
    )
