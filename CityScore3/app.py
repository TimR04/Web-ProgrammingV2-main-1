"""
CityScore – City Comparison Web App

This is the main Flask application that powers the CityScore3 web tool.
It handles user input, performs data lookups via APIs and local datasets,
calculates weighted scores for each city, and renders interactive HTML pages.

Data sources used:
- Geocoding: OpenStreetMap Nominatim API
- Air Quality: OpenWeatherMap API
- Cost of Living: RapidAPI (Cost of Living & Prices)
- Education: World Bank API (seperate endpoints)
- Health: World Bank API (seperate endpoints)
- Safety: Local CSV (crime_data.csv)
- Weather: OpenWeatherMap Current Weather API
- City Info: Wikipedia Summary API
- City Image: Unsplash API
"""

import os
from datetime import datetime

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session

from services.geocoding import get_coordinates
from services.airpollution import get_normalized_air_quality, fetch_air_pollution_raw
from services.costofliving import get_normalized_cost_score, fetch_cost_details
from services.education import calculate_education_score, fetch_education_details
from utils.crimerate import calculate_safety_score, get_crime_index
from services.healthapi import calculate_health_score, fetch_health_details
from services.city_image import download_city_background
from services.wikipedia import get_wikipedia_summary
from services.currentweatherapi import fetch_weather_data
from utils.iso_country_loader import load_iso_mapping
from utils.city_facts import CITY_FUN_FACTS
from utils.final_score import calculate_city_score

# Define absolute paths to data files (platform-independent)
BASE_DIR = os.path.dirname(__file__)
ISO_CSV_PATH = os.path.join(BASE_DIR, "data", "iso_codes.csv")
CRIME_CSV_PATH = os.path.join(BASE_DIR, "data", "crime_data.csv")

# Load ISO-3 to country name mapping
ISO_TO_COUNTRY = load_iso_mapping(ISO_CSV_PATH)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Enables session handling


@app.route("/")
def landing_page():
    """Initial landing page with a welcome or project intro."""
    return render_template("landing.html")


@app.route("/index")
def index():
    """Main form for user input: city, country, and weighting sliders."""
    return render_template("index.html")


@app.route('/score', methods=['POST'])
def score():
    """
    Handles form submission, stores user input in session, redirects to loading screen.
    """
    city = request.form.get('city')
    country = request.form.get('country')

    if not city or not country:
        return render_template('result.html', error="❌ Please provide both city and country name.")

    try:
        weights = [
            float(request.form.get('weight_cost', 0)),
            float(request.form.get('weight_air', 0)),
            float(request.form.get('weight_edu', 0)),
            float(request.form.get('weight_safety', 0)),
            float(request.form.get('weight_health', 0))
        ]
    except ValueError:
        return render_template('result.html', error="❌ Invalid weights entered.")

    if abs(sum(weights) - 1.0) > 0.01:
        return render_template('result.html', error="❌ Weights must add up to exactly 1.0.")

    session['input_data'] = {
        'city': city,
        'country': country,
        'weights': weights
    }

    return redirect(url_for('loading_screen'))


@app.route("/loading")
def loading_screen():
    """
    Fun loading screen with city facts and image previews.
    """
    fun_facts = [
        {"city": city, "fact": fact,
         "image": f"/static/city_photos/{city.lower().replace(' ', '')}.jpg"}
        for city, fact in CITY_FUN_FACTS.items()
    ]
    return render_template("loading.html", fun_facts=fun_facts)


@app.route("/result")
def results_page():
    """
    Main result page logic.
    - Tries to use cached results from session.
    - Falls back to fresh calculation if needed.
    - Redirects to index only if nothing is available.
    """
    data = session.get("input_data")
    cached = session.get("results")

    if not data and cached:
        print("⚠️ input_data missing – using cached results")
        return render_template("result.html", **cached)

    if not data:
        return redirect(url_for("index"))

    city = data.get("city")
    country = data.get("country")
    weights = data.get("weights")

    if cached and cached.get("city") == city and cached.get("country") == country:
        print("✅ Using cached results")
        return render_template("result.html", **cached)

    if not city or not country or not weights:
        return redirect(url_for("index"))

    country_code = next((code for code, name in ISO_TO_COUNTRY.items()
                         if name.lower() == country.lower()), None)

    if not country_code:
        return render_template('result.html', error="❌ Country name not recognized in ISO mapping.")

    country_name = ISO_TO_COUNTRY[country_code]

    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        return render_template('result.html', error="❌ Could not determine coordinates for this city.")

    air_score = get_normalized_air_quality(lat, lon)
    cost_score = get_normalized_cost_score(city, country_name)
    education_score = calculate_education_score(country_code)
    safety_score = calculate_safety_score(CRIME_CSV_PATH, country_name)
    health_score = calculate_health_score(country_code)
    weather_data = fetch_weather_data(lat, lon)

    if None in [air_score, cost_score, education_score, safety_score, health_score]:
        return render_template('result.html', error="❌ Failed to load one or more required data points.")

    final_score = calculate_city_score(
        cost=cost_score,
        air=air_score,
        edu=education_score,
        safety=safety_score,
        health=health_score,
        weights=weights
    )

    background_path = download_city_background(city) or "/static/default.jpg"
    wikipedia_summary = get_wikipedia_summary(city, lang="en")
    fun_fact = CITY_FUN_FACTS.get(city.lower(), "🌍 Cities are full of surprises!")

    result_data = {
        "city": city,
        "country": country,
        "country_code": country_code,
        "cost_score": cost_score,
        "air_score": air_score,
        "education_score": education_score,
        "safety_score": safety_score,
        "health_score": health_score,
        "final_score": final_score,
        "weights": weights,
        "background_path": background_path,
        "wikipedia_summary": wikipedia_summary,
        "weather_data": weather_data,
        "fun_fact": fun_fact
    }
    session['results'] = result_data

    return render_template("result.html", **result_data)


