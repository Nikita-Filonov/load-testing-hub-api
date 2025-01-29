from typing import TypeVar

from pydantic import BaseModel

from apps.compares.controllers.compares.compare_results_history.base import normalize_compare_results_history
from apps.compares.schema.compares.compare_results_history.base import GetCompareResultsHistoryResponse, \
    CompareResultsHistory, CompareResultHistory
from apps.compares.schema.compares.compare_results_history.compare_load_test_results_history import \
    GetCompareLoadTestResultsHistoryQuery
from services.postgres.repositories.load_test_results import LoadTestResultsRepository
from services.postgres.repositories.load_test_results_history import LoadTestResultsHistoryRepository
from utils.schema.metrics.number_of_requests import NumberOfRequestsSchema
from utils.schema.metrics.number_of_users import NumberOfUsersSchema
from utils.schema.metrics.requests_per_second import RequestsPerSecondSchema
from utils.schema.metrics.response_times import ResponseTimesSchema

T = TypeVar('T', bound=BaseModel)


async def get_compare_load_test_results_history(
        query: GetCompareLoadTestResultsHistoryQuery,
        result_type: type[CompareResultHistory[T]],
        load_test_results_repository: LoadTestResultsRepository,
        load_test_results_history_repository: LoadTestResultsHistoryRepository,
) -> GetCompareResultsHistoryResponse[T]:
    load_test_results = await load_test_results_repository.filter_by_ids_groped(
        query.compare_with_load_test_results
    )

    results_history = await load_test_results_history_repository.filter_by_load_test_result_id(
        query.load_test_result_id
    )
    compare_with_results_history = await load_test_results_history_repository.filter_by_load_test_result_ids_groped(
        query.compare_with_load_test_results
    )

    compares = [
        CompareResultsHistory[T](
            title='Current',
            results=[
                result_type(metrics=result.to_dict(), datetime=result.datetime)
                for result in results_history
            ]
        ),
        *[
            CompareResultsHistory[T](
                title=load_test_results[load_test_result_id].get_compare_title(),
                results=[
                    result_type(metrics=result.to_dict(), datetime=result.datetime)
                    for result in results_history
                ]
            )
            for load_test_result_id, results_history in compare_with_results_history.items()
        ]
    ]

    return GetCompareResultsHistoryResponse[T](compares=normalize_compare_results_history(compares))


async def get_compare_load_test_results_history_response_times(
        query: GetCompareLoadTestResultsHistoryQuery,
        load_test_results_repository: LoadTestResultsRepository,
        load_test_results_history_repository: LoadTestResultsHistoryRepository,
) -> GetCompareResultsHistoryResponse[ResponseTimesSchema]:
    return await get_compare_load_test_results_history(
        query=query,
        result_type=CompareResultHistory[ResponseTimesSchema],
        load_test_results_repository=load_test_results_repository,
        load_test_results_history_repository=load_test_results_history_repository
    )


async def get_compare_load_test_results_history_number_of_users(
        query: GetCompareLoadTestResultsHistoryQuery,
        load_test_results_repository: LoadTestResultsRepository,
        load_test_results_history_repository: LoadTestResultsHistoryRepository,
) -> GetCompareResultsHistoryResponse[NumberOfUsersSchema]:
    return await get_compare_load_test_results_history(
        query=query,
        result_type=CompareResultHistory[NumberOfUsersSchema],
        load_test_results_repository=load_test_results_repository,
        load_test_results_history_repository=load_test_results_history_repository
    )


async def get_compare_load_test_results_history_number_of_requests(
        query: GetCompareLoadTestResultsHistoryQuery,
        load_test_results_repository: LoadTestResultsRepository,
        load_test_results_history_repository: LoadTestResultsHistoryRepository,
) -> GetCompareResultsHistoryResponse[NumberOfRequestsSchema]:
    return await get_compare_load_test_results_history(
        query=query,
        result_type=CompareResultHistory[NumberOfRequestsSchema],
        load_test_results_repository=load_test_results_repository,
        load_test_results_history_repository=load_test_results_history_repository
    )


async def get_compare_load_test_results_history_requests_per_second(
        query: GetCompareLoadTestResultsHistoryQuery,
        load_test_results_repository: LoadTestResultsRepository,
        load_test_results_history_repository: LoadTestResultsHistoryRepository,
) -> GetCompareResultsHistoryResponse[RequestsPerSecondSchema]:
    return await get_compare_load_test_results_history(
        query=query,
        result_type=CompareResultHistory[RequestsPerSecondSchema],
        load_test_results_repository=load_test_results_repository,
        load_test_results_history_repository=load_test_results_history_repository
    )
