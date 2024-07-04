# generated by datamodel-codegen:
#   filename:  entity/services/connections/search/customSearchConnection.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra, Field

from .. import connectionBasicType


class CustomSearchType(Enum):
    CustomSearch = 'CustomSearch'


class CustomSearchConnection(BaseModel):
    class Config:
        extra = Extra.forbid

    type: CustomSearchType = Field(
        ..., description='Custom search service type', title='Service Type'
    )
    sourcePythonClass: Optional[str] = Field(
        None,
        description='Source Python Class Name to instantiated by the ingestion workflow',
        title='Source Python Class Name',
    )
    connectionOptions: Optional[connectionBasicType.ConnectionOptions] = Field(
        None, title='Connection Options'
    )
