import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import sys
import streamlit as st
from streamlit_app.utils import load_stats, load_html
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from transport_sim.simulation import load_config

config = load_config()
AGENTS_USED = config['num_agents']
config = load_config()
AGENTS_USED = config['num_agents']

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

st.set_page_config(page_title="Results", page_icon="📊")
st.title("📊 Simulation Results")

# st.markdown("""
# Welcome to the Skyral Transport Simulation Demo. This tool allows you to:
#
# - 🚉 Simulate tramline expansions and their impact on accessibility
# - 🧍 Model pedestrian agents using real city maps
# - 🎯 Compare baseline and intervention scenarios
#
# ➡️ To configure agent simulation parameters and define your tramline, please visit **`Agent Simulation`** in the sidebar.
# """)

# Check if result files exist
base_path = "transport_sim/results"
stat_file = os.path.join(base_path, "tramline_stats.json")
map_file = os.path.join(base_path, "tramline_access_colored.html")

if not os.path.exists(stat_file) or not os.path.exists(map_file):
    st.warning("No simulation results found. Please run an Agent-Based Simulation first.")
    st.stop()

# Load stats
baseline = load_stats("transport_sim/results/baseline_stats.json")
tramline = load_stats("transport_sim/results/tramline_stats.json")

def safe(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return round(val, 2)
    return val

# Load config to get traffic level

st.markdown(f"🚦 Traffic condition used: **{config.get('traffic', 'off-peak').title()}**")


POPULATION = 527_000
AGENTS_USED = tramline["total_agents"]
SCALING_FACTOR = POPULATION // AGENTS_USED

modes = tramline["modes"].keys()
baseline_scaled = [baseline["modes"][m]["count"] * SCALING_FACTOR for m in modes]
tramline_scaled = [tramline["modes"][m]["count"] * SCALING_FACTOR for m in modes]

x = np.arange(len(modes))
width = 0.35

fig, ax = plt.subplots()
bars1 = ax.bar(x - width/2, baseline_scaled, width, label='Baseline')
bars2 = ax.bar(x + width/2, tramline_scaled, width, label='Tramline')

ax.set_ylabel('Estimated People')
ax.set_title('Estimated Mode Usage Scaled to Bournemouth Population')
ax.set_xticks(x)
ax.set_xticklabels([m.title() for m in modes])
ax.legend()
ax.bar_label(bars1, fmt="%.0f", padding=3)
ax.bar_label(bars2, fmt="%.0f", padding=3)

st.markdown("### 👥 Population-Scaled Mode Usage Comparison")
st.caption(
    f"Estimated based on Bournemouth population of **527,000**, "
    f"scaled from **{AGENTS_USED}** simulated agents. "
    f"➡️ 1 agent ≈ **{round(527_000 / AGENTS_USED)} people**. "
    "[📊 Source](https://www.centreforcities.org/city/bournemouth/)"
)
st.pyplot(fig)
# -------------------------
# PART 1: Summary Improvement Table
# -------------------------
def clean(value):
    """Round numeric values, leave others untouched."""
    if isinstance(value, (int, float)):
        return round(value, 2)
    return value  # Don't inject '—' here

def format_display(val):
    """Render '—' in display for None or inf, else show rounded value."""
    if val is None or val == float("inf"):
        return "—"
    return round(val, 2)

def highlight_delta(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return "background-color: lightgreen"
        elif val < 0:
            return "background-color: salmon"
    return ""

# Compute raw values (keep all as float or None)
rows_summary = []
for mode in sorted(set(baseline["modes"]) | set(tramline["modes"])):
    base = baseline["modes"].get(mode, {})
    tram = tramline["modes"].get(mode, {})

    base_avg = base.get("avg_distance")
    tram_avg = tram.get("avg_distance")
    delta = round(base_avg - tram_avg, 2) if base_avg is not None and tram_avg is not None else None

    rows_summary.append({
        "Mode": mode.title(),
        "Before (m)": base_avg,
        "After (m)": tram_avg,
        "Δ Avg (m)": delta
    })

# Build DataFrame — keep raw numbers
df_summary = pd.DataFrame(rows_summary).set_index("Mode")

# Sort with proper float handling
df_summary["sort_col"] = df_summary["Δ Avg (m)"].apply(lambda x: x if isinstance(x, (int, float)) else float("-inf"))
df_summary = df_summary.sort_values("sort_col", ascending=False).drop(columns="sort_col")

# Now style with '—' where needed
styled_summary = (
    df_summary.style
    .format({col: format_display for col in df_summary.columns})
    .map(highlight_delta, subset=["Δ Avg (m)"])
)

# Display
st.markdown("### 🎯 Sorted Avg Distance Improvements")
st.dataframe(styled_summary, use_container_width=True)



# Load and display map
st.markdown("### Accessibility Map (with Tramline Overlay)")
map_html = load_html(map_file)
st.components.v1.html(map_html, height=600, scrolling=True)

st.info("Results shown are from the most recent simulation.")

# -------------------------
# PART 2: Full Breakdown Table
# -------------------------
rows_detailed = []
for mode in sorted(set(baseline["modes"]) | set(tramline["modes"])):
    base = baseline["modes"].get(mode, {})
    tram = tramline["modes"].get(mode, {})

    rows_detailed.append({
        "Mode": mode.title(),
        "Agent Count (Before)": base.get("count", 0),
        "Agent Count (After)": tram.get("count", 0),
        "Unreachable (Before)": base.get("unreachable", 0),
        "Unreachable (After)": tram.get("unreachable", 0),
        "Avg Distance (Before)": safe(base.get("avg_distance")),
        "Avg Distance (After)": safe(tram.get("avg_distance")),
        "Max Distance (Before)": safe(base.get("max_distance")),
        "Max Distance (After)": safe(tram.get("max_distance"))
    })

df_detailed = pd.DataFrame(rows_detailed)

st.markdown("### 📊 Full Travel Stats by Mode")
st.dataframe(df_detailed.set_index("Mode").T, use_container_width=True)

# Load both result files
try:
    peak_stats = load_stats("transport_sim/results/tramline_stats_peak.json")
    offpeak_stats = load_stats("transport_sim/results/tramline_stats_offpeak.json")
except:
    st.error("❌ One or both result files missing. Please re-run the simulation.")
    st.stop()

# Build comparison summary table
rows = []
for mode in sorted(set(peak_stats["modes"]) | set(offpeak_stats["modes"])):
    peak = peak_stats["modes"].get(mode, {})
    off = offpeak_stats["modes"].get(mode, {})

    def safe(val): return round(val, 2) if isinstance(val, (int, float)) else "—"

    rows.append({
        "Mode": mode.title(),
        "Peak Avg (m)": safe(peak.get("avg_distance")),
        "Off-Peak Avg (m)": safe(off.get("avg_distance")),
        "Δ Avg (m)": safe(off.get("avg_distance") - peak.get("avg_distance"))             if isinstance(off.get("avg_distance"), (int, float)) and isinstance(peak.get("avg_distance"), (int, float)) else "—"
    })

df = pd.DataFrame(rows).set_index("Mode")

def highlight_delta(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return "background-color: lightgreen"
        elif val < 0:
            return "background-color: salmon"
    return ""

st.markdown("### 🔄 Peak vs Off-Peak Comparison (Avg Distance by Mode)")
st.dataframe(df.style.map(highlight_delta, subset=["Δ Avg (m)"]), use_container_width=True)

