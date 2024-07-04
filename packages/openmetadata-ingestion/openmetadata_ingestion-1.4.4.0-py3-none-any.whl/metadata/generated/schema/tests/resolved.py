# generated by datamodel-codegen:
#   filename:  tests/resolved.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra, Field

from ..type import entityReference


class TestCaseFailureReasonType(Enum):
    FalsePositive = 'FalsePositive'
    MissingData = 'MissingData'
    Duplicates = 'Duplicates'
    OutOfBounds = 'OutOfBounds'
    Other = 'Other'


class Resolved(BaseModel):
    class Config:
        extra = Extra.forbid

    testCaseFailureReason: TestCaseFailureReasonType = Field(
        ..., description='Reason of Test Case resolution.'
    )
    testCaseFailureComment: str = Field(
        ..., description='Test case failure resolution comment.'
    )
    resolvedBy: Optional[entityReference.EntityReference] = Field(
        None, description='User who resolved the test case failure.'
    )
