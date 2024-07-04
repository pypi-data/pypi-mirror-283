# generated by datamodel-codegen:
#   filename:  entity/services/connections/pipeline/gluePipelineConnection.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra, Field

from .....security.credentials import awsCredentials
from .. import connectionBasicType


class GlueType(Enum):
    GluePipeline = 'GluePipeline'


class GluePipelineConnection(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Optional[GlueType] = Field(
        GlueType.GluePipeline, description='Service Type', title='Service Type'
    )
    awsConfig: awsCredentials.AWSCredentials = Field(
        ..., title='AWS Credentials Configuration'
    )
    supportsMetadataExtraction: Optional[
        connectionBasicType.SupportsMetadataExtraction
    ] = Field(None, title='Supports Metadata Extraction')
