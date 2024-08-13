from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.services.controllers.services import get_services, get_service
from apps.services.schema.services import GetServicesResponse, GetServicesQuery, GetServiceResponse
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

services_router = APIRouter(
    prefix=APIRoutes.SERVICES,
    tags=[APIRoutes.SERVICES.as_tag()]
)


@services_router.get('/{name}', response_model=GetServiceResponse)
async def get_service_view(
        name: str,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_service(name, session)


@services_router.get('', response_model=GetServicesResponse)
async def get_services_view(
        query: Annotated[GetServicesQuery, Depends(GetServicesQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_services(query, session)
