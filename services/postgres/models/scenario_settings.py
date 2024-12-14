from typing import TypedDict

from sqlalchemy import Column, Float, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel
from utils.common.array import find


class ScenarioMethodSettingsDict(TypedDict):
    method: str
    response_time: float
    content_length: float
    min_response_time: float
    max_response_time: float
    number_of_requests: float
    number_of_failures: float
    requests_per_second: float
    failures_per_second: float


class ScenarioSettingsModel(MixinModel):
    __tablename__ = "scenario_settings"

    response_time: Mapped[float] = Column(Float, nullable=False, default=0.0)
    number_of_users: Mapped[float] = Column(Float, nullable=False, default=0.0)
    min_response_time: Mapped[float] = Column(Float, nullable=False, default=0.0)
    max_response_time: Mapped[float] = Column(Float, nullable=False, default=0.0)
    number_of_requests: Mapped[float] = Column(Float, nullable=False, default=0.0)
    number_of_failures: Mapped[float] = Column(Float, nullable=False, default=0.0)
    requests_per_second: Mapped[float] = Column(Float, nullable=False, default=0.0)
    failures_per_second: Mapped[float] = Column(Float, nullable=False, default=0.0)

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
        default = ScenarioMethodSettingsDict(
            method="",
            response_time=0.0,
            content_length=0.0,
            min_response_time=0.0,
            max_response_time=0.0,
            number_of_requests=0.0,
            number_of_failures=0.0,
            requests_per_second=0.0,
            failures_per_second=0.0
        )

        return find(lambda m: m['method'] == method, self.methods_settings, default)
