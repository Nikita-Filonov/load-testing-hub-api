from apps.results.constants.method_results.protocol import ProtocolType


def snake_case_to_pascal_case(string: str) -> str:
    characters = string.split('_')
    return string if len(characters) == 1 else ''.join(char.capitalize() for char in characters)


def get_short_method(method: str, protocol: ProtocolType) -> str:
    match protocol:
        case ProtocolType.GRPC:
            return method.split('/')[-1]
        case ProtocolType.HTTP:
            return method
        case ProtocolType.KAFKA:
            return method
        case _:
            return method
