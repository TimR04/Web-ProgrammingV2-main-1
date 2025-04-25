# education.py

This module estimates a country’s **education score** based on global development indicators.  
It pulls data from the World Bank (via RapidAPI) and provides a normalized value between **0 and 100**.

---

## Purpose

Education is a key metric when comparing cities globally.  
While city-specific data is limited, we use **national-level data** to approximate education quality.

---

## Data Source

- **API**: World Bank API via RapidAPI
- **Input**: ISO country code (e.g., `"DE"` for Germany)
- **Output**:
    - Government expenditure on education (% of GDP)
    - Literacy rate (age 15+)
    - School enrollment (primary, secondary)

---

## ⚙️ How It Works

1. For each indicator, the module fetches the **latest available value** from the World Bank.
2. Each metric is **normalized to a 0–100 score**, where:
    - Higher literacy or enrollment = higher score
    - Lower government spending = worse score
3. A **weighted average** is calculated:
    - Literacy rate → 40%
    - Enrollment rate → 35%
    - Education expenditure → 25%
4. If any indicator is missing or unavailable, the score returns `None`.

---

## 📌 Function(s)

::: services.education.calculate_education_score
options:
show_signature: true
show_docstring: true