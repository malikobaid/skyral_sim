import json
import random
import networkx as nx
from transport_sim.agent import Agent
from transport_sim.city_loader import tram_coords_lookup
from collections import defaultdict
import osmnx as ox

def compute_stats(agents):
    stats = {
        "total_agents": len(agents),
        "unreachable": 0,
        "avg_distance": 0,
        "min_distance": float("inf"),
        "max_distance": 0,
        "modes": defaultdict(lambda: {
            "count": 0,
            "reachable_count": 0,
            "unreachable": 0,
            "total_distance": 0,
            "min_distance": float("inf"),
            "max_distance": 0,
            "avg_distance": None
        })
    }

    total_reachable = 0

    for agent in agents:
        mode = agent.mode
        mode_stats = stats["modes"][mode]
        mode_stats["count"] += 1

        if agent.status == 'unreachable':
            stats["unreachable"] += 1
            mode_stats["unreachable"] += 1
            continue

        # Reachable agent
        dist = agent.total_distance
        stats["avg_distance"] += dist
        stats["min_distance"] = min(stats["min_distance"], dist)
        stats["max_distance"] = max(stats["max_distance"], dist)
        total_reachable += 1

        mode_stats["reachable_count"] += 1
        mode_stats["total_distance"] += dist
        mode_stats["min_distance"] = min(mode_stats["min_distance"], dist)
        mode_stats["max_distance"] = max(mode_stats["max_distance"], dist)

    # Final averages
    if total_reachable > 0:
        stats["avg_distance"] /= total_reachable
    else:
        stats["avg_distance"] = None
        stats["min_distance"] = None
        stats["max_distance"] = None

    for mode, m in stats["modes"].items():
        if m["reachable_count"] > 0:
            m["avg_distance"] = m["total_distance"] / m["reachable_count"]
        else:
            m["avg_distance"] = None
            m["min_distance"] = None
            m["max_distance"] = None

    return stats



def load_config(path="transport_sim/config.json"):
    """Load simulation parameters from JSON config."""
    with open(path) as f:
        return json.load(f)


# def apply_scenario(graph, scenario):
#     if "add_edge" in scenario:
#         n1, n2 = scenario["add_edge"]
#         length = scenario.get("length", 300)
#
#         if isinstance(n1, str) and isinstance(n2, str):
#             if n1 in tram_coords_lookup and n2 in tram_coords_lookup:
#                 lat1, lon1 = tram_coords_lookup[n1]
#                 lat2, lon2 = tram_coords_lookup[n2]
#                 n1_id = ox.distance.nearest_nodes(graph, lon1, lat1)
#                 n2_id = ox.distance.nearest_nodes(graph, lon2, lat2)
#
#                 graph.add_edge(n1_id, n2_id, length=1, tram=True)
#                 graph.add_edge(n2_id, n1_id, length=1, tram=True)
#
#                 return (n1_id, n2_id)  # ✅ Add this
#     return None, None

def apply_scenario(graph, scenario):
    stops = scenario.get("tram_stops", [])
    length = scenario.get("length", 300)

    if not stops or len(stops) < 2:
        return None, None

    for i in range(len(stops) - 1):
        s1, s2 = stops[i], stops[i+1]

        if s1 in tram_coords_lookup and s2 in tram_coords_lookup:
            lat1, lon1 = tram_coords_lookup[s1]
            lat2, lon2 = tram_coords_lookup[s2]
            n1 = ox.distance.nearest_nodes(graph, lon1, lat1)
            n2 = ox.distance.nearest_nodes(graph, lon2, lat2)

            graph.add_edge(n1, n2, length=length, tram=True)
            graph.add_edge(n2, n1, length=length, tram=True)

    return None, None


def run_abm(graph, hub, num_agents, agent_distribution):
    agents = []

    mode_choices = ["drive", "cycle", "walk", "tram"]
    mode_weights = [
        agent_distribution.get("drive", 0),
        agent_distribution.get("cycle", 0),
        agent_distribution.get("walk", 0),
        agent_distribution.get("tram", 0),
    ]

    # Normalize weights (in case they don’t sum to 100)
    total = sum(mode_weights)
    if total == 0:
        raise ValueError("Agent distribution weights cannot all be zero.")
    mode_weights = [w / total for w in mode_weights]

    # Try to get real node IDs for tram stops
    tram_nodes = []
    if "Bournemouth Pier" in tram_coords_lookup and "Lansdowne" in tram_coords_lookup:
        lat1, lon1 = tram_coords_lookup["Bournemouth Pier"]
        lat2, lon2 = tram_coords_lookup["Lansdowne"]
        try:
            n1 = ox.distance.nearest_nodes(graph, lon1, lat1)
            n2 = ox.distance.nearest_nodes(graph, lon2, lat2)
            tram_nodes = [n1, n2]
        except Exception as e:
            print("⚠️ Could not resolve tram stop nodes:", e)

    for i in range(num_agents):
        mode = random.choices(mode_choices, weights=mode_weights, k=1)[0]

        if mode == "tram" and tram_nodes:
            # Spawn tram agents on or near tramline stops
            home_node = random.choice(tram_nodes)
        else:
            home_node = random.choice(list(graph.nodes))

        agent = Agent(
            id=i,
            home_node=home_node,
            graph=graph,
            hub_node=hub,
            mode=mode
        )
        agent.plan_route()
        agents.append(agent)

    return compute_stats(agents), agents


def adjust_for_traffic(G, traffic_level):
    if traffic_level == "rush hour":
        for u, v, data in G.edges(data=True):
            if "highway" in data.get("tags", {}):  # optional check
                data["length"] *= 1.5  # roads become "longer" (slower)
    return G