import json
import random
import networkx as nx
from transport_sim.agent import Agent


def load_config(path="transport_sim/config.json"):
    """Load simulation parameters from JSON config."""
    with open(path) as f:
        return json.load(f)


def apply_scenario(graph, scenario):
    """Apply scenario changes to the transport graph."""
    if "add_edge" in scenario:
        n1, n2 = scenario["add_edge"]
        length = scenario.get("length", 300)
        graph.add_edge(n1, n2, length=length)
        graph.add_edge(n2, n1, length=length)  # assume undirected


def run_abm(G, hub_node, num_agents=50):
    """Run agent-based transport simulation on graph G to a hub node."""

    if hub_node not in G:
        raise ValueError("Hub node is not in the graph.")

    # Use only nodes in the same connected component as the hub
    component = max(nx.connected_components(G), key=len)
    if hub_node not in component:
        raise ValueError("Hub node is not connected to largest component.")

    nodes = list(component)
    agents = [Agent(i, random.choice(nodes), G, hub_node) for i in range(num_agents)]

    for agent in agents:
        agent.plan_route()

    distances = [a.total_distance for a in agents if a.status == 'active']
    stats = {
        'total_agents': len(agents),
        'unreachable': sum(1 for a in agents if a.status == 'unreachable'),
        'avg_distance': sum(distances) / max(1, len(distances)),
        'min_distance': min(distances, default=0),
        'max_distance': max(distances, default=0)
    }

    return stats, agents
