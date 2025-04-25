# crimerate.py

This module handles crime data processing using a **local CSV file**.  
It computes a **normalized safety score (0–100)** for a given country based on the crime index.

---

## Purpose

The goal of this module is to evaluate safety levels per country using static crime data.  
Instead of relying on live APIs, a curated dataset (`crime_data.csv`) is used for consistency and performance.

---

## ⚙️ How It Works

1. Loads the CSV file using `pandas`
2. Searches for the matching country (case-insensitive)
3. Normalizes the raw **crime index** into a **safety score** using:

    ```
    safety_score = (max_crime_value - value) / (max_crime_value - min_crime_value) * 100
    ```

4. Returns a score between **0 (dangerous)** and **100 (very safe)**

---

## 📌 Function(s)

::: utils.crimerate.calculate_safety_score
options:
show_signature: true
show_docstring: true

This function takes in the CSV path and country name, and returns a normalized safety score.

---

## ✅ Why Local CSV?

- More control over data quality
- Faster lookups compared to APIs
- Easily editable and transparent