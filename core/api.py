# # weather_app/core/api.py

# import requests
# from config import API_KEY

# def fetch_weather(city: str) -> dict:
 
#     if not API_KEY:
#         raise RuntimeError("Missing API key. Please set API_KEY in your .env file.")
#     url = (
#         "http://api.openweathermap.org/data/2.5/weather"
#         f"?q={city}&appid={API_KEY}&units=imperial"
#     )
#     resp = requests.get(url)
#     resp.raise_for_status()
#     return resp.json()
##########################################################################
import requests
from datetime import datetime, timedelta
from config import API_KEY

def fetch_weather(city: str) -> dict:
    """Fetch current weather for a city."""
    url = (
        "http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=imperial"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def get_coordinates(city: str) -> tuple[float, float]:
    """Resolve a city name to (lat, lon)."""
    url = (
        f"http://api.openweathermap.org/geo/1.0/direct"
        f"?q={city}&limit=1&appid={API_KEY}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise ValueError(f"City '{city}' not found")
    return data[0]["lat"], data[0]["lon"]

def fetch_historical(lat: float, lon: float, dt: int) -> dict:
    """Fetch one historical snapshot (free tier: last 5 days max)."""
    url = (
        "https://api.openweathermap.org/data/2.5/onecall/timemachine"
        f"?lat={lat}&lon={lon}&dt={dt}"
        f"&units=imperial&appid={API_KEY}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["current"]

def fetch_last_5_days(city: str) -> list[dict]:
    """
    Returns up to the last 5 days of weather for `city`.
    Each dict includes a 'date' key in MM/DD/YYYY format.
    """
    lat, lon = get_coordinates(city)
    now = datetime.utcnow()
    history = []
    for days_ago in range(1, 6):
        dt = int(
            (now - timedelta(days=days_ago))
            .replace(hour=12, minute=0, second=0, microsecond=0)
            .timestamp()
        )
        entry = fetch_historical(lat, lon, dt)
        entry["date"] = datetime.fromtimestamp(dt).strftime("%m/%d/%Y")
        history.append(entry)
    return history
