# utils/map_display.py
import streamlit as st
try:
    import folium
    from streamlit_folium import st_folium
    _MAP_READY = True
except Exception:
    _MAP_READY = False

def display_map(lat, lon, alerts):
    """
    Show folium map with marker colored by presence of alerts.
    alerts: list of strings
    """
    label_text = "\n".join(alerts or ["No alerts"])
    color = "green"
    if any(sym in label_text for sym in ["⚠️", "🔥", "💨", "💧"]):
        color = "red"

    if not _MAP_READY:
        st.warning("Install folium + streamlit-folium to view the map. Showing coords below.")
        st.write(f"Location: lat={lat}, lon={lon}")
        st.write("Alerts:")
        for a in alerts:
            st.write(f"- {a}")
        return

    m = folium.Map(location=[lat, lon], zoom_start=11)
    folium.Circle(location=[lat, lon], radius=3000, color=color, fill=True, fill_opacity=0.2).add_to(m)
    folium.Marker([lat, lon], popup=label_text, icon=folium.Icon(color=color)).add_to(m)

    # Example safe zones (static demo markers)
    safe_zones = [
        (lat + 0.03, lon + 0.03, "Community Center (Safe)"),
        (lat - 0.04, lon - 0.02, "School Ground (Evacuation)")
    ]
    for s in safe_zones:
        folium.Marker([s[0], s[1]], popup=s[2], icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)

    st_folium(m, width=700, height=480)
