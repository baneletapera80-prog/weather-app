import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
ICON_URL = "https://openweathermap.org/img/wn/{}@2x.png"


def _request(url, city, units):
    if not API_KEY:
        return None, "API key missing. Check your .env file"
    try:
        response = requests.get(
            url,
            params={"q": city, "appid": API_KEY, "units": units},
            timeout=10,
        )
    except requests.exceptions.RequestException:
        return None, "No internet connection"

    if response.status_code == 200:
        return response.json(), None
    if response.status_code == 401:
        return None, "Invalid or inactive API key"
    if response.status_code == 404:
        return None, f"City '{city}' not found"
    return None, f"Error {response.status_code}"


def get_weather(city, units="metric"):
    data, error = _request(WEATHER_URL, city, units)
    if error:
        return {"ok": False, "error": error}
    return {
        "ok": True,
        "city": f"{data['name']}, {data['sys']['country']}",
        "temp": round(data["main"]["temp"]),
        "description": data["weather"][0]["description"].title(),
        "icon": data["weather"][0]["icon"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
    }


def get_forecast(city, units="metric"):
    data, error = _request(FORECAST_URL, city, units)
    if error:
        return {"ok": False, "error": error}

    days = []
    for item in data["list"]:
        if item["dt_txt"].endswith("12:00:00"):
            days.append(
                {
                    "date": item["dt_txt"][:10],
                    "temp": round(item["main"]["temp"]),
                    "icon": item["weather"][0]["icon"],
                }
            )
    return {"ok": True, "days": days[:5]}