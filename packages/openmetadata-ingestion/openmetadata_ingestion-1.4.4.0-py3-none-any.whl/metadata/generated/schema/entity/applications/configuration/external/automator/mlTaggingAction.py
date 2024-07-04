# generated by datamodel-codegen:
#   filename:  entity/applications/configuration/external/automator/mlTaggingAction.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Extra, Field


class MlTaggingActionType(Enum):
    MLTaggingAction = 'MLTaggingAction'


class MLTaggingAction(BaseModel):
    class Config:
        extra = Extra.forbid

    type: MlTaggingActionType = Field(
        ..., description='Application Type', title='Application Type'
    )
