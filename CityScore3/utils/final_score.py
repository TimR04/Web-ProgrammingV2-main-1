def calculate_city_score(cost, air, edu, safety, health, weights):
    """
    Calculate the final city score based on individual scores and user-defined weights.
    Score range: 0 (best) to 100 (worst)

    Args:
        cost, air, edu, safety, health (float): Normalized scores (0–100)
        weights (list of float): Weight for each category (should sum to 1.0)

    Returns:
        float or None: Weighted average score, or None if any score is missing
    """
    components = [cost, air, edu, safety, health]
    if None in components:
        return None
    weighted_score = sum(v * w for v, w in zip(components, weights))
    return round(weighted_score, 2)
