from utils.weather_utils import fetch_weather
import folium

def create_risk_map(city_name):
    # Fetch coordinates dynamically from weather API
    weather_data, err = fetch_weather(city_name)
    if err or not weather_data:
        # fallback coordinates
        lat, lon = 20.2961, 85.8245  # Bhubaneswar
    else:
        lat = weather_data["coord"]["lat"]
        lon = weather_data["coord"]["lon"]

    m = folium.Map(location=[lat, lon], zoom_start=12)

    # High risk area (red)
    folium.Circle(location=[lat, lon], radius=2000, color="red", fill=True, fill_opacity=0.3).add_to(m)
    # Medium risk area (orange)
    folium.Circle(location=[lat + 0.01, lon + 0.01], radius=1000, color="orange", fill=True, fill_opacity=0.2).add_to(m)

    # "You are here" marker
    folium.Marker(location=[lat, lon], tooltip="You are here", icon=folium.Icon(color="blue")).add_to(m)

    # Example safe zones (adjust relative to city center)
    folium.Marker(location=[lat + 0.03, lon + 0.03], tooltip="Community Center (Safe)", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(location=[lat - 0.02, lon - 0.03], tooltip="School Ground (Evacuation)", icon=folium.Icon(color="green")).add_to(m)

    return m
