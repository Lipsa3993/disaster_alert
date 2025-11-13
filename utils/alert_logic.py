def analyze_weather(data):
    alerts = []
    if not data:
        return ["✅ Weather data missing."]

    weather_main = data.get("weather", [{}])[0].get("main", "")
    temp = data.get("main", {}).get("temp")
    wind_speed = data.get("wind", {}).get("speed", 0)
    rain = 0
    if data.get("rain"):
        rain = data.get("rain").get("1h", data.get("rain").get("3h", 0))

    if weather_main in ["Thunderstorm", "Tornado"]:
        alerts.append(f"⚠️ Severe {weather_main} warning!")
    if rain > 20:
        alerts.append("💧 Heavy rainfall alert!")
    if wind_speed >= 20:
        alerts.append("💨 Strong wind alert!")
    if temp is not None:
        if temp >= 45:
            alerts.append("🔥 Extreme heat alert!")
        elif temp <= 0:
            alerts.append("❄️ Extreme cold alert!")
    if not alerts:
        alerts.append("✅ Weather is stable. No alerts.")
    return alerts
