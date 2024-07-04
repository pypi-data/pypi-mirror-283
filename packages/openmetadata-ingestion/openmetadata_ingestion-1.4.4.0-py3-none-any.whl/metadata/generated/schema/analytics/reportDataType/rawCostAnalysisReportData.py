# generated by datamodel-codegen:
#   filename:  analytics/reportDataType/rawCostAnalysisReportData.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field

from ...type import entityReference, lifeCycle


class RawCostAnalysisReportData(BaseModel):
    class Config:
        extra = Extra.forbid

    entity: entityReference.EntityReference = Field(
        ..., description='Entity of the life cycle data'
    )
    lifeCycle: Optional[lifeCycle.LifeCycle] = Field(
        None, description='Life Cycle data related to the entity'
    )
    sizeInByte: Optional[float] = Field(None, description='Entity size in bytes')
