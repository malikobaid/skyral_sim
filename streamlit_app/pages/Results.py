import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import streamlit as st
from streamlit_app.utils import load_stats, load_html

st.set_page_config(page_title="Results", page_icon="📊")
st.title("📊 Simulation Results")

st.markdown("""
Welcome to the Skyral Transport Simulation Demo. This tool allows you to:

- 🚉 Simulate tramline expansions and their impact on accessibility
- 🧍 Model pedestrian agents using real city maps
- 🎯 Compare baseline and intervention scenarios

➡️ To configure agent simulation parameters and define your tramline, please visit **`Agent Simulation`** in the sidebar.
""")

# Check if result files exist
base_path = "transport_sim/results"
stat_file = os.path.join(base_path, "tramline_stats.json")
map_file = os.path.join(base_path, "tramline_access_colored.html")

if not os.path.exists(stat_file) or not os.path.exists(map_file):
    st.warning("No simulation results found. Please run an Agent-Based Simulation first.")
    st.stop()

# Load and display stats
stats = load_stats(stat_file)
col1, col2, col3 = st.columns(3)
col1.metric("Average Distance", f"{stats['avg_distance']:.2f} m")
col2.metric("Unreachable Agents", f"{stats['unreachable']} / {stats['total_agents']}")
col3.metric("Max Distance", f"{stats['max_distance']:.2f} m")

# Load and display map
st.markdown("### Accessibility Map (with Tramline Overlay)")
map_html = load_html(map_file)
st.components.v1.html(map_html, height=600, scrolling=True)

st.info("Results shown are from the most recent simulation.")
