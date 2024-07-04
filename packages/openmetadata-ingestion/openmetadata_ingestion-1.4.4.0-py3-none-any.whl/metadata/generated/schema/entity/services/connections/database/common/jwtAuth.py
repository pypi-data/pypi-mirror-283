# generated by datamodel-codegen:
#   filename:  entity/services/connections/database/common/jwtAuth.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr


class JwtAuth(BaseModel):
    class Config:
        extra = Extra.forbid

    jwt: Optional[CustomSecretStr] = Field(
        None, description='JWT to connect to source.', title='JWT'
    )
