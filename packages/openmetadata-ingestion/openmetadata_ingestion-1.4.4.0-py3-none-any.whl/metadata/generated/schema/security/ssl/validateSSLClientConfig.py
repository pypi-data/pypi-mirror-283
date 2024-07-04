# generated by datamodel-codegen:
#   filename:  security/ssl/validateSSLClientConfig.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr


class ValidateSslClientConfig(BaseModel):
    class Config:
        extra = Extra.forbid

    caCertificate: Optional[CustomSecretStr] = Field(
        None,
        description='The CA certificate used for SSL validation.',
        title='CA Certificate',
    )
    sslCertificate: Optional[CustomSecretStr] = Field(
        None,
        description='The SSL certificate used for client authentication.',
        title='SSL Certificate',
    )
    sslKey: Optional[CustomSecretStr] = Field(
        None,
        description='The private key associated with the SSL certificate.',
        title='SSL Key',
    )
