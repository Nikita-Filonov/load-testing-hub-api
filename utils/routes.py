from enum import Enum


class APIRoutes(str, Enum):
    METHODS = '/methods'
    SERVICES = '/services'
    COMPARES = '/compares'
    SCENARIOS = '/scenarios'
    INTEGRATIONS = '/integrations'
    RATIO_RESULTS = '/ratio-results'
    METHOD_RESULTS = '/method-results'
    COMPARE_SETTINGS = '/compare-settings'
    EXCEPTION_RESULTS = '/exception-results'
    LOAD_TEST_RESULTS = '/load-test-results'
    AVERAGE_ANALYTICS = '/average-analytics'
    RESULTS_ANALYTICS = '/results-analytics'
    METHODS_ANALYTICS = '/methods-analytics'
    SCENARIO_SETTINGS = '/scenario-settings'
    METHOD_RESULTS_HISTORY = '/method-results-history'
    LOAD_TEST_RESULTS_HISTORY = '/load-test-results-history'

    def as_tag(self) -> str:
        return self[1:]
