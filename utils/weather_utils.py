import requests
import os

def fetch_weather(city_name):
    api_key = os.getenv("OWM_API_KEY")
    if not api_key:
        return None, "OpenWeatherMap API key missing."
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None, f"Error: {r.text}"
        return r.json(), None
    except Exception as e:
        return None, str(e)

def fetch_forecast(city_name):
    api_key = os.getenv("OWM_API_KEY")
    if not api_key:
        return None, "OpenWeatherMap API key missing."
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None, f"Error: {r.text}"
        return r.json(), None
    except Exception as e:
        return None, str(e)
