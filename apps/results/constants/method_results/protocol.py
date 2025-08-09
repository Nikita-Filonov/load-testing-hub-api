from enum import Enum


class ProtocolType(str, Enum):
    HTTP = "http"
    GRPC = "grpc"
    KAFKA = "kafka"
