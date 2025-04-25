"""
Air Pollution Module

This module handles fetching and scoring air pollution data for a given location.
It uses the OpenWeatherMap Air Pollution API to retrieve PM2.5, PM10, and NO2 levels,
then calculates a normalized air quality score.

API used:
- OpenWeatherMap Air Pollution API: https://openweathermap.org/api/air-pollution
"""

import requests


def normalize(value, min_val, max_val):
    """
    Normalize a value to a score from 0 (poor) to 100 (excellent).

    Args:
        value (float): Actual measurement value.
        min_val (float): Minimum expected value (best).
        max_val (float): Maximum expected value (worst).

    Returns:
        float: Score between 0 and 100.
    """
    score = (max_val - value) / (max_val - min_val) * 100
    return max(0, min(100, score))


def get_normalized_air_quality(lat: float, lon: float) -> int | None:
    """
    Fetch and calculate a normalized air quality score for a given location.

    Args:
        lat (float): Latitude of the city.
        lon (float): Longitude of the city.

    Returns:
        int | None: Score from 100 (excellent) to 0 (poor), or None if API call fails.
    """
    api_key = "7cd704982a17e0b79c63cb34c2f8ce58"
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        components = data["list"][0]["components"]

        pm25 = components.get("pm2_5", 0)
        pm10 = components.get("pm10", 0)
        no2 = components.get("no2", 0)

        # Normalization thresholds based on WHO recommendations
        score_pm25 = normalize(pm25, 0, 25)
        score_pm10 = normalize(pm10, 0, 50)
        score_no2 = normalize(no2, 0, 40)

        final_score = score_pm25 * 0.5 + score_pm10 * 0.3 + score_no2 * 0.2
        return round(final_score)  # ✅ korrekt: hoher Score = gute Luft


    except Exception as e:
        print(f"❌ Error fetching air quality data: {e}")
        return None


def fetch_air_pollution_raw(lat: float, lon: float) -> dict | None:
    """
    Fetch raw air quality component values from OpenWeatherMap.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.

    Returns:
        dict | None: Dictionary with pollutant values or None if request fails.
    """
    api_key = "7cd704982a17e0b79c63cb34c2f8ce58"
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["list"][0]["components"]

    except Exception as e:
        print(f"❌ Error fetching raw air pollution data: {e}")
        return None