"""
Cost of Living Module

Retrieves and processes cost of living data for a given city and country using the
"Cost of Living and Prices" API on RapidAPI.

API used:
- https://rapidapi.com/karnadi/api/cost-of-living-and-prices/
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = "ab8edca96cmshe86aae7faf8de8bp158d06jsn0db354d79061"

# Mapping of product categories to API good IDs
CATEGORIES = {
    "Real Estate (€/m²)": [1, 2],
    "Clothing": [5, 6, 7, 64],
    "Groceries": [9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27],
    "Rent": [28, 29, 30, 31],
    "Restaurants": [36, 37, 38],
    "Gasoline": [45],
    "Public Transport Pass": [46],
    "Utilities": [54],
    "Internet (60 Mbps)": [55]
}

# Value normalization ranges for scoring
NORMALIZATION_RANGES = {
    "Real Estate (€/m²)": (1000, 10000),
    "Clothing": (20, 150),
    "Groceries": (1, 10),
    "Rent": (300, 3000),
    "Restaurants": (5, 100),
    "Gasoline": (1.0, 2.5),
    "Public Transport Pass": (20, 120),
    "Utilities": (50, 500),
    "Internet (60 Mbps)": (10, 70)
}

# Predefined weights for each category
WEIGHTS = {
    "Real Estate (€/m²)": 0.15,
    "Clothing": 0.10,
    "Groceries": 0.15,
    "Rent": 0.20,
    "Restaurants": 0.10,
    "Gasoline": 0.05,
    "Public Transport Pass": 0.10,
    "Utilities": 0.10,
    "Internet (60 Mbps)": 0.05
}

def fetch_prices(city: str, country: str) -> list:
    url = "https://cost-of-living-and-prices.p.rapidapi.com/prices"
    querystring = {"city_name": city, "country_name": country}
    headers = {
        "x-rapidapi-host": "cost-of-living-and-prices.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, verify=False)
        response.raise_for_status()
        return response.json().get("prices", [])
    except requests.RequestException as e:
        print(f"❌ Error fetching cost data: {e}")
        return []

def fetch_cost_details(city: str, country: str) -> list[dict]:
    prices = fetch_prices(city, country)
    detailed = []

    if not prices:
        print("⚠️ No prices loaded.")
        return []

    for category, ids in CATEGORIES.items():
        items = []
        for p in prices:
            try:
                good_id = int(p.get("good_id", -1))
                if good_id in ids and p.get("avg") is not None:
                    items.append({
                        "name": p.get("item_name"),
                        "price": round(float(p["usd"]["avg"]), 2) if "usd" in p else None,
                        "currency": p.get("currency", "") or "EUR"
                    })
            except Exception as e:
                print(f"❌ Error parsing product: {e}")

        if items:
            avg = round(sum(i["price"] for i in items) / len(items), 2)
            detailed.append({
                "category": category,
                "products": items,
                "average": avg
            })

    return detailed

def get_normalized_cost_score(city, country):
    """
    Calculates a cost of living score (0–100), using USD average prices.
    Lower mean price → higher score. Stronger fluctuations between cheap/expensive.
    """
    print(f"🧪 Fetching cost data for: {city} ({country})")
    data = fetch_prices(city, country)
    print(f"📦 API Response: {data}")

    try:
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("No data or wrong format")

        # Extract USD average prices only
        avg_prices_usd = [
            float(item['usd']['avg']) for item in data
            if 'usd' in item and 'avg' in item['usd'] and item['usd']['avg'] not in [None, '', '0']
        ]

        if not avg_prices_usd:
            raise ValueError("No valid USD average prices found")

        mean_price = sum(avg_prices_usd) / len(avg_prices_usd)

        # Enhanced normalization range for stronger spread
        min_expected = 400   # super cheap cities
        max_expected = 8000  # super expensive cities

        # Non-linear scaling using exponential decay
        normalized = (max_expected - mean_price) / (max_expected - min_expected)
        score = max(0, min(round((normalized ** 1.5) * 100, 2), 100))

        return score

    except Exception as e:
        print(f"⚠️ Error in cost normalization: {e}")
        fallback_score = 60.0
        print(f"🧪 Using fallback cost score: {fallback_score}")
        return fallback_score

    