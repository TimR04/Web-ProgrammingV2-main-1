# ⚙️ How Scoring and Weighting Works

GlobalCityScore uses a modular, weighted scoring system to evaluate and compare cities across five quality-of-life categories:

- Cost of Living, Air Quality, Education, Safety, Health

Each of these categories contributes to the **final City Score**, which is a single number between **0 (poor)** and **100 (ideal)**.

---

## 🧮 1. Normalization

Each category collects raw data from public APIs or datasets.

These raw values (e.g. air pollution in µg/m³, crime rates, literacy rates) are **normalized** to a common 0–100 scale:

- A score of **100** means *very good* conditions
- A score of **0** means *very poor* conditions

This normalization ensures that completely different units (e.g. percent, prices, ratios) can be aggregated meaningfully.

---

## ⚖️ 2. Weighting System

Users can assign a **weight** to each category (from 0 to 1) to control its impact on the final score.

All weights must add up to **1.0**.

---

## 🔢 3. Final Score Calculation

Once all five category scores are normalized, the system applies the weighting:

```python
final_score = (
    cost_score   * weight_cost   +
    air_score    * weight_air    +
    education    * weight_edu    +
    safety_score * weight_safety +
    health_score * weight_health
)
```
---

## 🎯 4. Goal of the City Score

The final score represents a **quality-of-life index** where:

- **100** = best possible value
- **0** = worst-case value 

Users can compare cities with a single number, while also exploring category-specific metrics in detail.
