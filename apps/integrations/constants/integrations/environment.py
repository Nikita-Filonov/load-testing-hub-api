from enum import Enum


class IntegrationEnvironmentType(str, Enum):
    INTERNAL = 'INTERNAL'
    PRODUCTION = 'PRODUCTION'
