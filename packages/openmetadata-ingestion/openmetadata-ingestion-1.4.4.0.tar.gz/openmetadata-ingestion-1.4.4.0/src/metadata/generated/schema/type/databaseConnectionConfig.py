# generated by datamodel-codegen:
#   filename:  type/databaseConnectionConfig.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field


class DatabaseConnectionConfig(BaseModel):
    class Config:
        extra = Extra.forbid

    username: Optional[str] = Field(
        None, description='username to connect  to the data source.'
    )
    password: Optional[str] = Field(
        None, description='password to connect  to the data source.'
    )
    hostPort: Optional[str] = Field(
        None, description='Host and port of the data source.'
    )
    database: Optional[str] = Field(None, description='Database of the data source.')
    schema_: Optional[str] = Field(
        None, alias='schema', description='schema of the data source.'
    )
    includeViews: Optional[bool] = Field(
        True,
        description='optional configuration to turn off fetching metadata for views.',
    )
    includeTables: Optional[bool] = Field(
        True,
        description='Optional configuration to turn off fetching metadata for tables.',
    )
    generateSampleData: Optional[bool] = Field(
        True, description='Turn on/off collecting sample data.'
    )
    sampleDataQuery: Optional[str] = Field(
        'select * from {}.{} limit 50', description='query to generate sample data.'
    )
    enableDataProfiler: Optional[bool] = Field(
        False,
        description='Run data profiler as part of ingestion to get table profile data.',
    )
    includeFilterPattern: Optional[List[str]] = Field(
        None,
        description='Regex to only fetch tables or databases that matches the pattern.',
    )
    excludeFilterPattern: Optional[List[str]] = Field(
        None, description='Regex exclude tables or databases that matches the pattern.'
    )
