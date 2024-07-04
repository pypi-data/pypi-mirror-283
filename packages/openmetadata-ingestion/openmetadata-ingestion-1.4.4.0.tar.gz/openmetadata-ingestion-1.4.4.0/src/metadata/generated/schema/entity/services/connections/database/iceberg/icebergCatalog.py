# generated by datamodel-codegen:
#   filename:  entity/services/connections/database/iceberg/icebergCatalog.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from typing import Optional, Union

from pydantic import BaseModel, Extra, Field

from . import (
    dynamoDbCatalogConnection,
    glueCatalogConnection,
    hiveCatalogConnection,
    restCatalogConnection,
)


class IcebergCatalog(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str = Field(..., description='Catalog Name.', title='Name')
    connection: Union[
        hiveCatalogConnection.HiveCatalogConnection,
        restCatalogConnection.RestCatalogConnection,
        glueCatalogConnection.GlueCatalogConnection,
        dynamoDbCatalogConnection.DynamoDbCatalogConnection,
    ] = Field(
        ...,
        description='Catalog connection configuration, depending on your catalog type.',
        title='Connection',
    )
    databaseName: Optional[str] = Field(
        None,
        description="Custom Database Name for your Iceberg Service. If not set it will be 'default'.",
        title='Database Name',
    )
    warehouseLocation: Optional[str] = Field(
        None,
        description='Warehouse Location. Used to specify a custom warehouse location if needed.',
        title='Warehouse Location',
    )
