# generated by datamodel-codegen:
#   filename:  configuration/authenticationConfiguration.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from ..entity.services.connections.metadata import openMetadataConnection
from ..security.client import oidcClientConfig, samlSSOClientConfig
from . import ldapConfiguration


class ClientType(Enum):
    public = 'public'
    confidential = 'confidential'


class ResponseType(Enum):
    id_token = 'id_token'
    code = 'code'


class AuthenticationConfiguration(BaseModel):
    class Config:
        extra = Extra.forbid

    clientType: Optional[ClientType] = Field(
        ClientType.public, description='Client Type'
    )
    provider: openMetadataConnection.AuthProvider
    responseType: Optional[ResponseType] = Field(
        ResponseType.id_token,
        description='This is used by auth provider provide response as either id_token or code.',
    )
    providerName: str = Field(
        ..., description='Custom OIDC Authentication Provider Name'
    )
    publicKeyUrls: List[str] = Field(..., description='List of Public Key URLs')
    authority: str = Field(..., description='Authentication Authority')
    clientId: str = Field(..., description='Client ID')
    callbackUrl: str = Field(..., description='Callback URL')
    jwtPrincipalClaims: List[str] = Field(..., description='Jwt Principal Claim')
    jwtPrincipalClaimsMapping: Optional[List[str]] = Field(
        None, description='Jwt Principal Claim Mapping'
    )
    enableSelfSignup: Optional[bool] = Field(False, description='Enable Self Sign Up')
    ldapConfiguration: Optional[ldapConfiguration.LdapConfiguration] = Field(
        None, description='LDAP Configuration in case the Provider is LDAP'
    )
    samlConfiguration: Optional[samlSSOClientConfig.SamlSSOClientConfig] = Field(
        None,
        description='Saml Configuration that is applicable only when the provider is Saml',
    )
    oidcConfiguration: Optional[oidcClientConfig.OidcClientConfig] = Field(
        None, description='Oidc Configuration for Confidential Client Type'
    )
