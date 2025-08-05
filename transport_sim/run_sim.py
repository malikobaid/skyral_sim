import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.makedirs("transport_sim/results", exist_ok=True)
import networkx as nx
import json

from city_loader import load_city, get_hub_node, export_access_map
from simulation import load_config, apply_scenario, run_abm

config = load_config()

# Load base city graph and hub
G_base = load_city(config["city"])
hub = get_hub_node(G_base, config["hub"])
if hub not in G_base.nodes:
    raise ValueError("Hub node not in undirected graph.")

# Run baseline scenario
print("Running baseline...")
baseline_stats, baseline_agents = run_abm(G_base, hub, config["num_agents"])

# Copy base graph and apply tramline extension scenario
G_scenario = G_base.copy()
apply_scenario(G_scenario, config["scenarios"]["tramline_extension"])

print("Running tramline extension...")
tramline_stats, tramline_agents = run_abm(G_scenario, hub, config["num_agents"])

# Print stats
print("\n--- Simulation Results ---")
print("Baseline:", baseline_stats)
print("Tramline:", tramline_stats)
print("Δ Avg Distance:", baseline_stats['avg_distance'] - tramline_stats['avg_distance'])

# ✅ Export access map with distances from agents
# Baseline access map
baseline_distances = {
    a.home_node: a.total_distance
    for a in baseline_agents
    if a.status == 'active'
}
export_access_map(
    G_base,
    hub,
    baseline_distances,
    out_path="transport_sim/results/baseline_access.html"
)
print("✅ Saved baseline map to transport_sim/results/baseline_access.html")

# Tramline access map
tramline_distances = {
    a.home_node: a.total_distance
    for a in tramline_agents
    if a.status == 'active'
}
export_access_map(
    G_scenario,
    hub,
    tramline_distances,
    out_path="transport_sim/results/tramline_access_colored.html",
    tramline_nodes=config["scenarios"]["tramline_extension"]["add_edge"],
    tramline_names=config["tramline"]  # <- added
)
print("✅ Saved tramline map to transport_sim/results/tramline_access.html")


with open("transport_sim/results/baseline_stats.json", "w") as f:
    json.dump(baseline_stats, f)

with open("transport_sim/results/tramline_stats.json", "w") as f:
    json.dump(tramline_stats, f)