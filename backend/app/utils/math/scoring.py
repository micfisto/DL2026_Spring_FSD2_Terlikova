TOLERANCE_KM = 15
MAX_DISTANCE_KM = 100
MAX_POINTS = 1000


def calculate_points(distance_km: float) -> int:
    if distance_km <= TOLERANCE_KM:
        return MAX_POINTS

    if distance_km >= MAX_DISTANCE_KM:
        return 0

    ratio = (MAX_DISTANCE_KM - distance_km) / (MAX_DISTANCE_KM - TOLERANCE_KM)
    return int(MAX_POINTS * ratio)