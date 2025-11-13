import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from utils.weather_utils import fetch_weather, fetch_forecast
from utils.map_utils import create_risk_map
from utils.alert_utils import translate_alert, log_alert, speak_alert, send_sms, analyze_weather
from streamlit_folium import st_folium

# Load environment variables
load_dotenv()

st.set_page_config(page_title="SMART Disaster Alert", layout="wide")
st.title("🌪️ SMART Disaster Alert & Safety Recommendation System")

# Create tabs
tabs = st.tabs(["Weather", "Map & Safe Zones", "Alerts & SMS", "Logs & Records"])

# ---------------- Tab 1: Weather ----------------
with tabs[0]:
    city = st.text_input("Enter city:", "Bhubaneswar")
    if city:
        weather_data, err = fetch_weather(city)
        forecast_data, err2 = fetch_forecast(city)
        
        if err: 
            st.error(err)
        elif err2: 
            st.error(err2)
        else:
            # Current weather
            st.subheader("🌡️ Current Weather")
            st.write(f"Temperature: {weather_data['main']['temp']} °C")
            st.write(f"Humidity: {weather_data['main']['humidity']} %")
            st.write(f"Wind: {weather_data['wind']['speed']} m/s")
            st.write(f"Condition: {weather_data['weather'][0]['description']}")

            # Analyze alerts
            alerts = analyze_weather(weather_data)
            risk_level = "High" if any(sym in a for a in alerts for sym in ["⚠️","💧","💨","🔥","❄️"]) else "Low"
            advice = "Move to higher ground if in low-lying areas." if risk_level=="High" else "No immediate risk."

            st.subheader("📢 Risk Summary")
            st.write(f"Risk Level: {risk_level}")
            for a in alerts: 
                st.write(f"- {a}")
            st.write(f"Advice: {advice}")

            # Log alert
            log_alert(city,
                      weather_data['main']['temp'],
                      weather_data['main']['humidity'],
                      weather_data['wind']['speed'],
                      risk_level,
                      " | ".join(alerts),
                      advice)

            # 5-day forecast chart
            df = pd.DataFrame([{"dt_txt": item["dt_txt"], "temp": item["main"]["temp"]} for item in forecast_data["list"]])
            df["dt_txt"] = pd.to_datetime(df["dt_txt"])
            df_daily = df.groupby(df["dt_txt"].dt.date)["temp"].mean().reset_index()
            st.subheader("📅 5-Day Average Temperature")
            st.line_chart(df_daily.rename(columns={"dt_txt":"Date", "temp":"Temperature"}).set_index("Date"))

# ---------------- Tab 2: Map & Safe Zones ----------------
with tabs[1]:
    if city:
        st.subheader("🗺️ Risk Map & Safe Zones")
        risk_map = create_risk_map(city)
        st_folium(risk_map, width=700, height=500)

# ---------------- Tab 3: Alerts & SMS ----------------
with tabs[2]:
    st.subheader("📲 Send Disaster Alerts")
    phone_number = st.text_input("Phone number (+91…):", "")
    lang = st.selectbox("Language:", ["English", "Hindi", "Odia"])
    tts_enabled = st.checkbox("🔊 Enable voice alert (TTS)", value=True)

    if st.button("Check & Send Alert") and city and phone_number:
        weather_data, _ = fetch_weather(city)
        alerts = analyze_weather(weather_data)
        advice = "Move to higher ground if in low-lying areas." if any("⚠️" in a or "💧" in a for a in alerts) else "No immediate risk."
        alert_msg = " | ".join(alerts) + " | " + advice
        alert_translated = translate_alert(alert_msg, lang)
        
        # Display alert
        st.success(alert_translated)

        # Send SMS
        sms_sent = send_sms([alert_translated], phone_number)
        if sms_sent:
            st.info(f"✅ SMS sent to {phone_number}")
        else:
            st.warning("⚠️ SMS not sent. Check Twilio configuration.")

        # Speak alert (TTS)
        if tts_enabled:
            try:
                speak_alert(alert_translated)
            except Exception as e:
                st.warning(f"TTS failed: {e}")

# ---------------- Tab 4: Logs & Records ----------------
with tabs[3]:
    st.subheader("🗂️ Logs & Records")
    try:
        df_logs = pd.read_csv("logs.csv")
    except FileNotFoundError:
        df_logs = pd.DataFrame(columns=["timestamp","city","temp","humidity","wind","risk_level","alert","advice"])

    st.dataframe(df_logs)
    st.download_button("⬇️ Download CSV", df_logs.to_csv(index=False), "logs.csv")
