# geocoding.py

This module converts city and country names into **geographical coordinates** (latitude & longitude).

---

## Purpose

Coordinates are required to request location-based data from other APIs (e.g., pollution, weather).

---

## Data Source

- **API**: OpenStreetMap's Nominatim
- **Input**: City name (optionally country)
- **Output**: Latitude and Longitude as floats

---

## Function

::: services.geocoding.get_coordinates