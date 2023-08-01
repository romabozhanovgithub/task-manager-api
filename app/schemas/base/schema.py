from uuid import UUID
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


BaseSchemaConfig = ConfigDict(
    from_attributes=True,
    alias_generator=to_camel,
    populate_by_name=True,
    extra="ignore",
    json_encoders={
        UUID: str,
    },
)


class BaseSchema(BaseModel):
    model_config = BaseSchemaConfig
