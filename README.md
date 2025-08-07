# Skyral Transport Simulation Demo

An interactive agent-based urban transport simulation developed as a technical demo for the Applied Scientist role at Skyral.

---

## 🚦 Project: Urban Mobility Scenario Explorer

Simulates tramline extension scenarios and evaluates accessibility changes across a transport network using OSM data and agent-based modeling.

- Shortest path calculations via NetworkX
- Map-based routing UI with Streamlit + Folium
- Accessibility metrics and travel time visualisations
- Local AI chatbot (LLM + RAG) to answer questions about the app, codebase, and AWS deployment  
- ⚙️ Tech: Python, OSMnx, NetworkX, Streamlit, LlamaIndex, Ollama

---

## 📂 Structure

```text
skyral_sim/
├── transport_sim/     # Urban mobility network simulation core logic
├── streamlit_app/     # Streamlit web UI and main pages
│   ├── Home.py        # Main landing page with intro and chatbot
│   └── pages/
│       ├── AgentSimulation.py
│       └── Results.py
├── project_docs/      # Documentation, diagrams, FAQs for chatbot/RAG
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
````

---

## 🚀 Quick Start

1. **Clone the repo:**
    ```bash
    git clone https://github.com/malikobaid/skyral_sim.git
    cd skyral_sim
    ```

2. **Set up virtual environment:**
    ```bash
    python3 -m venv venv-skyral
    source venv-skyral/bin/activate
    ```

3. **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

4. **(First time only) Install [Ollama](https://ollama.com/download) and run the LLM backend locally:**
    ```bash
    ollama run llama3
    ```
    > Or use another compatible local model if you wish.

5. **Start the Streamlit app:**
    ```bash
    streamlit run streamlit_app/Home.py
    ```

---

## 🛠️ Core Technologies

- **Python, Streamlit, Pandas, NetworkX**
- **LlamaIndex** (local RAG for chatbot)
- **Ollama** (local LLM inference server)
- **AWS** (EC2, S3, CloudFront, Route53, IAM)
- **GitHub Actions** (CI/CD)

---

## 📊 Example Use Cases

- Simulate adding new tram lines and see their impact on city accessibility.
- Compare before/after metrics for car, tram, and cycle travel.
- Ask the project AI bot questions like:
  - "Where is the agent-based logic implemented?"
  - "What AWS services does this project use?"
  - "How does the simulation decide agent travel routes?"

---

## 📫 Contact

**Obaid Malik**  
🌐 [obaidmalik.co.uk](https://obaidmalik.co.uk)  
🔗 [LinkedIn](https://linkedin.com/in/malikobaid1)  
✉️ malikobaid@gmail.com

---

## 👀 Notes

- This project is for demonstration and technical interview purposes only.
- All answers from the AI bot come from **local docs and code**—no OpenAI API needed.
- If you want to deploy on AWS or another cloud, see `project_docs/aws_architecture.md` for guidance.


