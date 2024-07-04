# generated by datamodel-codegen:
#   filename:  system/eventPublisherJob.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from ..configuration import elasticSearchConfiguration
from ..type import basic
from . import indexingError


class Status(Enum):
    started = 'started'
    running = 'running'
    completed = 'completed'
    failed = 'failed'
    active = 'active'
    activeError = 'activeError'
    stopped = 'stopped'
    success = 'success'


class StepStats(BaseModel):
    totalRecords: Optional[int] = Field(0, description='Count of Total Failed Records')
    successRecords: Optional[int] = Field(
        0, description='Count of Total Successfully Records'
    )
    failedRecords: Optional[int] = Field(0, description='Count of Total Failed Records')


class Stats(BaseModel):
    class Config:
        extra = Extra.forbid

    jobStats: Optional[StepStats] = None
    entityStats: Optional[StepStats] = None


class RunMode(Enum):
    stream = 'stream'
    batch = 'batch'


class PublisherType(Enum):
    elasticSearch = 'elasticSearch'
    kafka = 'kafka'


class EventPublisherResult(BaseModel):
    class Config:
        extra = Extra.forbid

    name: Optional[str] = Field(None, description='Name of the result')
    timestamp: basic.Timestamp
    status: Status = Field(..., description='This schema publisher run job status.')
    failure: Optional[indexingError.IndexingAppError] = Field(
        None, description='Failure for the job'
    )
    stats: Optional[Stats] = None
    entities: Optional[List[str]] = Field(
        None, description='List of Entities to Reindex', unique_items=True
    )
    recreateIndex: Optional[bool] = Field(
        None, description='This schema publisher run modes.'
    )
    batchSize: Optional[int] = Field(
        None, description='Maximum number of events sent in a batch (Default 10).'
    )
    searchIndexMappingLanguage: Optional[
        elasticSearchConfiguration.SearchIndexMappingLanguage
    ] = Field(
        elasticSearchConfiguration.SearchIndexMappingLanguage.EN,
        description='Recreate Indexes with updated Language',
    )
    afterCursor: Optional[str] = Field(
        None,
        description='Provide After in case of failure to start reindexing after the issue is solved',
    )
