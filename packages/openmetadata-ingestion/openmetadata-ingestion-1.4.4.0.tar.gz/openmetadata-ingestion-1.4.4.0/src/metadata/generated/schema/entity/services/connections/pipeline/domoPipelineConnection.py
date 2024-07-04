# generated by datamodel-codegen:
#   filename:  entity/services/connections/pipeline/domoPipelineConnection.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import AnyUrl, BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr

from .. import connectionBasicType


class DomoPipelineType(Enum):
    DomoPipeline = 'DomoPipeline'


class DomoPipelineConnection(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Optional[DomoPipelineType] = Field(
        DomoPipelineType.DomoPipeline, description='Service Type', title='Service Type'
    )
    clientId: str = Field(..., description='Client ID for DOMO', title='Client ID')
    secretToken: CustomSecretStr = Field(
        ..., description='Secret token to connect to DOMO', title='Secret Token'
    )
    accessToken: Optional[str] = Field(
        None, description='Access token to connect to DOMO', title='Access Token'
    )
    apiHost: Optional[str] = Field(
        'api.domo.com',
        description='API Host to connect to DOMO instance',
        title='API Host',
    )
    instanceDomain: AnyUrl = Field(
        ...,
        description='URL of your Domo instance, e.g., https://openmetadata.domo.com',
        title='Instance Domain',
    )
    supportsMetadataExtraction: Optional[
        connectionBasicType.SupportsMetadataExtraction
    ] = Field(None, title='Supports Metadata Extraction')
