from pydantic import BaseModel, ConfigDict
from pydantic.v1.utils import to_lower_camel


class Model(BaseModel):
    # model_config = ConfigDict(
    #     from_attributes=True,
    #     arbitrary_types_allowed=True,
    #     alias_generator=to_lower_camel,
    # )

    field1: str
    second_field: str
    third_field: str

    class Config:
        from_attributes = True
        alias_generator = to_lower_camel
        populate_by_name = True


class Class:
    def __init__(
        self, field1: str, secondField: str, third_field: str
    ) -> None:
        self.field1 = field1
        self.secondField = secondField
        self.third_field = third_field


instance = Class(field1="test", secondField="test2", third_field="test3")

model = Model.model_validate(instance)

print(model)
