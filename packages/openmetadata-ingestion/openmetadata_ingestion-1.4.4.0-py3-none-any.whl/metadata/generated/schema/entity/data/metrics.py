# generated by datamodel-codegen:
#   filename:  entity/data/metrics.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from ...type import basic, entityHistory, entityReference, tagLabel, usageDetails, votes


class Metrics(BaseModel):
    class Config:
        extra = Extra.forbid

    id: basic.Uuid = Field(
        ..., description='Unique identifier that identifies this metrics instance.'
    )
    name: basic.EntityName = Field(
        ..., description='Name that identifies this metrics instance uniquely.'
    )
    fullyQualifiedName: Optional[basic.FullyQualifiedEntityName] = Field(
        None,
        description="A unique name that identifies a metric in the format 'ServiceName.MetricName'.",
    )
    displayName: Optional[str] = Field(
        None, description='Display Name that identifies this metric.'
    )
    description: Optional[basic.Markdown] = Field(
        None,
        description='Description of metrics instance, what it is, and how to use it.',
    )
    version: Optional[entityHistory.EntityVersion] = Field(
        None, description='Metadata version of the entity.'
    )
    updatedAt: Optional[basic.Timestamp] = Field(
        None,
        description='Last update time corresponding to the new version of the entity in Unix epoch time milliseconds.',
    )
    updatedBy: Optional[str] = Field(None, description='User who made the update.')
    href: Optional[basic.Href] = Field(
        None, description='Link to the resource corresponding to this entity.'
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this metrics.'
    )
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags for this chart.'
    )
    service: entityReference.EntityReference = Field(
        ..., description='Link to service where this metrics is hosted in.'
    )
    usageSummary: Optional[usageDetails.UsageDetails] = Field(
        None, description='Latest usage information for this database.'
    )
    changeDescription: Optional[entityHistory.ChangeDescription] = Field(
        None, description='Change that lead to this version of the entity.'
    )
    deleted: Optional[bool] = Field(
        False, description='When `true` indicates the entity has been soft deleted.'
    )
    domain: Optional[entityReference.EntityReference] = Field(
        None, description='Domain the Metrics belongs to.'
    )
    votes: Optional[votes.Votes] = None
