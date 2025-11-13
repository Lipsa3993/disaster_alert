# Disaster Alert System 🌪️

A **real-time disaster alert system** built with **Streamlit** and **OpenWeatherMap API**.  
It fetches weather data, detects potential disasters (storm, rain, heatwave, flood), and displays alerts with an **interactive map**.

---

## 🗂️ Project Structure
disaster_alert/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
├── utils/
│ ├── weather_utils.py
│ ├── alert_logic.py
│ └── map_display.py



---

## ⚡ Features

- Fetch current weather of any city.
- Generate disaster alerts based on temperature, humidity, wind speed, and weather conditions.
- Display an interactive map with safe (🟢) and alert (🔴) markers.

---

## 🔧 Setup Instructions

1. **Clone the repository** (or copy files to a folder):

```bash
git clone <your-repo-url>
cd disaster_alert


2. Create .env file with your OpenWeatherMap API key:

OWM_API_KEY=your_openweathermap_api_key


3. Install dependencies:

pip install -r requirements.txt


4. Run the Streamlit app:
streamlit run app.py


streamlit run app.py
5. Open the browser → enter a city → see weather, alerts, and map.

# 📦 Requirements

Python 3.8+

streamlit

python-dotenv

requests

folium

streamlit-folium

# 👩‍💻 Usage

Enter the city name in the input box.

View weather info (temperature, humidity, wind, description).

Check for alerts (heatwave, storm, flooding).

See interactive map with your location marker (red = alert, green = stable).

# 📝 Future Work

Phase 3: SMS/Email notifications using Twilio / Gmail API.

Add forecast-based alerts for upcoming 3–5 days.

Allow multiple locations on the map.