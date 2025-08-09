from pydantic import HttpUrl

from apps.integrations.constants.integrations.system import IntegrationSystemType
from apps.integrations.schema.integrations.builders import BuildIntegrationURLRequest, BuildIntegrationURLResponse
from config import Settings
from services.postgres.models import IntegrationsModel, LoadTestResultsModel
from services.postgres.repositories.integrations import IntegrationsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository


def get_kibana_integration_url(
        settings: Settings,
        integration: IntegrationsModel,
        load_test_result: LoadTestResultsModel,
) -> str:
    return integration.get_ready_url(
        host=settings.kibana_url.host,
        to_time=str(load_test_result.finished_at.strftime('%Y-%m-%dT%H:%M:%S') + '.000Z'),
        from_time=str(load_test_result.started_at.strftime('%Y-%m-%dT%H:%M:%S') + '.000Z'),
    )


def get_grafana_integration_url(
        settings: Settings,
        integration: IntegrationsModel,
        load_test_result: LoadTestResultsModel,
) -> str:
    return integration.get_ready_url(
        host=settings.grafana_url.host,
        to_time=str(int(load_test_result.finished_at.timestamp()) * 1000),
        from_time=str(int(load_test_result.started_at.timestamp()) * 1000),
    )


def get_kubernetes_integration_url(settings: Settings, integration: IntegrationsModel) -> str:
    return integration.get_ready_url(host=settings.kubernetes_url.host)


async def build_integration_url(
        request: BuildIntegrationURLRequest,
        settings: Settings,
        integrations_repository: IntegrationsRepository,
        load_test_results_repository: LoadTestResultsRepository,
) -> BuildIntegrationURLResponse:
    integration = await integrations_repository.get_by_id(request.integration_id)
    load_test_result = await load_test_results_repository.get_by_id(request.load_test_result_id)

    match request.system_type:
        case IntegrationSystemType.KIBANA:
            integration_url = get_kibana_integration_url(settings, integration, load_test_result)
        case IntegrationSystemType.GRAFANA:
            integration_url = get_grafana_integration_url(settings, integration, load_test_result)
        case IntegrationSystemType.KUBERNETES:
            integration_url = get_kubernetes_integration_url(settings, integration)
        case _:
            raise ValueError(f"Unsupported integration system type: {integration.system_type}")

    return BuildIntegrationURLResponse(integration_url=HttpUrl(integration_url))
