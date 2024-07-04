# generated by datamodel-codegen:
#   filename:  api/analytics/createWebAnalyticEvent.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field

from ...analytics import basic as basic_1
from ...type import basic, entityReference


class CreateWebAnalyticEvent(BaseModel):
    class Config:
        extra = Extra.forbid

    name: basic.EntityName = Field(
        ..., description='Name that identifies this report definition.'
    )
    displayName: Optional[str] = Field(
        None, description='Display Name the report definition.'
    )
    description: Optional[basic.Markdown] = Field(
        None, description='Description of the report definition.'
    )
    eventType: basic_1.WebAnalyticEventType = Field(
        ..., description='dimension(s) and metric(s) for a report'
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this report definition'
    )
