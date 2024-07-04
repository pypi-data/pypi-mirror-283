# generated by datamodel-codegen:
#   filename:  metadataIngestion/dbtconfig/dbtBucketDetails.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field


class DbtBucketDetails(BaseModel):
    class Config:
        extra = Extra.forbid

    dbtBucketName: Optional[str] = Field(
        None,
        description='Name of the bucket where the dbt files are stored',
        title='DBT Bucket Name',
    )
    dbtObjectPrefix: Optional[str] = Field(
        None,
        description='Path of the folder where the dbt files are stored',
        title='DBT Object Prefix',
    )
