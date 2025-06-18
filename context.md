Below is a clean, self-contained Python “schema file” that you can drop into `sfm_schema.py` (or any module name you prefer). It captures the canonical Social Fabric Matrix (SFM) concepts described by F. Gregory Hayden—entities, relationships, dimensional metadata, and enumerations for value categories, institutional layers, and flow types.

```python
# sfm_schema.py
# Core data structures for modeling an F. Gregory Hayden Social Fabric Matrix (SFM)

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional


# ───────────────────────────────────────────────
# 1. ENUMERATIONS  (shared controlled vocabularies)
# ───────────────────────────────────────────────

class ValueCategory(Enum):
    ECONOMIC = auto()        # Market-priced goods, services, financial returns
    SOCIAL = auto()          # Distributional equity, social cohesion, well-being
    ENVIRONMENTAL = auto()   # Resource stocks, ecological integrity
    CULTURAL = auto()        # Norms, beliefs, heritage
    INSTITUTIONAL = auto()   # Governance quality, rule consistency
    TECHNOLOGICAL = auto()   # Knowledge base, production techniques


class InstitutionLayer(Enum):
    FORMAL_RULE = auto()     # Constitutions, statutes, property law
    ORGANIZATION = auto()    # Firms, ministries, NGOs, unions
    INFORMAL_NORM = auto()   # Customs, habits, social expectations


class ResourceType(Enum):
    NATURAL = auto()         # Land, water, raw minerals
    PRODUCED = auto()        # Machinery, infrastructures
    HUMAN = auto()           # Labor, human capital, skills
    INFORMATION = auto()     # Data, R&D findings, patents


class FlowNature(Enum):
    INPUT = auto()           # Resource or value entering a process
    OUTPUT = auto()          # Product, waste, or value leaving a process
    TRANSFER = auto()        # Exchange between actors without transformation


class RelationshipKind(Enum):
    GOVERNS = auto()         # Institution/actor exerts authority or sets rules
    USES = auto()            # Actor/process employs a resource or technology
    PRODUCES = auto()        # Process generates an output flow
    EXCHANGES_WITH = auto()  # Actor-to-actor transfer
    LOCATED_IN = auto()      # Spatial anchoring
    OCCURS_DURING = auto()   # Temporal anchoring


# ───────────────────────────────────────────────
# 2. DIMENSIONAL “META” ENTITIES
# ───────────────────────────────────────────────

@dataclass(frozen=True)
class TimeSlice:
    """Discrete period for snapshot-style SFM accounting (e.g., fiscal year, quarter)."""
    label: str                    # e.g. "FY2025" or "Q1-2030"


@dataclass(frozen=True)
class SpatialUnit:
    """Hierarchical spatial identifier (nation, state, metro, census tract, etc.)."""
    code: str                     # e.g. "US-WA-SEATTLE"
    name: str                     # human-friendly display


@dataclass(frozen=True)
class Scenario:
    """Counterfactual or policy-design scenario name (baseline, carbon tax, UBI...)."""
    label: str


# ───────────────────────────────────────────────
# 3. CORE NODES (ACTORS, PROCESSES, RESOURCES…)
#    All inherit from a minimal “Node” base
# ───────────────────────────────────────────────

@dataclass
class Node:
    """Generic graph node with a UUID primary key and free-form metadata."""
    label: str
    description: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    meta: Dict[str, str] = field(default_factory=dict)


@dataclass
class Actor(Node):
    """Individuals, firms, agencies, communities."""
    legal_form: Optional[str] = None       # e.g. "Corporation", "Household"
    sector: Optional[str] = None           # NAICS or custom taxonomy


@dataclass
class Institution(Node):
    """Rules-in-use, organizations, or informal norms (Hayden’s three layers)."""
    layer: InstitutionLayer = InstitutionLayer.FORMAL_RULE


@dataclass
class Resource(Node):
    """Stock or asset available for use or transformation."""
    rtype: ResourceType = ResourceType.NATURAL
    unit: Optional[str] = None             # e.g. "tonnes", "person-hours"


@dataclass
class Process(Node):
    """Transformation activity that converts inputs to outputs (production, consumption, disposal)."""
    technology: Optional[str] = None       # e.g. "EAF-Steel-2024"
    responsible_actor_id: Optional[str] = None  # Actor that controls the process


@dataclass
class Flow(Node):
    """Edge-like node representing an actual quantified transfer of resources or value."""
    nature: FlowNature = FlowNature.TRANSFER
    quantity: Optional[float] = None
    unit: Optional[str] = None
    time: Optional[TimeSlice] = None
    space: Optional[SpatialUnit] = None
    scenario: Optional[Scenario] = None


# ───────────────────────────────────────────────
# 4. EXPLICIT RELATIONSHIP OBJECT
#    (Keeps multiplicity, weight, and dimension tags)
# ───────────────────────────────────────────────

@dataclass
class Relationship:
    """Typed edge connecting two nodes in the SFM graph."""
    source_id: str
    target_id: str
    kind: RelationshipKind
    weight: Optional[float] = None         # e.g. $-value, mass, influence score
    time: Optional[TimeSlice] = None
    space: Optional[SpatialUnit] = None
    scenario: Optional[Scenario] = None
    meta: Dict[str, str] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


# ───────────────────────────────────────────────
# 5. CONVENIENCE “GRAPH” AGGREGATE
# ───────────────────────────────────────────────

@dataclass
class SFMGraph:
    """In-memory container for nodes + relationships; can later sync to Neo4j, RDF, etc."""
    actors: Dict[str, Actor] = field(default_factory=dict)
    institutions: Dict[str, Institution] = field(default_factory=dict)
    resources: Dict[str, Resource] = field(default_factory=dict)
    processes: Dict[str, Process] = field(default_factory=dict)
    flows: Dict[str, Flow] = field(default_factory=dict)
    relationships: Dict[str, Relationship] = field(default_factory=dict)

    # ————— CRUD helpers —————
    def add_node(self, node: Node) -> None:
        if isinstance(node, Actor):          self.actors[node.id] = node
        elif isinstance(node, Institution):  self.institutions[node.id] = node
        elif isinstance(node, Resource):     self.resources[node.id] = node
        elif isinstance(node, Process):      self.processes[node.id] = node
        elif isinstance(node, Flow):         self.flows[node.id] = node
        else: raise TypeError(f"Unsupported node type: {type(node)}")

    def add_relationship(self, rel: Relationship) -> None:
        self.relationships[rel.id] = rel

    # Example query: all flows produced by a given process
    def outputs_of_process(self, process_id: str) -> List[Flow]:
        outs: List[Flow] = []
        for rel in self.relationships.values():
            if rel.kind == RelationshipKind.PRODUCES and rel.source_id == process_id:
                out_flow = self.flows.get(rel.target_id)
                if out_flow: outs.append(out_flow)
        return outs
```

### How the pieces map to Hayden’s SFM language
1. Nodes  
   • **Actor** ≈ decision-making entity (household, firm, agency).  
   • **Institution** covers three nested layers (formal rules, organizations, informal norms).  
   • **Resource** is a stock (land, labor, capital, knowledge).  
   • **Process** is the techno-economic activity that transforms inputs into outputs.  
   • **Flow** is the quantified linkage used to populate the actual matrix cells (money, material, influence, etc.).

2. Dimensional Attachments  
   TimeSlice, SpatialUnit, and Scenario can be optionally attached to either Flows or Relationships, letting you slice the full matrix by period, region, or policy counterfactual without duplicating the core topology.

3. RelationshipKind enumerates the canonical edge semantics Hayden lists in his writing: governance, usage, production, exchange, spatial anchoring, and temporal anchoring.

Feel free to adapt the naming conventions, add attributes (e.g., `price`, `currency`, ESG tags), or plug these dataclasses directly into a Neo4j Object-Graph Mapper (OGM) like `neomodel`.