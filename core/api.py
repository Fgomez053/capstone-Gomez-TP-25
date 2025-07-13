# weather_app/core/api.py

import requests
from config import API_KEY

def fetch_weather(city: str) -> dict:
 
    if not API_KEY:
        raise RuntimeError("Missing API key. Please set API_KEY in your .env file.")
    url = (
        "http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=imperial"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()
