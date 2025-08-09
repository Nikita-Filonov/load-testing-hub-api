from enum import Enum


class CompareSettingsContext(str, Enum):
    COMPARE_WITH_AVERAGE = "compare_with_average"
    COMPARE_WITH_PREVIOUS = "compare_with_previous"
    COMPARE_RESULT_WITH_RESULTS = "compare_result_with_results"
    COMPARE_RESULT_WITH_AVERAGES = "compare_result_with_averages"
    COMPARE_RESULT_WITH_SCENARIO = "compare_result_with_scenario"
    COMPARE_METHOD_WITH_SCENARIO = "compare_method_with_scenario"
    COMPARE_AVERAGES_WITH_SCENARIO = "compare_averages_with_scenario"
