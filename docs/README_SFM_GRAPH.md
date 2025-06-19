# ***This directory is the sandbox for developing the [SFM Graph Service](docs/SFMSuiteDesignProposal.md).*** #
# Foundation of the experimental SFM system.


## Install and Run

Install the dependencies
```bash
pip install fastapi uvicorn networkx neo4j matplotlib pyvis neo4j
```

Run the service (from the top level directory):
```bash
uvicorn sfmgraph.api:app --reload
```

---
## Technical Roadmap
Document future enhancements, such as AI-driven impact analysis, integration with enterprise data sources, and iterative improvements to the simulation engine.

### Extending the Prototype
To build a production-ready suite of software tools and services implementing the SFM framework, consider the following:

- Graph Databases:
Migrate from in-memory NetworkX to a scalable graph database like Neo4j or TigerGraph for real-time querying and large datasets.
API Layer: Develop REST or GraphQL APIs in frameworks like FastAPI or Node.js for external integrations.
Advanced Analysis & Machine Learning:

- Simulation Engines:
Integrate machine learning frameworks (e.g., TensorFlow, PyTorch) to simulate policy impacts based on historical data.
ROI Calculators: Design robust algorithms to calculate the return on investment (ROI) for policy changes.
User Interface & Visualization:

- Interactive Dashboards:
Use rich front-end libraries like React with D3.js or Cytoscape.js to make dynamics, interactive network graphs accessible to policymakers.
Collaboration Tools: Build multi-user environments that allow departmental collaboration, annotation, and commenting on the graph model.

- Modularity & Microservices:
Architecture: Consider a microservices approach where different modules (data ingestion, simulation, visualization) are decoupled for flexibility and independent scaling.
Security & Compliance: Ensure that the solution follows data security guidelines (e.g., GDPR, HIPAA) if handling sensitive institutional data.

### ***TODO**
- **Graph Analysis**: Implement reachability & feedback loop detection.
- **UI & Dashboard**: Build **React/D3.js** front-end for visualization.
- **Simulation Framework**: Add policy impact modeling.
