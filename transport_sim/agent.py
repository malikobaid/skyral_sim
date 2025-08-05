import networkx as nx
import random

class Agent:
    def __init__(self, id, home_node, graph, hub_node, mode='walk'):
        self.id = id
        self.home_node = home_node
        self.graph = graph
        self.hub_node = hub_node
        self.mode = mode
        self.route = []
        self.total_distance = 0
        self.status = 'active'

    def plan_route(self):
        try:
            self.route = nx.shortest_path(self.graph, self.home_node, self.hub_node, weight='length')
            self.total_distance = nx.shortest_path_length(self.graph, self.home_node, self.hub_node, weight='length')
        except:
            self.status = 'unreachable'
            self.route = []

    def switch_mode(self, new_mode):
        self.mode = new_mode
        self.plan_route()

    def step(self):
        # Could implement walking along route or just log final distance
        pass
