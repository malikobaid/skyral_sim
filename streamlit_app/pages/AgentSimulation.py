# streamlit_app/pages/AgentSimulation.py
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import sys
import json
from datetime import datetime
import streamlit as st
import subprocess

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

# Bournemouth-specific default shares from Centre for Cities
default_drive = 63
default_cycle = 4
default_walk = 22
default_tram = 9

drive_pct = st.slider("🚗 Drive (%)", 0, 100, default_drive)
remaining = 100 - drive_pct
cycle_pct = st.slider("🚲 Cycle (%)", 0, remaining, default_cycle)
tram_pct = 100 - drive_pct - cycle_pct

st.text(f"🚋 Tram (%) will be: {tram_pct}")

st.caption(
    "Default modal share from Centre for Cities – "
    "[Bournemouth city profile](https://www.centreforcities.org/city/bournemouth/)"
)

# Optional: date and time
st.subheader("🕒 Simulation Date & Time")
sim_date = st.date_input("Date", value=datetime.today())
sim_time = st.time_input("Time", value=datetime.strptime("08:00", "%H:%M").time())

selected_traffic_level = st.selectbox("Traffic Level", ["off-peak", "rush hour"])

# --- 3. Save & Run ---
if st.button("🚀 Save & Run Simulation"):

    base_config = {
        "city": selected_city,
        "tramline": [tram_start, tram_end],
        "num_agents": num_agents,
        "hub": "Bournemouth Station",
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
                "tram_stops": [tram_start, tram_end],
                "length": 300
            }
        }
    }
    resultOk = True
    error_msgs = []

    for traffic in ["off-peak", "peak"]:
        config = base_config.copy()
        config["traffic"] = traffic
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", f"transport_sim/config_{traffic}.json")
        )
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        with st.spinner(f"Running simulation for {traffic}..."):
            run_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "transport_sim", "run_sim.py")
            )
            result = subprocess.run(["python3", run_path, config_path], capture_output=True, text=True)

        if result.returncode != 0:
            resultOk = False
            error_msgs.append(f"❌ {traffic} failed:\n{result.stderr.strip()}")

    if resultOk:
        st.success("✅ Simulation complete. Please check the Results tab.")
    else:
        st.error("❌ One or more simulations failed.")
        for msg in error_msgs:
            st.code(msg)

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
