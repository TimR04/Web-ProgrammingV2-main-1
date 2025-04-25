"""
Current Weather Module

Fetches live weather conditions using OpenWeatherMap's current weather API.

API used:
- https://openweathermap.org/current
"""

import requests


def fetch_weather_data(lat: float, lon: float, api_key: str = "7cd704982a17e0b79c63cb34c2f8ce58") -> dict | None:
    """
    Fetch current weather data (temperature, humidity, wind, etc.) for a given location.

    Args:
        lat (float): Latitude of the city.
        lon (float): Longitude of the city.
        api_key (str): OpenWeatherMap API key.

    Returns:
        dict | None: Dictionary with weather information or None on error.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=en&appid={api_key}"
    
    try:
        response = requests.get(url, verify=False)
        data = response.json()

        return {
            "temperature": round(data["main"]["temp"], 1),
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind_speed": round(data["wind"]["speed"] * 3.6)  # m/s → km/h
        }

    except Exception as e:
        print("❌ Failed to load weather data:", e)
        return None