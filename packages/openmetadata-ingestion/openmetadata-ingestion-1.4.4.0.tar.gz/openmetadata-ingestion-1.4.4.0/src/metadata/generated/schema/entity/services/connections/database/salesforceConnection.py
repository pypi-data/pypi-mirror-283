# generated by datamodel-codegen:
#   filename:  entity/services/connections/database/salesforceConnection.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr

from .. import connectionBasicType


class SalesforceType(Enum):
    Salesforce = 'Salesforce'


class SalesforceConnection(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Optional[SalesforceType] = Field(
        SalesforceType.Salesforce, description='Service Type', title='Service Type'
    )
    username: str = Field(
        ...,
        description='Username to connect to the Salesforce. This user should have privileges to read all the metadata in Redshift.',
        title='Username',
    )
    password: Optional[CustomSecretStr] = Field(
        None, description='Password to connect to the Salesforce.', title='Password'
    )
    securityToken: Optional[CustomSecretStr] = Field(
        None, description='Salesforce Security Token.', title='Security Token'
    )
    sobjectName: Optional[str] = Field(
        None, description='Salesforce Object Name.', title='Object Name'
    )
    databaseName: Optional[str] = Field(
        None,
        description='Optional name to give to the database in OpenMetadata. If left blank, we will use default as the database name.',
        title='Database Name',
    )
    salesforceApiVersion: Optional[str] = Field(
        '42.0',
        description='API version of the Salesforce instance',
        title='Salesforce API Version',
    )
    salesforceDomain: Optional[str] = Field(
        'login', description='Domain of Salesforce instance', title='Salesforce Domain'
    )
    connectionOptions: Optional[connectionBasicType.ConnectionOptions] = Field(
        None, title='Connection Options'
    )
    connectionArguments: Optional[connectionBasicType.ConnectionArguments] = Field(
        None, title='Connection Arguments'
    )
    supportsMetadataExtraction: Optional[
        connectionBasicType.SupportsMetadataExtraction
    ] = Field(None, title='Supports Metadata Extraction')
