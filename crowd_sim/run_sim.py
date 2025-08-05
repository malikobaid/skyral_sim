from core_sim.agent import Agent
from core_sim.environment import Environment
from core_sim.scheduler import Scheduler


def run_simulation(grid_size=(10, 10), num_agents=5, steps=15):
    env = Environment(grid_size)

    # Place agents at center (for now)
    start_pos = (grid_size[0] // 2, grid_size[1] // 2)
    agents = [Agent(i, start_pos) for i in range(num_agents)]

    scheduler = Scheduler(agents)

    print("Initial positions:")
    for a in agents:
        print(f"Agent {a.id} at {a.position}")

    for t in range(steps):
        scheduler.step(env)
        print(f"After step {t + 1}:")
        for a in agents:
            print(f"Agent {a.id}: pos={a.position}, status={a.status}")

    return agents


if __name__ == "__main__":
    run_simulation()
