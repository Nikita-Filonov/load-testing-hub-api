from enum import Enum
from typing import TypedDict

from sqlalchemy import Column, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class CompareSettingsContext(str, Enum):
    COMPARE_WITH_AVERAGE = "compare_with_average"
    COMPARE_WITH_PREVIOUS = "compare_with_previous"
    COMPARE_RESULT_WITH_RESULTS = "compare_result_with_results"
    COMPARE_RESULT_WITH_AVERAGES = "compare_result_with_averages"
    COMPARE_RESULT_WITH_SCENARIO = "compare_result_with_scenario"
    COMPARE_METHOD_WITH_SCENARIO = "compare_method_with_scenario"
    COMPARE_AVERAGES_WITH_SCENARIO = "compare_averages_with_scenario"


class CompareSettingsWeightsDict(TypedDict):
    response_time: float
    min_response_time: float
    max_response_time: float
    number_of_requests: float
    number_of_failures: float
    requests_per_second: float
    failures_per_second: float


def get_default_compare_settings_weights_dict() -> CompareSettingsWeightsDict:
    return CompareSettingsWeightsDict(
        response_time=0.5,
        min_response_time=0.0,
        max_response_time=0.0,
        number_of_requests=0.0,
        number_of_failures=0.0,
        requests_per_second=0.5,
        failures_per_second=0.0
    )


class CompareSettingsHighlightThresholdDict(TypedDict):
    compare_with_average: float
    compare_with_previous: float
    compare_result_with_results: float
    compare_result_with_averages: float
    compare_result_with_scenario: float
    compare_method_with_scenario: float
    compare_averages_with_scenario: float


def get_default_compare_settings_highlight_threshold_dict() -> CompareSettingsHighlightThresholdDict:
    return CompareSettingsHighlightThresholdDict(
        compare_with_average=-50,
        compare_with_previous=-50,
        compare_result_with_results=-50,
        compare_result_with_averages=-50,
        compare_result_with_scenario=-50,
        compare_method_with_scenario=-50,
        compare_averages_with_scenario=-50
    )


class CompareSettingsModel(MixinModel):
    __tablename__ = "compare_settings"

    weights: CompareSettingsWeightsDict = Column(
        JSON,
        default=get_default_compare_settings_weights_dict(),
        nullable=False,
    )
    highlight_threshold: CompareSettingsHighlightThresholdDict = Column(
        JSON,
        default=get_default_compare_settings_highlight_threshold_dict(),
        nullable=False
    )

    service_id: Mapped[int] = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True
    )
