import requests
from config.config import WEATHER_API_KEY

def get_weather_by_location(location, language):
    if not WEATHER_API_KEY:
        return None, None

    city = location.split(",")[0].strip()

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        r = requests.get(url, params=params, timeout=5)
        if r.status_code != 200:
            return None, None

        data = r.json()

        weather_data = {
            "city": city,
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "desc": data["weather"][0]["description"]
        }

        if language == "Hindi":
            text = f"""
📍 स्थान: {city}
🌡️ तापमान: {weather_data['temp']}°C
💧 नमी: {weather_data['humidity']}%
💨 हवा की गति: {weather_data['wind']} m/s
🌦️ मौसम: {weather_data['desc']}
"""
        else:
            text = f"""
📍 Location: {city}
🌡️ Temperature: {weather_data['temp']}°C
💧 Humidity: {weather_data['humidity']}%
💨 Wind speed: {weather_data['wind']} m/s
🌦️ Weather: {weather_data['desc']}
"""

        return text, weather_data

    except Exception:
        return None, None
