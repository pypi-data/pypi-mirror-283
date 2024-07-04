# generated by datamodel-codegen:
#   filename:  analytics/reportDataType/webAnalyticEntityViewReportData.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from ...type import basic, tagLabel


class WebAnalyticEntityViewReportData(BaseModel):
    class Config:
        extra = Extra.forbid

    entityType: Optional[str] = Field(None, description='entity type')
    entityTier: Optional[str] = Field(None, description='entity tier')
    entityFqn: Optional[basic.FullyQualifiedEntityName] = Field(
        None, description='entity fully qualified name'
    )
    entityHref: Optional[str] = Field(None, description='entity href')
    tagsFQN: Optional[List[tagLabel.TagFQN]] = Field(None, description='Tags FQN')
    owner: Optional[str] = Field(None, description='Name of the entity owner')
    ownerId: Optional[str] = Field(None, description='Name of the entity owner')
    views: Optional[int] = Field(
        None, description='Number of time the entity was viewed'
    )
