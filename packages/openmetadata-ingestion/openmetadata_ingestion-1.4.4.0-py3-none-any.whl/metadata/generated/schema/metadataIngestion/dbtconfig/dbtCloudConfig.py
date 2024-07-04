# generated by datamodel-codegen:
#   filename:  metadataIngestion/dbtconfig/dbtCloudConfig.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import AnyUrl, BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr


class DbtConfigType(Enum):
    cloud = 'cloud'


class DbtCloudConfig(BaseModel):
    class Config:
        extra = Extra.forbid

    dbtConfigType: DbtConfigType = Field(..., description='dbt Configuration type')
    dbtCloudAuthToken: CustomSecretStr = Field(
        ...,
        description='dbt cloud account authentication token',
        title='dbt Cloud Authentication Token',
    )
    dbtCloudAccountId: str = Field(
        ..., description='dbt cloud account Id', title='dbt Cloud Account Id'
    )
    dbtCloudProjectId: Optional[str] = Field(
        None,
        description="In case of multiple projects in a dbt cloud account, specify the project's id from which you want to extract the dbt run artifacts",
        title='dbt Cloud Project Id',
    )
    dbtCloudJobId: Optional[str] = Field(
        None, description='dbt cloud job id.', title='dbt Cloud Job Id'
    )
    dbtCloudUrl: AnyUrl = Field(
        ...,
        description='URL to connect to your dbt cloud instance. E.g., https://cloud.getdbt.com or https://emea.dbt.com/',
        title='dbt Cloud URL',
    )
