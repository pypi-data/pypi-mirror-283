# generated by datamodel-codegen:
#   filename:  entity/feed/assets.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra

from ...type import entityReferenceList


class AssetsFeedInfo(BaseModel):
    class Config:
        extra = Extra.forbid

    updatedAssets: Optional[entityReferenceList.EntityReferenceList] = None
