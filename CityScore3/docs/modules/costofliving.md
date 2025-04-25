# costofliving.py

This module fetches cost of living data via [RapidAPI's Cost of Living API](https://rapidapi.com/karnadi/api/cost-of-living-and-prices)  
and calculates a **normalized cost score (0–100)** for use in city comparison.

---

## Purpose

The **cost of living** is a crucial factor when evaluating cities.  
This module provides up-to-date price information for categories such as:

- Restaurants
- Groceries
- Transportation
- Housing
- Utilities

These are then used to calculate a **normalized cost score**,  
where **higher scores indicate more affordability**.

---

## Data Source

- **API**: Cost of Living API (via RapidAPI)
- **Input**: City and country
- **Output**: Average prices for a wide range of goods and services

---

## ⚙️ How It Works

1. Calls the API with city and country as input
2. Extracts prices for core categories (food, rent, transport, etc.)
3. Applies category weightings (e.g., rent has higher impact than clothing)
4. Averages prices and normalizes using global min/max ranges
5. Returns a score between **0 (expensive)** and **100 (affordable)**

---

## 📌 Function(s)

::: services.costofliving.fetch_prices
options:
show_signature: true
show_docstring: true

::: services.costofliving.fetch_cost_details
options:
show_signature: true
show_docstring: true

::: services.costofliving.get_normalized_cost_score
options:
show_signature: true
show_docstring: true

---

## Example Use Case

```python
score = get_normalized_cost_score("Berlin", "Germany")
print(score)  # e.g. 74.5 → quite affordable