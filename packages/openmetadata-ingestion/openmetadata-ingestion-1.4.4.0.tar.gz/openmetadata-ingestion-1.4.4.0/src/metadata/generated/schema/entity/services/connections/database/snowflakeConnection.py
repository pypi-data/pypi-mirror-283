# generated by datamodel-codegen:
#   filename:  entity/services/connections/database/snowflakeConnection.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr

from .. import connectionBasicType


class SnowflakeType(Enum):
    Snowflake = 'Snowflake'


class SnowflakeScheme(Enum):
    snowflake = 'snowflake'


class SnowflakeConnection(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Optional[SnowflakeType] = Field(
        SnowflakeType.Snowflake, description='Service Type', title='Service Type'
    )
    scheme: Optional[SnowflakeScheme] = Field(
        SnowflakeScheme.snowflake,
        description='SQLAlchemy driver scheme options.',
        title='Connection Scheme',
    )
    username: str = Field(
        ...,
        description='Username to connect to Snowflake. This user should have privileges to read all the metadata in Snowflake.',
        title='Username',
    )
    password: Optional[CustomSecretStr] = Field(
        None, description='Password to connect to Snowflake.', title='Password'
    )
    account: str = Field(
        ...,
        description='If the Snowflake URL is https://xyz1234.us-east-1.gcp.snowflakecomputing.com, then the account is xyz1234.us-east-1.gcp',
        title='Account',
    )
    role: Optional[str] = Field(None, description='Snowflake Role.', title='Role')
    database: Optional[str] = Field(
        None,
        description='Database of the data source. This is optional parameter, if you would like to restrict the metadata reading to a single database. When left blank, OpenMetadata Ingestion attempts to scan all the databases.',
        title='Database',
    )
    warehouse: str = Field(..., description='Snowflake warehouse.', title='Warehouse')
    queryTag: Optional[str] = Field(
        None,
        description='Session query tag used to monitor usage on snowflake. To use a query tag snowflake user should have enough privileges to alter the session.',
        title='Query Tag',
    )
    privateKey: Optional[CustomSecretStr] = Field(
        None,
        description='Connection to Snowflake instance via Private Key',
        title='Private Key',
    )
    snowflakePrivatekeyPassphrase: Optional[CustomSecretStr] = Field(
        None,
        description='Snowflake Passphrase Key used with Private Key',
        title='Snowflake Passphrase Key',
    )
    includeTransientTables: Optional[bool] = Field(
        False,
        description='Optional configuration for ingestion of TRANSIENT tables, By default, it will skip the TRANSIENT tables.',
        title='Include Transient Tables',
    )
    clientSessionKeepAlive: Optional[bool] = Field(
        False,
        description='Optional configuration for ingestion to keep the client session active in case the ingestion process runs for longer durations.',
        title='Client Session Keep Alive',
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
    supportsUsageExtraction: Optional[
        connectionBasicType.SupportsUsageExtraction
    ] = None
    supportsLineageExtraction: Optional[
        connectionBasicType.SupportsLineageExtraction
    ] = None
    supportsDBTExtraction: Optional[connectionBasicType.SupportsDBTExtraction] = None
    supportsProfiler: Optional[connectionBasicType.SupportsProfiler] = Field(
        None, title='Supports Profiler'
    )
    supportsDatabase: Optional[connectionBasicType.SupportsDatabase] = Field(
        None, title='Supports Database'
    )
    supportsQueryComment: Optional[connectionBasicType.SupportsQueryComment] = Field(
        None, title='Supports Query Comment'
    )
    sampleDataStorageConfig: Optional[
        connectionBasicType.SampleDataStorageConfig
    ] = Field(None, title='Storage Config for Sample Data')
