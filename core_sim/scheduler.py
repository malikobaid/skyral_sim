class Scheduler:
    def __init__(self, agents):
        self.agents = agents

    def step(self, env):
        for agent in self.agents:
            if agent.status == "active":
                agent.step(env)
