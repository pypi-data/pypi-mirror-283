# generated by datamodel-codegen:
#   filename:  api/data/createContainer.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field, constr

from ...entity.data import container
from ...type import basic, entityReference, lifeCycle, tagLabel


class CreateContainerRequest(BaseModel):
    class Config:
        extra = Extra.forbid

    name: basic.EntityName = Field(
        ..., description='Name that identifies this Container model.'
    )
    displayName: Optional[str] = Field(
        None, description='Display Name that identifies this Container model.'
    )
    description: Optional[basic.Markdown] = Field(
        None, description='Description of the Container instance.'
    )
    service: basic.FullyQualifiedEntityName = Field(
        ...,
        description='Link to the storage service where this container is hosted in.',
    )
    parent: Optional[entityReference.EntityReference] = Field(
        None, description='Link to the parent container under which this entity sits.'
    )
    dataModel: Optional[container.ContainerDataModel] = Field(
        None,
        description="References to the container's data model, if data is structured, or null otherwise",
    )
    prefix: Optional[str] = Field(
        None, description='Optional prefix path defined for this container'
    )
    numberOfObjects: Optional[float] = Field(
        None, description='The number of objects/files this container has.'
    )
    size: Optional[float] = Field(
        None, description='The total size in KB this container has.'
    )
    fileFormats: Optional[List[container.FileFormat]] = Field(
        None,
        description='File & data formats identified for the container:  e.g. dataFormats=[csv, json]. These can be present both when the container has a dataModel or not',
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this database'
    )
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags for this Container Model'
    )
    extension: Optional[basic.EntityExtension] = Field(
        None,
        description='Entity extension data with custom attributes added to the entity.',
    )
    sourceUrl: Optional[basic.SourceUrl] = Field(
        None, description='Source URL of container.'
    )
    fullPath: Optional[str] = Field(
        None, description='Full path of the container/file.'
    )
    domain: Optional[str] = Field(
        None, description='Fully qualified name of the domain the Container belongs to.'
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
