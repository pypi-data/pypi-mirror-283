# generated by datamodel-codegen:
#   filename:  entity/services/connections/common/sslConfig.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Optional, Union

from pydantic import BaseModel, Extra, Field

from . import sslCertPaths, sslCertValues


class SslConfig(BaseModel):
    class Config:
        extra = Extra.forbid

    certificates: Optional[
        Union[sslCertPaths.SslCertificatesByPath, sslCertValues.SslCertificatesByValues]
    ] = Field(None, description='SSL Certificates', title='SSL Certificates')
