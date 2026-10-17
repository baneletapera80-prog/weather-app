# Weather App

A Flet weather app that uses the OpenWeatherMap API.

## Features
- Search current weather by city
- 5-day forecast
- Home and Settings pages (routing)
- Celsius / Fahrenheit switch
- Error messages for unknown cities

## Run it
1. Get a free key at openweathermap.org
2. Copy `.env.example` to `.env` and add your key
3. python -m venv .venv
4. .venv\Scripts\activate.bat
5. python -m pip install flet requests python-dotenv
6. flet run

## Credits
Built during the FNB App Academy, based on the demo app. I extended it with the forecast, routing and settings, with help from an AI assistant.