def get_average(items: list[float | int]) -> float:
    return sum(items) / len(items) if items else 0.0
