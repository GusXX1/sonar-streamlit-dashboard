import streamlit as st
import pandas as pd
import requests

# ThingSpeak channel info
channel_id = "2951632"
read_api_key = "WQFE193EYDD0BACO"
results = 100

# Set page config
st.set_page_config(page_title="📡 Sonar IoT Dashboard", page_icon="🌐", layout="wide")

# Header
st.markdown("<h1 style='text-align: center; color: cyan;'>📡 Sonar IoT Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Live sensor data from ultrasonic sonar, visualized in real-time.</p>", unsafe_allow_html=True)
st.divider()

# Fetch data from ThingSpeak
url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}&results={results}"
res = requests.get(url).json()
feeds = res["feeds"]

# Convert to DataFrame
df = pd.DataFrame(feeds)
df["created_at"] = pd.to_datetime(df["created_at"])
df["distance_cm"] = pd.to_numeric(df["field1"])
df["led_value"] = pd.to_numeric(df["field2"])
df["tone_value"] = pd.to_numeric(df["field3"])
df.dropna(inplace=True)

# Show metrics
latest = df.iloc[-1]
col1, col2, col3 = st.columns(3)
col1.metric("📏 Distance (cm)", f"{latest['distance_cm']:.2f}")
col2.metric("💡 LED Intensity", f"{latest['led_value']:.2f}")
col3.metric("🔊 Tone Value", f"{latest['tone_value']:.2f}")
st.divider()

# Charts section
st.subheader("📈 Live Sensor Graphs")

with st.container():
    c1, c2, c3 = st.columns(3)
    c1.line_chart(df.set_index("created_at")["distance_cm"], use_container_width=True)
    c2.line_chart(df.set_index("created_at")["led_value"], use_container_width=True)
    c3.line_chart(df.set_index("created_at")["tone_value"], use_container_width=True)

st.caption("Made by Gustavo using Streamlit • Data from ThingSpeak Channel 2951632")
