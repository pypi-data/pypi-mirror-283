# generated by datamodel-codegen:
#   filename:  auth/revokeToken.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from pydantic import BaseModel, Extra

from ..type import basic


class GenerateJwtTokenRequest(BaseModel):
    class Config:
        extra = Extra.forbid

    id: basic.Uuid
