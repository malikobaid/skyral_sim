import os
import sys
import matplotlib.pyplot as plt
import imageio

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core_sim.agent import Agent
from core_sim.environment import Environment
from core_sim.scheduler import Scheduler

def render_grid(grid_size, agents, step_num, out_dir):
    fig, ax = plt.subplots()
    ax.set_xlim(0, grid_size[0])
    ax.set_ylim(0, grid_size[1])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Step {step_num}")

    # Plot agents
    for agent in agents:
        x, y = agent.position
        color = 'green' if agent.status == "evacuated" else 'red'
        ax.plot(x + 0.5, y + 0.5, 'o', color=color)

    # Save image
    frame_path = os.path.join(out_dir, f"frame_{step_num:03}.png")
    plt.savefig(frame_path)
    plt.close()
    return frame_path

def run_and_generate_gif(grid_size=(10, 10), num_agents=5, steps=15, gif_name="evacuation.gif"):
    env = Environment(grid_size)
    start_pos = (grid_size[0] // 2, grid_size[1] // 2)
    agents = [Agent(i, start_pos) for i in range(num_agents)]
    scheduler = Scheduler(agents)

    os.makedirs("frames", exist_ok=True)
    frames = []

    for t in range(steps):
        scheduler.step(env)
        frame_path = render_grid(grid_size, agents, t, "frames")
        frames.append(imageio.imread(frame_path))

    imageio.mimsave(gif_name, frames, duration=0.5)
    print(f"Saved GIF: {gif_name}")

    # Clean up frames
    for f in os.listdir("frames"):
        os.remove(os.path.join("frames", f))
    os.rmdir("frames")

if __name__ == "__main__":
    run_and_generate_gif()
