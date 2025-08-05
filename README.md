# Skyral Simulation Demos

A set of interactive simulation prototypes developed in support of my application for the Applied Scientist role at Skyral.

## 🔍 Projects

### 1. Urban Mobility Scenario Explorer
Simulates tramline extension scenarios and evaluates accessibility changes across a transport network using OSM data.

- Shortest path algorithms via NetworkX
- Map-based routing UI with Streamlit + Folium
- Accessibility metrics and time-based visualisations
- ⚙️ Tech: Python, OSMnx, NetworkX, Streamlit

### 2. Crowd Evacuation Simulation (WIP)
Agent-based simulation of crowd dynamics under different environmental layouts. Visualised as animated GIFs for scenario comparisons.

- ABM logic using simple rule-based agents
- Supports entry/exit points, obstacles, and randomised runs
- ⚙️ Tech: Python, Matplotlib, NumPy

---

## 📂 Structure

```
skyral_sim/
├── transport_sim/           # Urban mobility network simulation
├── crowd_sim/               # Crowd evacuation ABM
├── streamlit_app/           # Streamlit UI for demos
├── core_sim/                # Shared functions/utilities
├── cleanup.py               # Cleanup script
├── README.md
└── requirements.txt
```

## 🚀 Quick Start

```bash
# Clone repo
git clone https://github.com/malikobaid/skyral_sim.git
cd skyral_sim

# Create environment and install
python3 -m venv venv-skyral
source venv-skyral/bin/activate
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app/Home.py
```

## 📫 Contact

Obaid Malik  
🌐 [obaidmalik.co.uk](https://obaidmalik.co.uk)  
🔗 [LinkedIn](https://linkedin.com/in/malikobaid1)  
✉️ malikobaid@gmail.com
