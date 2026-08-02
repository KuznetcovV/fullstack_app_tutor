from pydantic import BaseModel, ConfigDict, field_validator

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    @field_validator("*", mode="after")
    @classmethod
    def validate_not_empty(cls, value):
        if isinstance(value, str) and not value:
            raise ValueError("Value cannot be empty")

        return value