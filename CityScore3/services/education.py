"""
Education Score Module

Calculates a country's education quality score based on multiple World Bank indicators.

API used:
- World Development Indicators via RapidAPI: https://rapidapi.com/word-bank/api/world-development-indicators
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API headers
headers = {
    "x-rapidapi-key": "ab8edca96cmshe86aae7faf8de8bp158d06jsn0db354d79061",
    "x-rapidapi-host": "word-bank-world-development-indicators.p.rapidapi.com"
}

# Indicators with normalization and weighting config
INDICATORS = {
    "SE.ADT.LITR.ZS":     {"name": "Adult Literacy Rate",                "min": 40,  "max": 100, "weight": 0.20, "positive": True},
    "SE.PRM.ENRR":        {"name": "Primary School Enrollment",         "min": 50,  "max": 120, "weight": 0.15, "positive": True},
    "SE.SEC.ENRR":        {"name": "Secondary School Enrollment",       "min": 30,  "max": 110, "weight": 0.15, "positive": True},
    "SE.TER.ENRR":        {"name": "Tertiary School Enrollment",        "min": 10,  "max": 100, "weight": 0.15, "positive": True},
    "SE.XPD.TOTL.GD.ZS":  {"name": "Gov. Expenditure on Education from GDP (%)",     "min": 1.5, "max": 8.0,  "weight": 0.10, "positive": True},
    "SE.PRM.ENRL.TC.ZS":  {"name": "Pupil-teacher ratio (primary)",     "min": 10,  "max": 40,  "weight": 0.15, "positive": False},
    "SE.XPD.SECO.PC.ZS":  {"name": "Gov. expenditure per student (% GDP/capita)", "min": 5, "max": 35, "weight": 0.10, "positive": True}
}

def fetch_education_details(country: str) -> list[dict]:
    """
    Fetch detailed education indicator data for display.

    Args:
        country (str): Country code (e.g., 'DEU').

    Returns:
        list of dict: List of indicator name, value, year, unit.
    """
    details = []

    for indicator_id, info in INDICATORS.items():
        url = "https://word-bank-world-development-indicators.p.rapidapi.com/data"
        params = {"country": country, "indicator": indicator_id}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
            if response.status_code != 200:
                continue
            data = response.json().get("data", {})
        except requests.RequestException:
            continue

        valid_data = {int(year): val for year, val in data.items() if val is not None}
        if not valid_data:
            continue

        latest_year = max(valid_data)
        value = round(float(valid_data[latest_year]), 2)

        details.append({
            "id": indicator_id,
            "name": info["name"],
            "value": value,
            "year": latest_year,
            "unit": "%" if "ZS" in indicator_id else None  # primitive Einheitenerkennung
        })

    return details

def calculate_education_score(country: str) -> float | None:
    """
    Calculate a weighted education quality score for a given country.

    Args:
        country (str): Country code (e.g., 'DEU', 'USA').

    Returns:
        float | None: Education score (0–100), or None if data is missing.
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
            print(f"❌ Request failed for {info['name']}: {e}")
            continue

        valid_data = {int(year): val for year, val in data.items() if val is not None}
        if not valid_data:
            print(f"⚠️ No valid data found for {info['name']}")
            continue

        latest_year = max(valid_data)
        value = float(valid_data[latest_year])
        min_val = info["min"]
        max_val = info["max"]
        weight = info["weight"]
        positive = info["positive"]

        if positive:
            score = (value - min_val) / (max_val - min_val) * 100
        else:
            score = (max_val - value) / (max_val - min_val) * 100

        score = max(0, min(100, score))
        weighted = score * weight
        total_score += weighted

    return round(total_score, 2) if total_score > 0 else None