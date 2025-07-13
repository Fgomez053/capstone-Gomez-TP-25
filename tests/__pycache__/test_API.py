import requests
import json
from config import API_KEY

def fetch_weather(city: str) -> dict:
    """
    Fetch current weather for `city` from OpenWeatherMap.
    """
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        # Optional: get Celsius instead of Kelvin
        "units": "metric"
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()  # will raise an HTTPError on bad status
    return resp.json()

if __name__ == "__main__":
    data = fetch_weather("Seattle")
    # Pretty-print the JSON
    print(json.dumps(data, indent=2))