# streamlit_app/pages/AgentSimulation.py

import sys
import os
import json
from datetime import datetime
import streamlit as st

# Adjust path for imports from streamlit_app/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from streamlit_app.utils import get_stops_for_city

# Page config
st.set_page_config(page_title="Agent Simulation Config", page_icon="🛠️")
st.title("🛠️ Agent Simulation Configuration")

# --- 1. Select City and Tramline Stops ---
st.subheader("🏙️ Select City & Tramline")

cities = ["Bournemouth", "Poole", "Southampton"]
selected_city = st.selectbox("City", cities)

tram_stops = get_stops_for_city(selected_city)

col1, col2 = st.columns(2)
with col1:
    tram_start = st.selectbox("Start Point", tram_stops)
with col2:
    tram_end = st.selectbox("End Point", tram_stops)

if tram_start == tram_end:
    st.error("Start and end points must be different!")

# --- 2. Agent & Simulation Settings ---
st.subheader("👥 Agent & Simulation Settings")

num_agents = st.number_input("Number of Agents", min_value=10, max_value=1000, step=10, value=300)

st.markdown("### 🚶 Agent Type Distribution")
drive_pct = st.slider("🚗 Drive (%)", 0, 100, 40)
remaining = 100 - drive_pct
cycle_pct = st.slider("🚲 Cycle (%)", 0, remaining, 30)
tram_pct = 100 - drive_pct - cycle_pct
st.text(f"🚋 Tram (%) will be: {tram_pct}")

# Optional: date and time (can be used in your simulation config later)
st.subheader("🕒 Simulation Date & Time")
sim_date = st.date_input("Date", value=datetime.today())
sim_time = st.time_input("Time", value=datetime.strptime("08:00", "%H:%M").time())

# --- 3. Save & Run ---
if tram_start != tram_end:
    if st.button("🚀 Save & Run Simulation"):
        config = {
            "city": selected_city,
            "tramline": [tram_start, tram_end],
            "num_agents": num_agents,
            "agent_distribution": {
                "drive": drive_pct,
                "cycle": cycle_pct,
                "tram": tram_pct
            },
            "sim_date": sim_date.isoformat(),
            "sim_time": sim_time.strftime("%H:%M"),
            "scenarios": {
                "baseline": {},
                "tramline_extension": {
                    "add_edge": [tram_start, tram_end],
                    "length": 300  # Placeholder — you can replace with actual graph length
                }
            }
        }

        with open("transport_sim/config.json", "w") as f:
            json.dump(config, f, indent=2)

        st.success("✅ Configuration saved and simulation triggered!")

# --- 4. Summary Preview ---
st.subheader("📋 Configuration Preview")
st.json({
    "city": selected_city,
    "tram_start": tram_start,
    "tram_end": tram_end,
    "num_agents": num_agents,
    "agent_distribution": {
        "drive": drive_pct,
        "cycle": cycle_pct,
        "tram": tram_pct
    },
    "sim_date": sim_date.isoformat(),
    "sim_time": sim_time.strftime("%H:%M")
})
