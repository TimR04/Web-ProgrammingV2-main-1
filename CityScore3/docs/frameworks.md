# Frameworks and Libraries Used

This project uses a small, carefully selected set of Python libraries to remain lightweight, maintainable, and tailored to the specific needs of a data-driven web app like **CityScore3**.

---

## 🔧 Flask

> **Used for:** Building the web interface and handling user interactions

[Flask](https://flask.palletsprojects.com/) is a minimalist Python web framework that offers just enough to build powerful web apps — without unnecessary overhead.

**Why Flask for CityScore3?**

- We needed a **clean and customizable backend** to handle form input, routing, and templating
- Flask's simplicity matched our architecture perfectly: single-page frontend + multiple API calls
- It integrates seamlessly with HTML templates, which is ideal for rendering result pages dynamically
- We had full control over request handling, without being locked into opinionated structures

In CityScore3, Flask handles:

- User input (e.g. selected city and weights)
- Routing (`@app.route`) for detail pages and final result rendering
- Dynamic template rendering with Jinja2

---

## 🔗 Requests

> **Used for:** Fetching data from APIs

[Requests](https://docs.python-requests.org/) is Python's de-facto standard for HTTP communication.

**Why Requests for CityScore3?**

- Our project heavily depends on **real-time external data** from multiple APIs (weather, cost, air, etc.)
- Requests makes API communication **straightforward and reliable**
- We benefit from **clean error handling**, especially when APIs fail or return unexpected data
- Compatible with both RESTful JSON APIs and simpler GET-based services like Wikipedia

We use `requests` to connect to:

- OpenWeatherMap (weather & air pollution)
- World Bank API (health, education)
- Cost of Living API (via RapidAPI)
- Wikipedia summary API
- Unsplash (city background images)

---

## 📊 Pandas

> **Used for:** Processing structured data (CSV)

[Pandas](https://pandas.pydata.org/) is the backbone of many data-driven Python apps — and a perfect match for our local data use case.

**Why Pandas for CityScore3?**

- We needed to read, clean, and work with a **country-level CSV dataset** on crime scores
- Pandas allowed us to **filter by country**, normalize values, and extract specific metrics quickly
- Its concise syntax and fast performance made it ideal for a lightweight backend process

In this project, Pandas is used for:

- Loading and filtering the `crime_data.csv`
- Performing simple data transformations
- Supporting normalization logic for the safety score

---

## 🌐 urllib3

> **Used indirectly via Requests** for low-level HTTP handling

[urllib3](https://urllib3.readthedocs.io/) is used under the hood by `requests`, but we sometimes interact with it directly when suppressing SSL warnings.

**Why urllib3 matters in this project?**

- Some APIs (especially from RapidAPI) return **SSL errors or outdated certificates**
- We disable SSL warnings in selected modules to keep the console output clean
- Even though we don’t use it directly, it's critical for reliable HTTP behavior under the hood

---

## Summary

| Library   | Role                                | Why it was chosen for *CityScore3*                                   |
|-----------|-------------------------------------|-----------------------------------------------------------------------|
| Flask     | Web backend / routing               | Lightweight, fully customizable, perfect for form-based apps         |
| Requests  | API communication                   | Easy, stable, and ideal for calling multiple external APIs           |
| Pandas    | CSV processing                      | Fast and flexible handling of local country-level crime data         |
| urllib3   | HTTP infrastructure (via Requests)  | Ensures robust API connectivity and clean error suppression          |