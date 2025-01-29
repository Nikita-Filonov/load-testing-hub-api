from sqlalchemy import Column, String, Integer, select, func
from sqlalchemy.orm import Mapped, column_property

from services.postgres.models import ScenariosModel, LoadTestResultsModel
from services.postgres.models.base.status import StatusModel, ModelStatus


class ServicesModel(StatusModel):
    __tablename__ = "services"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    url: Mapped[str] = Column(String(250), nullable=False)
    name: Mapped[str] = Column(String(100), nullable=False)
    cluster: Mapped[str] = Column(String(100), nullable=True)
    namespace: Mapped[str] = Column(String(250), nullable=True)

    number_of_scenarios: Mapped[int] = column_property(
        select(func.count(ScenariosModel.id).label('number_of_scenarios'))
        .filter(
            ScenariosModel.status == ModelStatus.ACTIVE,
            ScenariosModel.service_id == id
        )
        .correlate_except(ScenariosModel)
        .scalar_subquery(),
        deferred=True
    )
    number_of_load_test_results: Mapped[int] = column_property(
        select(func.count(LoadTestResultsModel.id).label('number_of_load_test_results'))
        .filter(
            LoadTestResultsModel.status == ModelStatus.ACTIVE,
            LoadTestResultsModel.service_id == id
        )
        .correlate_except(LoadTestResultsModel)
        .scalar_subquery(),
        deferred=True
    )
