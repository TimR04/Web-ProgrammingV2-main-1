# app.py

This file is the **main entry point** of the CityScore application.  
It runs the Flask web server, handles user input, connects all service modules, and returns the final city score along with details.

---

## Responsibilities

- Receives and validates user input (city, country, weights)
- Calls helper modules from `services/` and `utils/` to:
    - Geocode the location
    - Retrieve and normalize data from various APIs
    - Compute weighted scores
- Handles session storage and routing
- Renders HTML templates with all aggregated data

---

## Routing Functions

These routes define the app’s navigation flow:

### Landing & Forms

- `landing_page()`: Intro page
- `index()`: City form and weighting input
- `score()`: POST route to validate input and trigger the next step

### 🔹 Flow & Results

- `loading_screen()`: Fun fact and image loading screen
- `results_page()`: Main score + breakdown page

### 🔹 Details Pages

Each `/details/*` route shows additional data for a specific category.

- `/details/cost` → Cost breakdown
- `/details/air` → Air pollution data
- `/details/education` → Education indicators
- `/details/safety` → Crime statistics
- `/details/health` → Health indicators

---

## Utility Functions

::: app.calculate_city_score  
Calculates the final city score based on individual scores and user-defined weights.

::: app.get_country_name_from_code  
Maps a 2-letter ISO country code to a full country name using a local CSV file.

---

## Dependencies

This app uses the following helper modules:

- `services.geocoding`: Convert city names into coordinates
- `services.costofliving`: Fetch cost data and normalize
- `services.airpollution`: Get pollution data and normalize
- `services.healthapi`: Fetch and evaluate healthcare data
- `services.education`: Education score via World Bank
- `utils.crimerate`: Crime statistics from local CSV
- `services.city_image`: Background image handling
- `services.wikipedia`: Wiki summaries
- `services.currentweatherapi`: Live weather info
- `utils.iso_country_loader`: ISO mapping helper
- `utils.city_facts`: Random city fun facts

---

## Notes

- Requires a valid `app.secret_key` to enable session management.
- City photos are loaded from `/static/city_photos/`, with a default fallback.
- API failures or missing data will redirect the user to an error-friendly message.