from enum import Enum


class APIRoutes(str, Enum):
    METHODS = '/methods'
    SERVICES = '/services'
    COMPARES = '/compares'
    SCENARIOS = '/scenarios'
    RATIO_RESULTS = '/ratio-results'
    METHOD_RESULTS = '/method-results'
    HISTORY_RESULTS = '/history-results'
    COMPARE_SETTINGS = '/compare-settings'
    EXCEPTION_RESULTS = '/exception-results'
    LOAD_TEST_RESULTS = '/load-test-results'
    AVERAGE_ANALYTICS = '/average-analytics'
    RESULTS_ANALYTICS = '/results-analytics'
    METHODS_ANALYTICS = '/methods-analytics'
    SCENARIO_SETTINGS = '/scenario-settings'
    INTEGRATIONS_KIBANA = '/integrations-kibana'
    INTEGRATIONS_GRAFANA = '/integrations-grafana'

    def as_tag(self) -> str:
        return self[1:]
