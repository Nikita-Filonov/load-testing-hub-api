def get_compare_percent(current: float, previous: float) -> float:
    if current == 0.0 or previous == 0.0:
        return 0.0

    return round(((current - previous) / previous) * 100, 2)
