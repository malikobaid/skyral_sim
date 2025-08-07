# Features and Usage

---

## 1. Problem Addressed

The Skyral Transport Simulation demo addresses the **challenge of evaluating how new transport infrastructure (such as a tram line) would impact accessibility and travel behavior in a real city**.  
Most UK cities have limited tools for simulating multiple transport modes (driving, cycling, trams) with agent-based models that are easy to configure and visualize for rapid scenario testing. This demo provides a starting point for exploring such impacts, helping planners and stakeholders make more informed decisions.

---

## 2. Why This Problem (Even If The Demo Isn’t a Full Product)

- **Relevance:** Urban transport planning is a critical part of smart city development, and agent-based simulation is becoming a core technique for scenario analysis.
- **Demonstration of Skills:** Even though this demo is not a full production-grade system, it demonstrates a practical approach to building, deploying, and integrating simulation, interactive visualization, and modern MLOps tools (including LLM-powered Q&A) using open-source technologies and AWS.
- **Communication:** The project is meant to communicate how technical ideas, data, and constraints come together to inform real-world decisions—crucial for roles that blend data science, engineering, and urban systems.

---

## 3. Assumptions Made for Simplicity

- The city area and agent population are simplified (e.g., reduced to a few zones and agents for performance and demo clarity).
- Only a limited set of transport modes are modeled: drive, cycle, tram.
- The tramline is user-selected and does not account for engineering or planning constraints.
- Agents’ route choice and behavior are basic and not calibrated with real-world travel survey data.
- Traffic conditions and rush hour effects are not dynamically simulated—agents have static travel speeds.
- Only summary results are shown; detailed agent paths, congestion, or real-time maps are not provided.
- The building energy, comfort, or environmental impact is out of scope for this demo.

---

## 4. How These Assumptions Would Be Addressed in a Real Application

In a real application, you’d use real city maps and up-to-date travel data for accurate routes and destinations. Agent behavior would be modeled using travel surveys or mobile data—so, for example, agents might choose the fastest or least congested route based on live or historic traffic data. You could integrate with real traffic APIs or plugins (like Google Maps API or open-source transport data packages) to simulate delays, congestion, or events. Tram routes would be designed with real engineering and budget constraints. The visuals and analytics would be more advanced, showing detailed feedback on how infrastructure changes affect actual journeys.


---

## 5. Limitations of the App

- Not a fully validated or production-grade transport model.
- Agents’ decisions and outcomes are synthetic and may not match real-world behavior.
- UI/UX is optimized for a technical demo, not end-user adoption.
- No live data ingestion or city data integration in this version.
- The simulation scale and realism are intentionally constrained for performance and clarity.
- LLM chatbot answers only from supplied docs and cannot give true expert advice about urban planning or infrastructure.

---

## 6. How This App Can Be Improved

The app could be improved by integrating real-time or historic traffic data plugins, so agents react to actual road conditions or typical rush hour patterns. Agents could have personal schedules and habits, using data-driven preferences to make decisions. Better charts and maps, a more user-friendly interface, support for larger simulations, and clearer scenario comparisons would all make the app more useful for real-world planning.

---

## 7. How to Use

1. **Overview:** Start from the main page for project introduction and context.
2. **Configure Simulation:** Use the Agent Simulation page to select tramline points, set agent counts, and transport types.
3. **Run Simulation:** Launch the scenario—inputs are disabled and a progress popup appears while it runs.
4. **Review Results:** Use the Results page to view before/after metrics, agent mode breakdowns, and summary tables.
5. **Ask Questions:** Use the floating chatbot to get help about the app’s usage, features, codebase, or deployment.

---

*For further improvements, feedback is welcomed!*
