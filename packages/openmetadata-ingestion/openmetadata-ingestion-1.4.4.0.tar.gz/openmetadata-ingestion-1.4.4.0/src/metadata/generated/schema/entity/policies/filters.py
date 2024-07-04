# generated by datamodel-codegen:
#   filename:  entity/policies/filters.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel, Field

from ...type import basic


class Filters(BaseModel):
    __root__: Any = Field(..., title='Filters')


class Prefix(BaseModel):
    __root__: str = Field(..., description='Prefix path of the entity.')


class Regex(BaseModel):
    __root__: str = Field(..., description='Regex that matches the entity.')


class Tags(BaseModel):
    __root__: List[basic.EntityName] = Field(
        ..., description='Set of tags to match on (OR among all tags).'
    )
