# generated by datamodel-codegen:
#   filename:  metadataIngestion/storage/storageMetadataS3Config.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field

from ...security.credentials import awsCredentials
from . import storageBucketDetails


class StorageMetadataS3Config(BaseModel):
    class Config:
        extra = Extra.forbid

    securityConfig: Optional[awsCredentials.AWSCredentials] = Field(
        None, title='S3 Security Config'
    )
    prefixConfig: storageBucketDetails.StorageMetadataBucketDetails = Field(
        ..., title='Storage Metadata Prefix Config'
    )
