# Project Code Structure

This document describes the main files and folders in the Skyral Transport Simulation project, explaining what each part does and how they connect.

---

## Root Directory (`skyral_sim/`)

skyral_sim/
│
├── project_docs/
│ ├── aws_architecture.md
│ ├── faq.md
│ ├── features_and_usage.md
│ ├── job_description.txt
│ ├── Obaid_Malik_CV_Skyral.pdf
│ └── README.md
│
├── streamlit_app/
│ ├── .streamlit/
│ │ └── config.toml
│ ├── pages/
│ │ ├── AgentSimulation.py
│ │ ├── Chatbot.py
│ │ └── Results.py
│ ├── backend_runner.py
│ ├── Overview.py
│ └── utils.py
│
├── transport_sim/
│ ├── results/
│ │ └── (simulation results and data)
│ ├── agent.py
│ ├── bournemouth_graph.png
│ ├── city_loader.py
│ ├── config.json
│ ├── config_off-peak.json
│ ├── config_peak.json
│ ├── run_sim.py
│ ├── simulation.py
│ └── travel_time_map.html
│
├── requirements.txt
└── README.md



---

## Explanation of Major Folders and Files

### `project_docs/`
- **Project documentation** for users and the chatbot to answer questions about the app.
    - `aws_architecture.md`: AWS deployment and architecture details.
    - `faq.md`: Frequently asked questions.
    - `features_and_usage.md`: What the app does, limitations, how to use it.
    - `job_description.txt`: The job ad or challenge this project responds to.
    - `Obaid_Malik_CV_Skyral.pdf`: Author’s CV for context.
    - `README.md`: Project summary and instructions.

---

### `streamlit_app/`
- **The main Streamlit web application.**

    - `.streamlit/config.toml`: App configuration.
    - `Home.py`: The home/landing page (placed outside `pages/` to avoid duplicate menu entries).
    - `pages/`: Contains main app feature pages:
        - `AgentSimulation.py`: User interface for setting up and running new simulation scenarios.
        - `Results.py`: UI for displaying simulation results, tables, and plots.
    - `backend_runner.py`: Handles backend logic, task running, or integration for simulations.
    - `utils.py`: General utility functions shared across the app.

---

### `transport_sim/`
- **Simulation engine and core logic for the transport model.**
    - `agent.py`: Defines how each simulated agent (person/traveler) behaves.
    - `simulation.py`: Core simulation logic (how scenarios are run).
    - `run_sim.py`: Main entry point to start a simulation.
    - `city_loader.py`: Loads and processes city or network data.
    - `config.json`, `config_off-peak.json`, `config_peak.json`: Configuration files for different simulation scenarios.
    - `bournemouth_graph.png`: Visualization of the city or transport network.
    - `travel_time_map.html`: Interactive HTML map showing simulation results.
    - `results/`: Stores output data and simulation results.

---

### `requirements.txt`
- Lists all Python packages needed to run the project.

---

### `README.md` (at root)
- High-level summary and instructions for the whole project.

---

## How It All Connects

- The **Streamlit app** (`streamlit_app/`) provides the user interface and calls functions from the **simulation engine** (`transport_sim/`) to run new scenarios.
- Simulation results and config files live in `transport_sim/` and are loaded/displayed in the app.
- Documentation and context for the chatbot and users are kept in `project_docs/`.
- Helper files like `backend_runner.py` and `utils.py` keep business logic organized outside of UI code.
- App configuration, secrets, and environment settings live in `.streamlit/`.

---

*This file is included so the chatbot can answer questions about where to find specific features, how the app is organized, and what each part does.*
