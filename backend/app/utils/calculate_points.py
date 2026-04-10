def calculate_points(distance_km: float) -> int:
    points = max(0, 1000 - int(distance_km * 10))
    return points