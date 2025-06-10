# sfmToolkit
SFM Toolkit: A Prototype for Implementing the [Social Fabric Matrix Framework](./sfm-overview.md). 

# Overview
This was intended to be used for a grad school project, but ended up as a precursor to the [SFM Suite](./suite/README.md) I am experimenting with. The code example, [sfm-toolkit.py](./sfm-toolkit.py) demonstrates:

- Defining the core data entities: An SFEntity (to represent policies, regulations, etc.) and a Relationship (to connect these entities).

- Building a graph model: Using NetworkX to store and analyze the interconnected relationships.

- Visualization: Rendering a simple diagram with matplotlib to illustrate the matrix of relationships.

- A starting point for simulations: A placeholder function to simulate policy impact changes. 

The included pytyon file is a starting point designed to demonstrate three core capabilities of the SFM framework:

- Mapping Entities and Relationships: By defining abstract classes for SFEntity and Relationship, you can represent any component of an organization’s policy or institutional ecosystem. Relationships are captured as directed edges with associated properties (like "compliesWith" or "supports") and weights that quantify influence.

- Graph-Based Analysis & Visualization: Using NetworkX, the system builds a directed graph where nodes represent entities and edges represent quantified relationships. Visualization (via matplotlib) aids in understanding the network structure visually.

- Simulation of Policy Changes: The simulate_policy_change() function provides a placeholder to adjust relationship weights. You can enhance this function with more sophisticated algorithms that reflect real-world impacts, ROI analysis, or predictive modeling.

Further Documentation
Setup Instructions:

# SFM Toolkit Prototype

**Requirements**
- Python 3.8+
- networkx
- matplotlib

**Installation**
```bash
pip install networkx matplotlib
```
Running the Prototype:
```
python sfm-toolkit.py
```
