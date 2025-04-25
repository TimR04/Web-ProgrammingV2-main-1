"""
Health Score Module

Calculates health-related scores based on multiple World Bank indicators accessed via RapidAPI.

API used:
- World Development Indicators via RapidAPI: https://rapidapi.com/word-bank/api/world-development-indicators
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "x-rapidapi-key": "ab8edca96cmshe86aae7faf8de8bp158d06jsn0db354d79061",
    "x-rapidapi-host": "word-bank-world-development-indicators.p.rapidapi.com"
}

INDICATORS = {
    "SP.DYN.LE00.IN":  {"name": "Life Expectancy",               "min": 50,  "max": 85,  "weight": 0.25, "positive": True},
    "SP.DYN.IMRT.IN":  {"name": "Infant Mortality",              "min": 1,   "max": 80,  "weight": 0.25, "positive": False},
    "SH.XPD.CHEX.GD.ZS":{"name": "Health Expenditure (% of GDP)","min": 2,   "max": 15,  "weight": 0.20, "positive": True},
    "SH.MED.PHYS.ZS":  {"name": "Physicians per 1000",           "min": 0.2, "max": 5,   "weight": 0.15, "positive": True},
    "SH.MED.BEDS.ZS":  {"name": "Hospital Beds per 1000",        "min": 0.5, "max": 13,  "weight": 0.15, "positive": True}
}


def fetch_health_details(country: str) -> list[dict]:
    """
    Fetch raw health indicator values and their normalized scores.

    Args:
        country (str): ISO3 country code.

    Returns:
        list[dict]: List of indicators with name, year, raw value and normalized score.
    """
    details = []

    for indicator_id, info in INDICATORS.items():
        url = "https://word-bank-world-development-indicators.p.rapidapi.com/data"
        params = {"country": country, "indicator": indicator_id}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
            if response.status_code != 200:
                print(f"❌ API error for {info['name']}: Status {response.status_code}")
                continue
            data = response.json().get("data", {})
        except requests.RequestException as e:
            print(f"❌ Request error for {info['name']}: {e}")
            continue

        valid_data = {int(year): val for year, val in data.items() if val is not None}
        if not valid_data:
            continue

        latest_year = max(valid_data.keys())
        value = float(valid_data[latest_year])
        min_val = info["min"]
        max_val = info["max"]
        positive = info["positive"]

        score = (value - min_val) / (max_val - min_val) * 100 if positive else \
                (max_val - value) / (max_val - min_val) * 100

        score = max(0, min(100, score))

        details.append({
            "name": info["name"],
            "year": latest_year,
            "value": round(value, 2),
            "score": round(score, 2)
        })

    return details


def calculate_health_score(country: str) -> float | None:
    """
    Calculate an overall health score for a given country.

    Args:
        country (str): ISO3 country code.

    Returns:
        float | None: Weighted health score (0–100), or None on error.
    """
    total_score = 0

    for indicator_id, info in INDICATORS.items():
        url = "https://word-bank-world-development-indicators.p.rapidapi.com/data"
        params = {"country": country, "indicator": indicator_id}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
            if response.status_code != 200:
                print(f"❌ API error for {info['name']}: Status {response.status_code}")
                continue
            data = response.json().get("data", {})
        except requests.RequestException as e:
            print(f"❌ Request error for {info['name']}: {e}")
            continue

        valid_data = {int(year): val for year, val in data.items() if val is not None}
        if not valid_data:
            print(f"⚠️ No valid data for {info['name']}")
            continue

        latest_year = max(valid_data.keys())
        value = float(valid_data[latest_year])
        min_val = info["min"]
        max_val = info["max"]
        weight = info["weight"]
        positive = info["positive"]

        score = (value - min_val) / (max_val - min_val) * 100 if positive else \
                (max_val - value) / (max_val - min_val) * 100

        score = max(0, min(100, score))
        total_score += score * weight

    return round(total_score, 2) if total_score > 0 else None