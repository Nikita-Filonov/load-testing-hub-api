import asyncio
from typing import Sequence

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.load_test_results.compares import get_load_test_result_compare
from apps.results.schema.load_test_results.compares import LoadTestResultCompare
from apps.results.schema.load_test_results.results import GetLoadTestResultsQuery, \
    GetLoadTestResultsResponse, LoadTestResult
from services.postgres.models.load_test_results import LoadTestResultsModel


async def get_load_test_results_compares(
        session: AsyncSession,
        results: Sequence[LoadTestResultsModel],
        scenario: str | None,
) -> tuple[LoadTestResultCompare]:
    return await asyncio.gather(*[
        get_load_test_result_compare(
            session,
            result=result,
            scenario=scenario,
            previous_result=results[index + 1] if (index + 1) < len(results) else None
        )
        for index, result in enumerate(results)
    ])


def get_load_test_result_with_compare(
        result: LoadTestResultsModel,
        compare: LoadTestResultCompare
) -> LoadTestResult:
    load_test_result = LoadTestResult.model_validate(result)
    load_test_result.compare = compare

    return load_test_result


async def get_load_test_results_with_filters(
        query: GetLoadTestResultsQuery,
        session: AsyncSession
) -> (list[LoadTestResultsModel], int):
    filters = (LoadTestResultsModel.service == query.service,)
    if query.scenario:
        filters += (LoadTestResultsModel.scenario == query.scenario,)

    if query.started_at:
        filters += (LoadTestResultsModel.started_at > query.started_at,)

    if query.finished_at:
        filters += (LoadTestResultsModel.finished_at < query.finished_at,)

    if query.trigger_ci_project_version:
        filters += (
            func.lower(LoadTestResultsModel.trigger_ci_project_version).contains(
                query.trigger_ci_project_version.lower()
            ),
        )

    results = await LoadTestResultsModel.filter(
        session,
        limit=query.limit + 1,
        offset=query.offset,
        order_by=(LoadTestResultsModel.created_at.desc(),),
        clause_filter=filters
    )
    total_results = await LoadTestResultsModel.count(
        session,
        column=LoadTestResultsModel.id,
        clause_filter=filters
    )

    return results, total_results


async def get_load_test_results(
        query: GetLoadTestResultsQuery,
        session: AsyncSession
) -> GetLoadTestResultsResponse:
    results, total_results = await get_load_test_results_with_filters(query, session)
    compares = await get_load_test_results_compares(session, results, query.scenario)

    if len(results) == query.limit + 1:
        results = results[:-1]

    return GetLoadTestResultsResponse(
        items=[
            get_load_test_result_with_compare(result, compares[index])
            for index, result in enumerate(results)
        ],
        total=total_results,
        limit=query.limit,
        offset=query.offset
    )
