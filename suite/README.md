# ***This directory is the sandbox for developing the [SFM Suite](./SFMSuiteDesignProposal.md).*** #
# Foundation of the experimental SFM system: data models, storage architecture, APIs, initial functionality, and install instructions.

### **1. Core Architecture Overview**
We need a modular and scalable structure that allows:
- **Entity Management**: Define policies, regulations, institutions, technologies, and social beliefs.
- **Relationship Mapping**: Capture interconnections between entities and their influences.
- **Graph Analysis**: Compute reachability, centrality, and feedback loops.
- **Simulation Tools**: Model policy impact and ROI scenarios.
- **Visualization & APIs**: Provide accessible UI and external integrations.

We'll use **Python** for the backend with **FastAPI** for RESTful APIs, **NetworkX or Neo4j** for graph storage, and **D3.js or PyVis** for visualization.

---

### **2. Core Service Setup (Python - FastAPI)**
#### Install Dependencies:
```bash
pip install fastapi uvicorn networkx neo4j matplotlib pyvis
```

#### Define Core Models (`models.py`):
```python
from pydantic import BaseModel
from typing import Optional, Dict

class SFMEntity(BaseModel):
    id: str
    name: str
    category: str
    properties: Optional[Dict] = {}

class SFMRelationship(BaseModel):
    id: str
    source_id: str
    target_id: str
    description: str
    weight: Optional[float] = None
```

---

### **3. Graph Storage & Operations**
Using **NetworkX** or **Neo4j**.

#### Initialize Graph (`graph-service.py`):
```python
import networkx as nx

class SFMGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_entity(self, entity):
        self.graph.add_node(entity.id, **entity.dict())

    def add_relationship(self, relationship):
        self.graph.add_edge(relationship.source_id, relationship.target_id, **relationship.dict())

    def visualize(self):
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, font_size=10)
        plt.show()
```

---

### **4. API Endpoints (`api.py`)**
#### FastAPI Service:
```python
from fastapi import FastAPI
from .models import SFMEntity, SFMRelationship
from .graph_service import SFMGraph

app = FastAPI()
sfm_graph = SFMGraph()

@app.post("/entity/")
def add_entity(entity: SFMEntity):
    sfm_graph.add_entity(entity)
    return {"message": "Entity added"}

@app.post("/relationship/")
def add_relationship(rel: SFMRelationship):
    sfm_graph.add_relationship(rel)
    return {"message": "Relationship added"}

@app.get("/visualize/")
def visualize():
    sfm_graph.visualize()
    return {"message": "Graph visualization rendered"}
```

Run the service:
```bash
uvicorn api:app --reload
```

---

### **5. TODO**
- **Database Integration**: Store entities/relationships in **Neo4j**.
- **Graph Analysis**: Implement reachability & feedback loop detection.
- **UI & Dashboard**: Build **React/D3.js** front-end for visualization.
- **Simulation Framework**: Add policy impact modeling.
