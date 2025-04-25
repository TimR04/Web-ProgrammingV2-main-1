# 🌐 Data Sources & APIs

This project integrates various public and third-party APIs to gather real-time and historical data from trusted sources.

| Domain          | API/Service                                                | Data Retrieved                                                  |
|-----------------|-------------------------------------------------------------|------------------------------------------------------------------|
| Geocoding       | [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/) | Latitude & longitude of a city                                  |
| Air Quality     | [OpenWeatherMap Air Pollution API](https://openweathermap.org/api/air-pollution) | PM2.5, PM10, NO2 concentration levels                           |
| Cost of Living  | [RapidAPI – Cost of Living](https://rapidapi.com/karnadi/api/cost-of-living-and-prices/) | Prices for housing, food, transport, utilities, etc.            |
| Education       | [World Bank API](https://data.worldbank.org/) via RapidAPI | Literacy rate, enrollment rates, gov. expenditure on education  |
| Safety/Crime    | Local CSV (`crime_data.csv`)                                | Crime index per country                                         |
| Weather         | [OpenWeatherMap Current API](https://openweathermap.org/current) | Current temperature, humidity, wind speed, weather description  |
| Health          | World Bank API via RapidAPI                                 | Life expectancy, infant mortality, physicians & hospital beds    |
| Wikipedia       | [Wikipedia REST API](https://www.mediawiki.org/wiki/REST_API) | City summary / short description                                |