import pandas as pd
from datetime import datetime
import pyttsx3
import os
from twilio.rest import Client

# ---------------- Log alert ----------------
def log_alert(city, temp, humidity, wind, risk_level, alert_msg, advice):
    log_file = "logs.csv"
    df_new = pd.DataFrame([{
        "timestamp": datetime.now().isoformat(),
        "city": city,
        "temp": temp,
        "humidity": humidity,
        "wind": wind,
        "risk_level": risk_level,
        "alert": alert_msg,
        "advice": advice
    }])
    try:
        df_logs = pd.read_csv(log_file)
        df_logs = pd.concat([df_logs, df_new], ignore_index=True)
    except FileNotFoundError:
        df_logs = df_new
    df_logs.to_csv(log_file, index=False)
    return df_logs

# ---------------- TTS alert ----------------
def speak_alert(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

# ---------------- Translate alert ----------------
def translate_alert(message, lang):
    if lang == "English":
        return message
    elif lang == "Hindi":
        return "चेतावनी: " + message
    elif lang == "Odia":
        return "ସତର୍କ: " + message
    return message

# ---------------- SMS via Twilio ----------------
def send_sms(alerts, recipient_number):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_NUMBER")

    if not all([account_sid, auth_token, twilio_number]):
        print("Twilio credentials missing.")
        return False
    if not alerts:
        return False

    message_body = "\n".join(alerts)
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=twilio_number,
            to=recipient_number
        )
        print(f"SMS sent! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False

# ---------------- Weather alert logic ----------------
def analyze_weather(data):
    alerts = []
    if not data:
        return alerts
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
