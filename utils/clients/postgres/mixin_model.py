from utils.clients.postgres.create_model import CreateModel
from utils.clients.postgres.filter_model import FilterModel
from utils.clients.postgres.update_model import UpdateModel


class MixinModel(
    FilterModel,
    CreateModel,
    UpdateModel
):
    __abstract__ = True
