from sqlalchemy import Column, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped

from services.postgres.models.base.content_length import get_default_content_length_model_dict, \
    ContentLengthModelDict
from services.postgres.models.base.metrics import MetricsModelDict, get_default_metrics_model_dict
from services.postgres.models.base.number_of_users import NumberOfUsersModelDict, \
    get_default_number_of_users_model_dict
from utils.base.array import find
from utils.clients.postgres.mixin_model import MixinModel


class ScenarioResultSettingsDict(MetricsModelDict, NumberOfUsersModelDict):
    pass


def get_default_scenario_result_settings_dict() -> ScenarioResultSettingsDict:
    return ScenarioResultSettingsDict(
        **get_default_metrics_model_dict(),
        **get_default_number_of_users_model_dict()
    )


class ScenarioMethodSettingsDict(MetricsModelDict, ContentLengthModelDict):
    method: str


def get_default_scenario_method_settings_dict() -> ScenarioMethodSettingsDict:
    return ScenarioMethodSettingsDict(
        method="",
        **get_default_metrics_model_dict(),
        **get_default_content_length_model_dict(),
    )


class ScenarioSettingsModel(MixinModel):
    __tablename__ = "scenario_settings"

    result_settings: Mapped[ScenarioResultSettingsDict] = Column(
        JSON,
        default=get_default_scenario_result_settings_dict(),
        nullable=False,
    )
    methods_settings: Mapped[list[ScenarioMethodSettingsDict]] = Column(
        JSON, nullable=False, default=[]
    )

    scenario_id: Mapped[int] = Column(
        Integer,
        ForeignKey("scenarios.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True
    )

    def get_method_settings_or_default(self, method: str) -> ScenarioMethodSettingsDict:
        return find(
            lambda m: m['method'] == method, self.methods_settings,
            get_default_scenario_method_settings_dict()
        )
