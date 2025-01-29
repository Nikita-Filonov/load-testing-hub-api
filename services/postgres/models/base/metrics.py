from dataclasses import dataclass

from services.postgres.models.base.number_of_requests import NumberOfRequestsModel, \
    get_default_number_of_requests_model_dict, NumberOfRequestsModelDict, \
    NumberOfRequestsModelAverages
from services.postgres.models.base.percentiles import PercentilesModel, \
    get_default_percentiles_model_dict, PercentilesModelDict, PercentilesModelAverages
from services.postgres.models.base.requests_per_second import RequestsPerSecondModel, \
    get_default_requests_per_second_model_dict, RequestsPerSecondModelDict, \
    RequestsPerSecondModelAverages
from services.postgres.models.base.response_times import ResponseTimesModel, get_default_response_times_model_dict, \
    ResponseTimesModelDict, ResponseTimesModelAverages


class MetricsModelDict(
    PercentilesModelDict,
    ResponseTimesModelDict,
    NumberOfRequestsModelDict,
    RequestsPerSecondModelDict
):
    pass


def get_default_metrics_model_dict() -> MetricsModelDict:
    return MetricsModelDict(
        **get_default_percentiles_model_dict(),
        **get_default_response_times_model_dict(),
        **get_default_number_of_requests_model_dict(),
        **get_default_requests_per_second_model_dict()
    )


@dataclass
class MetricsModelAverages(
    PercentilesModelAverages,
    ResponseTimesModelAverages,
    NumberOfRequestsModelAverages,
    RequestsPerSecondModelAverages
):
    ...


class MetricsModel(
    PercentilesModel,
    ResponseTimesModel,
    NumberOfRequestsModel,
    RequestsPerSecondModel
):
    __abstract__ = True

    @classmethod
    def get_average_allowed_columns(cls):
        return (
            *PercentilesModel.get_average_allowed_columns(),
            *ResponseTimesModel.get_average_allowed_columns(),
            *NumberOfRequestsModel.get_average_allowed_columns(),
            *RequestsPerSecondModel.get_average_allowed_columns()
        )
