from apps.integrations.schema.integrations import GetIntegrationURLQuery
from apps.integrations.schema.kibana import GetKibanaDiscoverURLResponse
from config import Settings
from services.postgres.repositories.services import ServicesRepository
from utils.integrations.kibana import KibanaDiscoverURLBuilder


async def get_kibana_discover_url(
        query: GetIntegrationURLQuery,
        setting: Settings,
        services_repository: ServicesRepository
) -> GetKibanaDiscoverURLResponse:
    service = await services_repository.get_by_id(query.service_id)

    builder = KibanaDiscoverURLBuilder(
        to_time=str(query.finished_at.strftime('%Y-%m-%dT%H:%M:%S') + '.000Z'),
        from_time=str(query.started_at.strftime('%Y-%m-%dT%H:%M:%S') + '.000Z'),
        namespace=service.namespace,
    )

    return GetKibanaDiscoverURLResponse(
        discover_url=builder.build_url(setting.kibana_url)
    )
