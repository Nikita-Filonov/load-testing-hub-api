from sqlalchemy.ext.asyncio import AsyncSession

from apps.services.schema.scenarios import CreateScenarioRequest, GetScenariosQuery, GetScenariosResponse, Scenario, \
    GetScenarioDetailsResponse, ScenarioDetails, GetScenarioResponse
from services.postgres.models import ScenariosModel, ScenarioSettingsModel


async def get_scenario(name: str, session: AsyncSession) -> GetScenarioResponse:
    scenario = await ScenariosModel.get(session, name=name)

    return GetScenarioResponse(scenario=Scenario.model_validate(scenario))


async def get_scenarios(query: GetScenariosQuery, session: AsyncSession) -> GetScenariosResponse:
    scenarios = await ScenariosModel.filter(
        session,
        clause_filter=(ScenariosModel.service == query.service,)
    )

    return GetScenariosResponse(
        scenarios=[Scenario.model_validate(scenario) for scenario in scenarios]
    )


async def create_scenario(request: CreateScenarioRequest, session: AsyncSession):
    scenario = await ScenariosModel.get(session, name=request.scenario.name)
    settings = await ScenarioSettingsModel.get(session, scenario=request.scenario.name)

    if scenario:
        await ScenariosModel.update(
            session,
            clause_filter=(ScenariosModel.name == request.scenario.name,),
            **request.scenario.model_dump(mode='json')
        )
    else:
        await ScenariosModel.create(session, **request.scenario.model_dump(mode='json'))

    if not settings:
        await ScenarioSettingsModel.create(session, scenario=request.scenario.name)


async def get_scenario_details(name: str, session: AsyncSession) -> GetScenarioDetailsResponse:
    scenario = await ScenariosModel.get(session, name=name)

    return GetScenarioDetailsResponse(
        details=ScenarioDetails.model_validate(scenario)
    )
