# generated by datamodel-codegen:
#   filename:  security/secrets/secretsManagerClientLoader.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum


class SecretsManagerClientLoader(Enum):
    noop = 'noop'
    airflow = 'airflow'
    env = 'env'
