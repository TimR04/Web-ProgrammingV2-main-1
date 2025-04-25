"""
Climate Module

Fetches monthly historical climate data for a given city using the OpenWeatherMap Aggregated Climate API.

API used:
- OpenWeatherMap Climate API: https://openweathermap.org/history#climate_monthly
"""

import requests
import calendar
from geocoding import get_coordinates


def fetch_monthly_climate_data(city_name: str, api_key: str) -> dict | None:
    """
    Fetches monthly aggregated climate data for a given city.

    Args:
        city_name (str): Name of the city (e.g., "Berlin").
        api_key (str): Your OpenWeatherMap API key.

    Returns:
        dict | None: A dictionary with month names as keys and climate data (JSON objects) as values,
                     or None if coordinates could not be determined.
    """
    lat, lon = get_coordinates(city_name)

    if lat is None or lon is None:
        print("❌ Could not determine coordinates.")
        return None

    monthly_data = {}

    for month in range(1, 13):
        url = (
            f"http://history.openweathermap.org/data/2.5/aggregated/month?"
            f"lat={lat}&lon={lon}&month={month}&appid={api_key}"
        )

        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            data = response.json()
            month_name = calendar.month_name[month]
            monthly_data[month_name] = data

        except Exception as e:
            print(f"❌ Error retrieving data for month {month}: {e}")
            monthly_data[calendar.month_name[month]] = None

    return monthly_data


if __name__ == "__main__":
    city = "Berlin"
    api_key = "7cd704982a17e0b79c63cb34c2f8ce58"
    climate_by_month = fetch_monthly_climate_data(city, api_key)

    if climate_by_month:
        print(f"\n📆 Monthly climate data for {city}:\n")
        for month, data in climate_by_month.items():
            print(f"\n📊 {month}:\n{data}")
    else:
        print("❌ No climate data found.")