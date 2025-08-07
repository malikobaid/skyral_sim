# Skyral Transport Simulation Demo

## Overview

This project is a working demo for the Skyral Applied Scientist (Transport Modelling) role. It lets you simulate how introducing new tramlines (or other transport changes) could affect accessibility and agent travel choices in a city. The project is meant to show hands-on skills in agent-based simulation, cloud deployment, data engineering, and technical communication.

---

## Key Features

- Modular, agent-based transport scenario simulation
- Simple UI to select tramlines and adjust agent parameters
- Compare travel accessibility before and after new infrastructure
- Results breakdown by mode: car, cycle, tram
- Floating chatbot that can answer questions about the project, AWS setup, and technical details
- Deployed on AWS using S3, CloudFront, Route 53, EC2, and CI/CD

---

## Usage

1. **Home:** Read a quick summary of the problem and approach.
2. **Agent Simulation:** Select tramline points and agent types; configure simulation details.
3. **Run Simulation:** See progress and wait for results to calculate.
4. **Results:** View a table and plots comparing travel times and accessibility by agent mode, before and after tramline changes.
5. **Chatbot:** Use the chatbot in the lower corner to ask anything about the app, setup, or project files.

---

## Technical Stack

- **Frontend:** Streamlit
- **Backend:** Python (agent simulation, logic, RAG-powered chatbot)
- **LLM:** Local model via Ollama (planned)
- **Cloud:** AWS (S3, CloudFront, Route 53, EC2, Certificate Manager, IAM, CloudWatch)
- **CI/CD:** GitHub Actions

---

## About This Demo

This demo is a technical proof-of-concept, not a commercial tool.  
Some features (like the LLM chatbot and realistic traffic data integration) are designed to show technical breadth and can be extended for production use.  
Assumptions and simplifications are detailed in `features_and_usage.md`.

---

## Author

Obaid Malik  
[LinkedIn](https://www.linkedin.com/in/malikobaid1/) | [GitHub](https://github.com/malikobaid)

---

