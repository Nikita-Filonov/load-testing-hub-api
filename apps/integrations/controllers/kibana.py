from sqlalchemy.ext.asyncio import AsyncSession

from apps.integrations.schema.integrations import GetIntegrationURLQuery
from apps.integrations.schema.kibana import GetKibanaDiscoverURLResponse
from config import Settings
from services.postgres.models import ServicesModel
from utils.integrations.kibana import KibanaDiscoverURLBuilder


async def get_kibana_discover_url(
        query: GetIntegrationURLQuery,
        setting: Settings,
        session: AsyncSession
) -> GetKibanaDiscoverURLResponse:
    service = await ServicesModel.get(
        session, clause_filter=(ServicesModel.name == query.service,)
    )

    builder = KibanaDiscoverURLBuilder(
        to_time=str(query.finished_at.strftime('%Y-%m-%dT%H:%M:%S') + '.000Z'),
        from_time=str(query.started_at.strftime('%Y-%m-%dT%H:%M:%S') + '.000Z'),
        namespace=service.namespace,
    )

    return GetKibanaDiscoverURLResponse(
        discover_url=builder.build_url(setting.kibana_url)
    )
