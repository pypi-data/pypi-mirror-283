# generated by datamodel-codegen:
#   filename:  api/data/createDashboard.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field, constr

from ...entity.data import dashboard
from ...type import basic, entityReference, lifeCycle, tagLabel


class CreateDashboardRequest(BaseModel):
    class Config:
        extra = Extra.forbid

    name: basic.EntityName = Field(
        ..., description='Name that identifies this dashboard.'
    )
    displayName: Optional[str] = Field(
        None,
        description='Display Name that identifies this Dashboard. It could be title or label from the source services',
    )
    description: Optional[basic.Markdown] = Field(
        None,
        description='Description of the database instance. What it has and how to use it.',
    )
    dashboardType: Optional[dashboard.DashboardType] = dashboard.DashboardType.Dashboard
    sourceUrl: Optional[basic.SourceUrl] = Field(
        None, description='Dashboard URL suffix from its service.'
    )
    project: Optional[str] = Field(
        None,
        description='Name of the project / workspace / collection in which the dashboard is contained',
    )
    charts: Optional[List[basic.FullyQualifiedEntityName]] = Field(
        None,
        description='List of fully qualified name of charts included in this Dashboard.',
    )
    dataModels: Optional[List[basic.FullyQualifiedEntityName]] = Field(
        None,
        description='List of fully qualified name of data models included in this Dashboard.',
    )
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags for this dashboard'
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this dashboard'
    )
    service: basic.FullyQualifiedEntityName = Field(
        ...,
        description='Link to the dashboard service fully qualified name where this dashboard is hosted in',
    )
    extension: Optional[basic.EntityExtension] = Field(
        None,
        description='Entity extension data with custom attributes added to the entity.',
    )
    domain: Optional[basic.FullyQualifiedEntityName] = Field(
        None, description='Fully qualified name of the domain the Dashboard belongs to.'
    )
    dataProducts: Optional[List[basic.FullyQualifiedEntityName]] = Field(
        None,
        description='List of fully qualified names of data products this entity is part of.',
    )
    lifeCycle: Optional[lifeCycle.LifeCycle] = Field(
        None, description='Life Cycle of the entity'
    )
    sourceHash: Optional[constr(min_length=1, max_length=32)] = Field(
        None, description='Source hash of the entity'
    )
