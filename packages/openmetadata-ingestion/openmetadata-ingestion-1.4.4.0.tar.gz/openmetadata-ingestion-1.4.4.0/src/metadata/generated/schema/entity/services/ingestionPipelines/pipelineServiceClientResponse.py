# generated by datamodel-codegen:
#   filename:  entity/services/ingestionPipelines/pipelineServiceClientResponse.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field


class PipelineServiceClientResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    code: int = Field(..., description='Status code')
    reason: Optional[str] = Field(
        None,
        description='Extra information to be sent back to the client, such as error traces.',
    )
    platform: str = Field(
        ..., description='Orchestration platform used by the Pipeline Service Client.'
    )
    version: Optional[str] = Field(None, description='Ingestion version being used.')
