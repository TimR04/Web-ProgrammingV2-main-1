# iso_country_loader.py

This utility module is responsible for reading and mapping ISO3 country codes from a local CSV file.

---

## Purpose

In the CityScore3 application, various APIs and datasets use **ISO3 country codes** (e.g., `DEU`, `FRA`, `USA`).  
This module provides a consistent way to translate those codes into human-readable country names.

---

## How It Works

1. Reads a semicolon-separated CSV file (`iso_codes.csv`) located in the `data/` folder.
2. Extracts two columns:
    - `ISO3` → 3-letter country code (e.g. `DEU`)
    - `Country` → Full country name (e.g. `Germany`)
3. Returns a dictionary mapping each **ISO code** to its corresponding **country name**.

---

## Example Output

```python
{
    "DEU": "Germany",
    "FRA": "France",
    "ESP": "Spain",
    ...
}
```

## Function(s)

::: utils.iso_country_loader.load_iso_mapping
options:
show_signature: true
show_docstring: true