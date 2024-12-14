from typing import Annotated

from fastapi import APIRouter, Depends

from apps.results.controllers.methods import get_methods, get_short_methods, get_method_details
from apps.results.schema.methods import GetMethodsQuery, GetMethodsResponse, GetShortMethodsResponse, \
    GetShortMethodsQuery, GetMethodDetailsQuery, GetMethodDetailsResponse
from services.postgres.repositories.method_results import MethodResultsRepository, get_method_results_repository
from utils.routes import APIRoutes

methods_router = APIRouter(
    prefix=APIRoutes.METHODS,
    tags=[APIRoutes.METHODS.as_tag()]
)


@methods_router.get('', response_model=GetMethodsResponse)
async def get_methods_view(
        query: Annotated[GetMethodsQuery, Depends(GetMethodsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_methods(query, method_results_repository)


@methods_router.get('/short', response_model=GetShortMethodsResponse)
async def get_short_methods_view(
        query: Annotated[GetShortMethodsQuery, Depends(GetShortMethodsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_short_methods(query, method_results_repository)


@methods_router.get('/details', response_model=GetMethodDetailsResponse)
async def get_method_details_view(
        query: Annotated[GetMethodDetailsQuery, Depends(GetMethodDetailsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_method_details(query, method_results_repository)
