# airpollution.py

This module provides access to **air quality data** and computes a normalized **air quality score**  
using the [OpenWeatherMap Air Pollution API](https://openweathermap.org/api/air-pollution).

---

## Purpose

Air quality is a key factor in assessing the livability of a city.  
This module allows us to retrieve real-time pollution data (e.g., PM2.5, PM10)  
and convert it into a score ranging from **0 (worst)** to **1 (best)**.

---

## ⚙️ How It Works (Air Quality)

1. Takes a city's coordinates (latitude & longitude)
2. Calls the OpenWeatherMap API to retrieve the latest pollution readings
3. Applies normalization to the **PM2.5** value (fine particulate matter)
4. Converts raw pollution value into a **normalized air quality score**:
   - **Low PM2.5** → score near **100** (clean air)
   - **High PM2.5** → score near **0** (polluted air)

The normalized air score contributes to the final City Score based on the user's selected weight.

---

## Why PM2.5?

PM2.5 is one of the most critical indicators of air pollution  
due to its ability to penetrate deep into the lungs.  
It is also the most consistently reported metric across the globe.

---

## 📌 Function(s)

::: services.airpollution.get_normalized_air_quality

Returns a score between 0 and 1 based on current PM2.5 levels.

::: services.airpollution.fetch_air_pollution_raw

Returns the **raw pollution data** from the OpenWeatherMap API for deeper inspection.

---

## Example Use Case

```python
lat, lon = 48.8566, 2.3522  # Paris coordinates
score = get_normalized_air_quality(lat, lon)