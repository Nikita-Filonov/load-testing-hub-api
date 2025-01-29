from typing import TypeVar

from pydantic import BaseModel

from apps.compares.controllers.compares.compare_results_history.base import normalize_compare_results_history
from apps.compares.schema.compares.compare_results_history.base import GetCompareResultsHistoryResponse, \
    CompareResultHistory, CompareResultsHistory
from apps.compares.schema.compares.compare_results_history.compare_method_results_history import \
    GetCompareMethodResultsHistoryQuery
from services.postgres.repositories.method_results import MethodResultsRepository
from services.postgres.repositories.method_results_history import MethodResultsHistoryRepository
from utils.base.strings import get_short_method
from utils.schema.metrics.number_of_requests import NumberOfRequestsSchema
from utils.schema.metrics.number_of_users import NumberOfUsersSchema
from utils.schema.metrics.requests_per_second import RequestsPerSecondSchema
from utils.schema.metrics.response_times import ResponseTimesSchema

T = TypeVar('T', bound=BaseModel)


async def get_compare_method_results_history(
        query: GetCompareMethodResultsHistoryQuery,
        result_type: type[CompareResultHistory[T]],
        method_results_repository: MethodResultsRepository,
        method_results_history_repository: MethodResultsHistoryRepository
) -> GetCompareResultsHistoryResponse[T]:
    method_result = await method_results_repository.get_by_method(
        method=query.method,
        load_test_result_id=query.load_test_result_id
    )
    method_results_history = await method_results_history_repository.filter_by_method_result_id(
        method_result.id
    )

    compare_with_method_results = await method_results_repository.filter_groped_by_id(
        method=query.method,
        load_test_result_ids=query.compare_with_load_test_results
    )
    compare_with_method_results_history = await method_results_history_repository.filter_by_method_result_ids_groped(
        list(compare_with_method_results)
    )

    compares = [
        CompareResultsHistory[T](
            title=f'Current: {get_short_method(method_result.method)}',
            results=[
                result_type(metrics=result.to_dict(), datetime=result.datetime)
                for result in method_results_history
            ]
        ),
        *[
            CompareResultsHistory[T](
                title=compare_with_method_results[method_result_id].get_compare_title(),
                results=[
                    result_type(metrics=result.to_dict(), datetime=result.datetime)
                    for result in results_history
                ]
            )
            for method_result_id, results_history in compare_with_method_results_history.items()
        ]
    ]

    return GetCompareResultsHistoryResponse[T](compares=normalize_compare_results_history(compares))


async def get_compare_method_results_history_response_times(
        query: GetCompareMethodResultsHistoryQuery,
        method_results_repository: MethodResultsRepository,
        method_results_history_repository: MethodResultsHistoryRepository
) -> GetCompareResultsHistoryResponse[ResponseTimesSchema]:
    return await get_compare_method_results_history(
        query=query,
        result_type=CompareResultHistory[ResponseTimesSchema],
        method_results_repository=method_results_repository,
        method_results_history_repository=method_results_history_repository
    )


async def get_compare_method_results_history_number_of_users(
        query: GetCompareMethodResultsHistoryQuery,
        method_results_repository: MethodResultsRepository,
        method_results_history_repository: MethodResultsHistoryRepository
) -> GetCompareResultsHistoryResponse[NumberOfUsersSchema]:
    return await get_compare_method_results_history(
        query=query,
        result_type=CompareResultHistory[NumberOfUsersSchema],
        method_results_repository=method_results_repository,
        method_results_history_repository=method_results_history_repository
    )


async def get_compare_method_results_history_number_of_requests(
        query: GetCompareMethodResultsHistoryQuery,
        method_results_repository: MethodResultsRepository,
        method_results_history_repository: MethodResultsHistoryRepository
) -> GetCompareResultsHistoryResponse[NumberOfRequestsSchema]:
    return await get_compare_method_results_history(
        query=query,
        result_type=CompareResultHistory[NumberOfRequestsSchema],
        method_results_repository=method_results_repository,
        method_results_history_repository=method_results_history_repository
    )


async def get_compare_method_results_history_requests_per_second(
        query: GetCompareMethodResultsHistoryQuery,
        method_results_repository: MethodResultsRepository,
        method_results_history_repository: MethodResultsHistoryRepository
) -> GetCompareResultsHistoryResponse[RequestsPerSecondSchema]:
    return await get_compare_method_results_history(
        query=query,
        result_type=CompareResultHistory[RequestsPerSecondSchema],
        method_results_repository=method_results_repository,
        method_results_history_repository=method_results_history_repository
    )
