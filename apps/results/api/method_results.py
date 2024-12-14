from typing import Annotated

from fastapi import APIRouter, Depends

from apps.results.controllers.method_results import get_method_results, create_method_results
from apps.results.schema.method_results import GetMethodResultsQuery, GetMethodResultsResponse, \
    CreateMethodResultsRequest
from services.postgres.repositories.method_results import MethodResultsRepository, get_method_results_repository
from utils.routes import APIRoutes

method_results_router = APIRouter(
    prefix=APIRoutes.METHOD_RESULTS,
    tags=[APIRoutes.METHOD_RESULTS.as_tag()]
)


@method_results_router.get('', response_model=GetMethodResultsResponse)
async def get_method_results_view(
        query: Annotated[GetMethodResultsQuery, Depends(GetMethodResultsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
):
    return await get_method_results(query, method_results_repository)


@method_results_router.post('')
async def create_method_results_view(
        request: CreateMethodResultsRequest,
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
):
    return await create_method_results(request, method_results_repository)
