from typing import TypedDict

from sqlalchemy import Column, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped

from services.postgres.models.base.content_length import ContentLengthModelDict, get_default_content_length_model_dict
from services.postgres.models.base.metrics import MetricsModelDict, get_default_metrics_model_dict
from services.postgres.models.base.number_of_users import NumberOfUsersModelDict, get_default_number_of_users_model_dict
from utils.clients.postgres.mixin_model import MixinModel


class CompareSettingsWeightsDict(
    MetricsModelDict,
    ContentLengthModelDict,
    NumberOfUsersModelDict,
):
    pass


def get_default_compare_settings_weights_dict() -> CompareSettingsWeightsDict:
    defaults = get_default_metrics_model_dict()
    defaults['requests_per_second'] = 0.5
    defaults['average_response_time'] = 0.5

    return CompareSettingsWeightsDict(
        **defaults,
        **get_default_content_length_model_dict(),
        **get_default_number_of_users_model_dict()
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

    weights: Mapped[CompareSettingsWeightsDict] = Column(
        JSON,
        default=get_default_compare_settings_weights_dict(),
        nullable=False,
    )
    highlight_threshold: Mapped[CompareSettingsHighlightThresholdDict] = Column(
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
