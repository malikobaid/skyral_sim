# streamlit_app/pages/Overview.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")
st.title("🏠 Bournemouth Transit Optimisation Simulator")

st.markdown("""
### Problem
Urban transport systems often struggle to efficiently serve growing populations with diverse mobility needs. The current infrastructure may not support equitable access to key transport hubs.

### Proposed Solution
We simulate an agent-based transport accessibility model that helps decision-makers explore the impact of new tramline extensions and mobility policies.

### Features
- Agent-based travel distance simulation using real road networks
- Interactive tramline routing on map
- Metrics, accessibility heatmaps and summary stats

### Architecture
- OSM data via OSMnx  
- Agent-based model using NetworkX graphs  
- Streamlit UI with Folium maps and JSON configs

### Why It Matters
Improves understanding of how infrastructure changes can impact mobility, congestion, and equity.
""")
