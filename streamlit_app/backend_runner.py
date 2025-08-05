# streamlit_app/backend_runner.py

def run_simulation(tramline_nodes, num_agents):
    import json
    import subprocess

    # Load current config
    with open("transport_sim/config.json") as f:
        config = json.load(f)

    # Update tramline edge and number of agents
    config["scenarios"]["tramline_extension"]["add_edge"] = tramline_nodes
    config["num_agents"] = num_agents

    # Save updated config
    with open("transport_sim/config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Call the simulation script
    subprocess.run(["python", "transport_sim/run_sim.py"], check=True)
