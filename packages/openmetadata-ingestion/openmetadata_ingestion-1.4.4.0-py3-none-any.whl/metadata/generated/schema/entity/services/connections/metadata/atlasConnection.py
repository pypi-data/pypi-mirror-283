# generated by datamodel-codegen:
#   filename:  entity/services/connections/metadata/atlasConnection.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr

from .. import connectionBasicType


class AtlasType(Enum):
    Atlas = 'Atlas'


class AtlasConnection(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Optional[AtlasType] = Field(AtlasType.Atlas, description='Service Type')
    username: str = Field(
        ...,
        description='username to connect  to the Atlas. This user should have privileges to read all the metadata in Atlas.',
    )
    password: CustomSecretStr = Field(
        ..., description='password to connect  to the Atlas.'
    )
    hostPort: Optional[AnyUrl] = Field(
        None, description='Host and port of the Atlas service.', title='Host and Port'
    )
    databaseServiceName: Optional[List[str]] = Field(
        None, description='service type of the data source.'
    )
    messagingServiceName: Optional[List[str]] = Field(
        None, description='service type of the messaging source'
    )
    entity_type: str = Field(
        ...,
        description='Name of the Entity Type available in Atlas.',
        title='Entity Type',
    )
    connectionOptions: Optional[connectionBasicType.ConnectionOptions] = None
    connectionArguments: Optional[connectionBasicType.ConnectionArguments] = None
    supportsMetadataExtraction: Optional[
        connectionBasicType.SupportsMetadataExtraction
    ] = None
