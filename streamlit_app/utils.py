import os
from PIL import Image
import streamlit as st
import json

tram_stops_by_city = {
    "Bournemouth": [
        "Bournemouth Pier", "Boscombe", "Winton", "Lansdowne", "Southbourne"
    ],
    "Poole": [
        "Poole Station", "Parkstone", "Canford Cliffs", "Hamworthy"
    ],
    "Southampton": [
        "Central Station", "Portswood", "Highfield", "Woolston", "Ocean Village"
    ]
}

def get_stops_for_city(city):
    return tram_stops_by_city.get(city, [])


def load_image(path):
    """Safely load an image file with fallback."""
    if os.path.exists(path):
        return Image.open(path)
    else:
        st.warning(f"File not found: {path}")
        return None

def display_metric_card(label, value, unit="", icon="📊"):
    """Reusable styled metric block in Streamlit."""
    st.markdown(f"""
    <div style="padding:10px; border:1px solid #ccc; border-radius:8px; margin-bottom:10px;">
        <h4>{icon} {label}</h4>
        <p style="font-size: 24px;">{value} {unit}</p>
    </div>
    """, unsafe_allow_html=True)

def load_config(config_path="crowd_sim/evac_config.json"):
    """Load simulation config if exists."""
    import json
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        st.warning(f"Config file not found: {config_path}")
        return {}

def load_stats(path):
    with open(path) as f:
        return json.load(f)

def load_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
