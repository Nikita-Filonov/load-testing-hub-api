from typing import TypedDict

from sqlalchemy import Column, Float, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel
from utils.common.array import find


class ScenarioMethodSettingsDict(TypedDict):
    method: str
    requests_per_second: float


class ScenarioSettingsModel(MixinModel):
    __tablename__ = "scenario_settings"

    requests_per_second: Mapped[float] = Column(Float, nullable=False, default=0.0)

    methods_settings: Mapped[list[ScenarioMethodSettingsDict]] = Column(
        JSON, nullable=False, default=[]
    )

    scenario: Mapped[str] = Column(
        String,
        ForeignKey("scenarios.name", ondelete="CASCADE"),
        nullable=True,
        primary_key=True
    )

    def get_method_settings(self, method: str) -> ScenarioMethodSettingsDict | None:
        return find(lambda m: m['method'] == method, self.methods_settings, None)
