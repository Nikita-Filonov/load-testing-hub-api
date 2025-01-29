from pydantic import BaseModel, ConfigDict


class DatabaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        ser_json_timedelta='float'
    )
