import sys
import os
import json
import networkx as nx
from collections import defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.makedirs("transport_sim/results", exist_ok=True)

from city_loader import load_city, get_hub_node, export_access_map
from simulation import load_config, apply_scenario, run_abm, adjust_for_traffic

def group_stats_by_mode(agents):
    mode_stats = defaultdict(list)
    for a in agents:
        if a.status == "active":
            mode_stats[a.mode].append(a.total_distance)

    result = {}
    for mode, dists in mode_stats.items():
        if dists:
            result[mode] = {
                "avg": sum(dists) / len(dists),
                "max": max(dists),
                "count": len(dists)
            }
    return result

import sys
config_path = sys.argv[1] if len(sys.argv) > 1 else "transport_sim/config.json"
config = load_config(config_path)
traffic_level = config.get("traffic", "off-peak")
G_base = load_city(config["city"])
G_base = adjust_for_traffic(G_base, traffic_level)  # Apply congestion if needed

hub = get_hub_node(G_base, config["hub"])
if hub not in G_base.nodes:
    raise ValueError("Hub node not in undirected graph.")

print("Running baseline...")
# Baseline
baseline_stats, baseline_agents = run_abm(G_base, hub, config["num_agents"], config["agent_distribution"])

# Tramline
G_scenario = G_base.copy()
apply_scenario(G_scenario, config["scenarios"]["tramline_extension"])
n1_id, n2_id = apply_scenario(G_scenario, config["scenarios"]["tramline_extension"])
print(f"✅ Tramline edge added: {n1_id} ↔ {n2_id}")
print(f"🔗 Path exists to hub: {nx.has_path(G_scenario, n1_id, hub)}")

print("Running tramline extension...")
tramline_stats, tramline_agents = run_abm(G_scenario, hub, config["num_agents"], config["agent_distribution"])

baseline_stats["by_mode"] = group_stats_by_mode(baseline_agents)
tramline_stats["by_mode"] = group_stats_by_mode(tramline_agents)

baseline_distances = {
    a.home_node: a.total_distance
    for a in baseline_agents if a.status == 'active'
}

# --- Convert tram stop names to node IDs ---
from city_loader import tram_coords_lookup
import osmnx as ox

tram_stops = config["scenarios"]["tramline_extension"]["tram_stops"]
if isinstance(tram_stops[0], str):
    latlon1 = tram_coords_lookup.get(tram_stops[0])
    latlon2 = tram_coords_lookup.get(tram_stops[1])
    if latlon1 and latlon2:
        n1 = ox.distance.nearest_nodes(G_scenario, latlon1[1], latlon1[0])
        n2 = ox.distance.nearest_nodes(G_scenario, latlon2[1], latlon2[0])
        tramline_nodes = [n1, n2]
    else:
        raise ValueError("Tram stop names not found in lookup.")
else:
    tramline_nodes = tram_stops

export_access_map(
    G_base,
    hub,
    baseline_distances,
    out_path="transport_sim/results/baseline_access.html"
)
print("✅ Saved baseline map to transport_sim/results/baseline_access.html")

tramline_distances = {
    a.home_node: a.total_distance
    for a in tramline_agents if a.status == 'active'
}
export_access_map(
    G_scenario,
    hub,
    tramline_distances,
    out_path="transport_sim/results/tramline_access_colored.html",
    tramline_nodes=tramline_nodes,
    tramline_names=config["tramline"]
)
print("✅ Saved tramline map to transport_sim/results/tramline_access_colored.html")

suffix = traffic_level.replace("-", "").lower()  # "offpeak" or "peak"

with open(f"transport_sim/results/baseline_stats_{suffix}.json", "w") as f:
    json.dump(baseline_stats, f)

with open(f"transport_sim/results/tramline_stats_{suffix}.json", "w") as f:
    json.dump(tramline_stats, f)