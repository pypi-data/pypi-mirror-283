# generated by datamodel-codegen:
#   filename:  type/csvFile.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from . import basic


class CsvHeader(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str
    required: Optional[bool] = False
    description: basic.Markdown = Field(
        ..., description='Description of the header field for documentation purposes.'
    )
    examples: List[str] = Field(..., description='Example values for the field')


class CsvRecord(BaseModel):
    __root__: List[str] = Field(
        ...,
        description='Represents a CSV record that contains one row values separated by a separator.',
    )


class CsvFile(BaseModel):
    class Config:
        extra = Extra.forbid

    headers: Optional[List[CsvHeader]] = None
    records: Optional[List[CsvRecord]] = None
