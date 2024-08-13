from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.schema.methods.compares import GetMethodScenarioCompareQuery, GetMethodScenarioCompareResponse, \
    MethodScenarioCompare
from services.postgres.models import MethodResultsModel, ScenarioSettingsModel


async def get_method_scenario_compare(
        query: GetMethodScenarioCompareQuery,
        session: AsyncSession
) -> GetMethodScenarioCompareResponse:
    result = await MethodResultsModel.get(
        session,
        clause_filter=(MethodResultsModel.method == query.method,)
    )
    settings = await ScenarioSettingsModel.get(
        session, clause_filter=(ScenarioSettingsModel.scenario == query.scenario,)
    )
    method_settings = settings.get_method_settings(query.method)

    average_requests_per_second = await result.get_average_requests_per_second(
        session, query.scenario, query.end_datetime, query.start_datetime
    )

    return GetMethodScenarioCompareResponse(
        compare=MethodScenarioCompare(
            average_requests_per_second=average_requests_per_second,
            scenario_requests_per_second=method_settings['requests_per_second']
        )
    )
