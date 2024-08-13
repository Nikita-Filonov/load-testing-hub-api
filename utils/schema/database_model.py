from pydantic import BaseModel, ConfigDict


class DatabaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
