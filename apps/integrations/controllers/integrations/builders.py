from apps.integrations.schema.integrations.builders import BuildIntegrationURLRequest, BuildKibanaDiscoverURLResponse, \
    BuildGrafanaDashboardURLResponse
from config import Settings

from services.postgres.repositories.integrations import IntegrationsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository
from utils.integrations.grafana import GrafanaDashboardURLBuilder
from utils.integrations.kibana import KibanaDiscoverURLBuilder


async def build_kibana_discover_url(
        request: BuildIntegrationURLRequest,
        setting: Settings,
        integrations_repository: IntegrationsRepository,
        load_test_results_repository: LoadTestResultsRepository,
) -> BuildKibanaDiscoverURLResponse:
    result = await load_test_results_repository.get_by_id(request.load_test_result_id)
    integration = await integrations_repository.get_by_id(request.integration_id)

    builder = KibanaDiscoverURLBuilder(
        to_time=str(result.finished_at.strftime('%Y-%m-%dT%H:%M:%S') + '.000Z'),
        from_time=str(result.started_at.strftime('%Y-%m-%dT%H:%M:%S') + '.000Z'),
        namespace=integration.namespace,
    )

    return BuildKibanaDiscoverURLResponse(
        discover_url=builder.build_url(setting.kibana_url)
    )


async def build_grafana_dashboard_url(
        request: BuildIntegrationURLRequest,
        setting: Settings,
        integrations_repository: IntegrationsRepository,
        load_test_results_repository: LoadTestResultsRepository,
) -> BuildGrafanaDashboardURLResponse:
    result = await load_test_results_repository.get_by_id(request.load_test_result_id)
    integration = await integrations_repository.get_by_id(request.integration_id)

    builder = GrafanaDashboardURLBuilder(
        to_time=str(int(result.finished_at.timestamp()) * 1000),
        from_time=str(int(result.started_at.timestamp()) * 1000),
        var_cluster=integration.cluster,
        var_namespace=integration.namespace,
    )

    return BuildGrafanaDashboardURLResponse(
        dashboard_url=builder.build_url(setting.grafana_url)
    )
