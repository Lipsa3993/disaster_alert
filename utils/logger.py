# utils/logger.py
import os, pandas as pd
from datetime import datetime

LOG_FILE = "weather_alert_log.csv"

def log_alert(city, data, alerts, advice=""):
    rec = {
        "timestamp": datetime.now().isoformat(),
        "city": city,
        "temp": data.get("main", {}).get("temp"),
        "humidity": data.get("main", {}).get("humidity"),
        "wind": data.get("wind", {}).get("speed"),
        "risk_level": " | ".join(alerts),
        "alerts": " | ".join(alerts),
        "advice": advice
    }
    df_new = pd.DataFrame([rec])
    if os.path.exists(LOG_FILE):
        df_old = pd.read_csv(LOG_FILE)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
        df_all.to_csv(LOG_FILE, index=False)
    else:
        df_new.to_csv(LOG_FILE, index=False)
