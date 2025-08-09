from enum import Enum


class IntegrationSystemType(str, Enum):
    KIBANA = "KIBANA"
    GRAFANA = "GRAFANA"
    KUBERNETES = "KUBERNETES"