# -------------------- Detail Views --------------------

@app.route("/details/cost")
def details_cost():
    """
    Shows cost of living breakdown per category (rent, food, transport, etc.).
    """
    city = request.args.get("city")
    country_code = request.args.get("country")
    country_name = ISO_TO_COUNTRY.get(country_code.upper(), country_code)
    details = fetch_cost_details(city, country_name)
    background_path = download_city_background(city) or "/static/default.jpg"

    return render_template(
        "details_cost.html",
        city=city,
        country=country_name,
        details=details,
        background_path=background_path,
        current_year=datetime.now().year
    )


@app.route("/details/air")
def details_air():
    """
    Displays detailed air quality values (PM2.5, NO2, etc.) for selected city.
    """
    city = request.args.get("city")
    country = request.args.get("country")
    lat, lon = get_coordinates(city)
    raw_data = fetch_air_pollution_raw(lat, lon)
    background_path = download_city_background(city) or "/static/default.jpg"

    return render_template(
        "details_air.html",
        city=city,
        country=country,
        data=raw_data,
        background_path=background_path,
        current_year=datetime.now().year
    )


@app.route("/details/education")
def details_education():
    """
    Returns all raw values and scores from World Bank education indicators.
    """
    city = request.args.get("city")
    country = request.args.get("country")

    if not city or not country:
        return render_template("result.html", error="❌ Missing city or country in URL.")

    details = fetch_education_details(country)
    background_path = download_city_background(city) or "/static/default.jpg"

    return render_template(
        "details_education.html",
        city=city,
        country=country,
        details=details,
        background_path=background_path,
        current_year=datetime.now().year
    )


@app.route("/details/safety")
def details_safety():
    """
    Shows crime index and compares with min/max crime levels from all countries in the dataset.
    """
    city = request.args.get("city")
    iso_code = request.args.get("country")
    background_path = download_city_background(city) or "/static/default.jpg"
    country_name = ISO_TO_COUNTRY.get(iso_code.upper(), iso_code)

    df = pd.read_csv(CRIME_CSV_PATH, sep=';', names=["Country", "CrimeScore"], decimal='.')
    df["Country"] = df["Country"].str.strip()
    df["CrimeScore"] = pd.to_numeric(df["CrimeScore"], errors="coerce")

    match = df[df["Country"].str.lower() == country_name.lower()]
    crime_value = match["CrimeScore"].values[0] if not match.empty else None

    min_row = df.loc[df["CrimeScore"].idxmin()]
    max_row = df.loc[df["CrimeScore"].idxmax()]

    return render_template(
        "details_safety.html",
        city=city,
        country=country_name,
        crime_value=crime_value,
        min_value=round(min_row["CrimeScore"], 2),
        min_country=min_row["Country"],
        max_value=round(max_row["CrimeScore"], 2),
        max_country=max_row["Country"],
        background_path=background_path,
        current_year=datetime.now().year
    )


@app.route("/details/health")
def details_health():
    """
    Displays detailed health stats (life expectancy, expenditure, physicians, etc.).
    """
    city = request.args.get("city")
    iso_code = request.args.get("country")
    country_name = ISO_TO_COUNTRY.get(iso_code.upper(), iso_code)
    background_path = download_city_background(city) or "/static/default.jpg"
    details = fetch_health_details(iso_code)

    return render_template(
        "details_health.html",
        city=city,
        country=country_name,
        details=details,
        background_path=background_path,
        current_year=datetime.now().year
    )


# -------------------- App Launch --------------------

if __name__ == '__main__':
    app.run(debug=True)
