# generated by datamodel-codegen:
#   filename:  api/classification/loadTags.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from . import createClassification, createTag


class LoadTags(BaseModel):
    class Config:
        extra = Extra.forbid

    createClassification: createClassification.CreateClassificationRequest
    createTags: Optional[List[createTag.CreateTagRequest]] = Field(None, min_items=1)
