"""
Geocoding Module

Provides functionality to convert city names into geographic coordinates (latitude & longitude)
using the Nominatim API (OpenStreetMap).

API used:
- Nominatim (https://nominatim.openstreetmap.org/)
"""

import requests


def get_coordinates(city: str) -> tuple[float, float] | tuple[None, None]:
    """
    Retrieve the latitude and longitude for a given city name.

    Args:
        city (str): City name to geocode.

    Returns:
        tuple: (latitude, longitude) as floats, or (None, None) if not found or on error.
    """
    url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    headers = {'User-Agent': 'CityScoreApp/1.0'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            print("❌ City not found.")
    else:
        print(f"❌ API error: {response.status_code}")

    return None, None
