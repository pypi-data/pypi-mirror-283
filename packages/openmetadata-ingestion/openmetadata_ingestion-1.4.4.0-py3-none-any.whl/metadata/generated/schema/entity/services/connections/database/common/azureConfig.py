# generated by datamodel-codegen:
#   filename:  entity/services/connections/database/common/azureConfig.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field

from ......security.credentials import azureCredentials


class AzureConfigurationSource(BaseModel):
    class Config:
        extra = Extra.forbid

    azureConfig: Optional[azureCredentials.AzureCredentials] = Field(
        None, title='Azure Credentials Configuration'
    )
