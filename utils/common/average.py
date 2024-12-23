def get_average(items: list[float | int]) -> float:
    if len(items) == 0:
        return 0.0

    return sum(items) / len(items)
