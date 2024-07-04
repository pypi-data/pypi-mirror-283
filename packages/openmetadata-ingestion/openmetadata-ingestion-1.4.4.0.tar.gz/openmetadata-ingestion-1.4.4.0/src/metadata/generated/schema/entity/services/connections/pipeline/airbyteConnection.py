# generated by datamodel-codegen:
#   filename:  entity/services/connections/pipeline/airbyteConnection.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import AnyUrl, BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr

from .. import connectionBasicType


class AirbyteType(Enum):
    Airbyte = 'Airbyte'


class AirbyteConnection(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Optional[AirbyteType] = Field(
        AirbyteType.Airbyte, description='Service Type', title='Service Type'
    )
    hostPort: AnyUrl = Field(..., description='Pipeline Service Management/UI URL.')
    username: Optional[str] = Field(
        None, description='Username to connect to Airbyte.', title='Username'
    )
    password: Optional[CustomSecretStr] = Field(
        None, description='Password to connect to Airbyte.', title='Password'
    )
    supportsMetadataExtraction: Optional[
        connectionBasicType.SupportsMetadataExtraction
    ] = Field(None, title='Supports Metadata Extraction')
