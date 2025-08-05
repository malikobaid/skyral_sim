class Agent:
    def __init__(self, agent_id, position):
        self.id = agent_id
        self.position = position  # (x, y)
        self.status = "active"

    def step(self, env):
        x, y = self.position
        # Naive logic: move towards nearest exit (e.g., left/up/right/down)
        possible_moves = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        for new_x, new_y in possible_moves:
            if env.is_within_bounds(new_x, new_y):
                self.position = (new_x, new_y)
                if env.is_exit(new_x, new_y):
                    self.status = "evacuated"
                break
