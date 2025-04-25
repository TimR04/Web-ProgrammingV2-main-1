# healthapi.py

This module computes a **normalized health score** (0–100) for a given country using public health indicators.  
It helps estimate the quality of healthcare in a given location.

---

## Purpose

Access to quality healthcare is an essential factor for comparing cities globally.  
Since most health data is country-level, we use the best available national indicators.

---

## Data Source

- **API**: World Bank Health Indicators (via RapidAPI)
- **Input**: ISO country code (e.g., `"FR"`)
- **Indicators Used**:
    - Life expectancy at birth
    - Infant mortality rate
    - Health expenditure per capita

---

## ⚙️ How It Works

1. Fetches all relevant indicators for the specified country.
2. Each indicator is **normalized to a score between 0 and 100**:
    - Higher life expectancy → higher score
    - Lower infant mortality → higher score (inverted)
    - Higher health expenditure → higher score
3. Applies **weights** to reflect importance:
    - Life expectancy → 50%
    - Infant mortality → 30%
    - Health expenditure → 20%
4. Final output is a **weighted average** health score:
    - **100** = excellent healthcare
    - **0** = poor healthcare or missing data

---

## 📌 Function(s)

::: services.healthapi.calculate_health_score
options:
show_signature: true
show_docstring: true

::: services.healthapi.fetch_health_details
options:
show_signature: true
show_docstring: true