# sonar_dashboard.py
import streamlit as st
import pandas as pd
import requests

# ThingSpeak settings
channel_id = "2951632"
read_api_key = "WQFE193EYDD0BACO"
results = 100

# Page setup
st.set_page_config(page_title="📡 Sonar Dashboard", layout="centered")
st.title("📡 Sonar IoT Dashboard")
st.markdown("Live distance & tone readings from ThingSpeak sensor")

# Fetch data
url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}&results={results}"
res = requests.get(url).json()
feeds = res["feeds"]

# Convert to DataFrame
df = pd.DataFrame(feeds)
df["created_at"] = pd.to_datetime(df["created_at"])
df["distance_cm"] = pd.to_numeric(df["field1"])
df["led_value"] = pd.to_numeric(df["field2"])
df["tone_value"] = pd.to_numeric(df["field3"])

# Show charts
st.line_chart(df.set_index("created_at")["distance_cm"], use_container_width=True)
st.line_chart(df.set_index("created_at")["led_value"], use_container_width=True)
st.line_chart(df.set_index("created_at")["tone_value"], use_container_width=True)

# Show latest data
st.subheader("🔍 Latest Readings")
latest = df.dropna().iloc[-1]
st.metric("Distance (cm)", f"{latest['distance_cm']:.2f}")
st.metric("LED Intensity", f"{latest['led_value']:.2f}")
st.metric("Tone Value", f"{latest['tone_value']:.2f}")
