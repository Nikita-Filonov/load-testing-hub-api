from apps.integrations.schema.grafana import GetGrafanaDashboardURLResponse
from apps.integrations.schema.integrations import GetIntegrationURLQuery
from config import Settings
from services.postgres.repositories.services import ServicesRepository
from utils.integrations.grafana import GrafanaDashboardURLBuilder


async def get_grafana_dashboard_url(
        query: GetIntegrationURLQuery,
        setting: Settings,
        services_repository: ServicesRepository
) -> GetGrafanaDashboardURLResponse:
    service = await services_repository.get_by_id(query.service_id)

    builder = GrafanaDashboardURLBuilder(
        to_time=str(int(query.finished_at.timestamp()) * 1000),
        from_time=str(int(query.started_at.timestamp()) * 1000),
        var_cluster=service.cluster,
        var_namespace=service.namespace,
    )

    return GetGrafanaDashboardURLResponse(
        dashboard_url=builder.build_url(setting.grafana_url)
    )
