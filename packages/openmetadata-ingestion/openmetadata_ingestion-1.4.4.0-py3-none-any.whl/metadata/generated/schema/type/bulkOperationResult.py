# generated by datamodel-codegen:
#   filename:  type/bulkOperationResult.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Extra, Field, conint

from . import basic


class RowCount(BaseModel):
    __root__: conint(ge=0) = Field(..., description='Type used to indicate row count')


class Index(BaseModel):
    __root__: conint(ge=1) = Field(
        ...,
        description='Type used to indicate row number or field number. In CSV the indexes start with 1.',
    )


class Response(BaseModel):
    class Config:
        extra = Extra.forbid

    request: Optional[Any] = Field(
        None, description='Request that can be processed successfully.'
    )
    message: Optional[str] = Field(None, description='Message for the request.')


class BulkOperationResult(BaseModel):
    class Config:
        extra = Extra.forbid

    dryRun: Optional[bool] = Field(
        None, description='True if the operation has dryRun flag enabled'
    )
    status: Optional[basic.Status] = None
    abortReason: Optional[str] = Field(
        None,
        description='Reason why import was aborted. This is set only when the `status` field is set to `aborted`',
    )
    numberOfRowsProcessed: Optional[RowCount] = None
    numberOfRowsPassed: Optional[RowCount] = None
    numberOfRowsFailed: Optional[RowCount] = None
    successRequest: Optional[List[Response]] = Field(
        None, description='Request that can be processed successfully.'
    )
    failedRequest: Optional[List[Response]] = Field(
        None, description='Failure Request that can be processed successfully.'
    )
