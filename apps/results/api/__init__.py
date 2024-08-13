from fastapi import APIRouter

from apps.results.api.history_results import history_results_router
from apps.results.api.load_test_results import load_test_results_router
from apps.results.api.method_results import method_results_router
from apps.results.api.methods import methods_router
from apps.results.api.ratio_results import ratio_results_router

results_app_router = APIRouter()
results_app_router.include_router(methods_router)
results_app_router.include_router(ratio_results_router)
results_app_router.include_router(method_results_router)
results_app_router.include_router(history_results_router)
results_app_router.include_router(load_test_results_router)
