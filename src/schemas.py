from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class EmailInput(CamelModel):
    subject: str
    body: str | None = None
    template_name: str | None = None
    template_variables: dict[str, Any] = {}


class SuccessResponse(CamelModel):
    message: str
