# generated by datamodel-codegen:
#   filename:  api/addGlossaryToAssetsRequest.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from ..type import entityReferenceList, tagLabel


class Operation(Enum):
    AddAssets = 'AddAssets'
    AddGlossaryTags = 'AddGlossaryTags'


class AddGlossaryToAssetsRequest(BaseModel):
    class Config:
        extra = Extra.forbid

    operation: Optional[Operation] = Field(
        None, description='Operation to be performed'
    )
    dryRun: Optional[bool] = Field(
        True,
        description='If true, the request will be validated but no changes will be made',
    )
    glossaryTags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Glossary Tags to be added'
    )
    assets: Optional[entityReferenceList.EntityReferenceList] = Field(
        None,
        description='List of assets to be created against which the glossary needs to be added.',
    )
