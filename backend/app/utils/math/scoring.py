TOLERANCE_KM = 15
MAX_DISTANCE_KM = 50
BASE_MAX_POINTS = 1000

DIFFICULTY_MULTIPLIERS = {
    "easy": 1.0,
    "medium": 1.5,
    "hard": 2.0
}


def get_max_points_for_difficulty(difficulty: str) -> int:
    multiplier = DIFFICULTY_MULTIPLIERS.get(difficulty, 1.0)
    return int(BASE_MAX_POINTS * multiplier)


def calculate_points(distance_km: float, difficulty: str = "easy") -> int:
    multiplier = DIFFICULTY_MULTIPLIERS.get(difficulty, 1.0)
    max_points = int(BASE_MAX_POINTS * multiplier)
    
    if distance_km <= TOLERANCE_KM:
        return max_points

    if distance_km >= MAX_DISTANCE_KM:
        return 0

    ratio = (MAX_DISTANCE_KM - distance_km) / (MAX_DISTANCE_KM - TOLERANCE_KM)
    return int(max_points * ratio)