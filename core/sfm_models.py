# sfm_schema.py
# Core data structures for modeling an F. Gregory Hayden Social Fabric Matrix (SFM)

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any
from datetime import datetime
from core.enums import (
    InstitutionLayer, RelationshipKind, ResourceType, FlowNature,ValueCategory)


# ───────────────────────────────────────────────
# DIMENSIONAL “META” ENTITIES
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
# CORE NODES (ACTORS, PROCESSES, RESOURCES…)
# All inherit from a minimal “Node” base
# ───────────────────────────────────────────────

@dataclass
class Node:
    """Generic graph node with a UUID primary key and free-form metadata."""
    label: str
    description: Optional[str] = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    meta: Dict[str, str] = field(default_factory=dict)
    
    def __iter__(self):
        """Iterator that yields (attribute_name, attribute_value) pairs."""
        for attr_name, attr_value in self.__dict__.items():
            yield attr_name, attr_value


@dataclass
class Actor(Node):
    """Individuals, firms, agencies, communities."""
    legal_form: Optional[str] = None       # e.g. "Corporation", "Household"
    sector: Optional[str] = None           # NAICS or custom taxonomy


@dataclass
class Institution(Node):
    """Rules-in-use, organizations, or informal norms (Hayden’s three layers)."""
    layer: Optional[InstitutionLayer] = None

@dataclass
class Policy(Institution):
    """Specific policy intervention or regulatory framework."""
    authority: Optional[str] = None    # Implementing body
    enforcement: Optional[float] = 0.0  # Strength of enforcement (0-1)
    target_sectors: List[str] = field(default_factory=list)
    
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

@dataclass
class BeliefSystem(Node):
    """Cultural myths, ideology or worldview that guides decision-making."""
    strength: Optional[float] = None  # Cultural embeddedness (0-1)
    domain: Optional[str] = None      # Area of society where belief operates

@dataclass
class FeedbackLoop(Node):
    """Represents a feedback loop in the Social Fabric Matrix."""
    relationships: List[uuid.UUID] = field(default_factory=list)
    description: Optional[str] = None
    polarity: Optional[str] = None  # "reinforcing" or "balancing"
    strength: Optional[float] = None  # Measure of loop strength/impact
    type: Optional[str] = None  # e.g. "positive", "negative", "neutral"
    
    # If you need to override the Node __init__ method
    # def __init__(self, id: uuid.UUID = None, name: str = "", description: str = None, 
    #              relationships: List[uuid.UUID] = None, **kwargs):
    #     super().__init__(id=id, name=name, description=description, **kwargs)
    #     self.relationships = relationships or []

@dataclass
class TechnologySystem(Node):
    """Coherent system of techniques, tools and knowledge."""
    maturity: Optional[float] = None  # Technology readiness level
    compatibility: Dict[str, float] = field(default_factory=dict)  # Fit with other systems

@dataclass
class Indicator(Node):
    """Measurable proxy for system performance."""
    value_category: Optional[ValueCategory] = None  # Non-default field moved to the beginning
    measurement_unit: Optional[str] = None             # Non-default field moved to the beginning  
    current_value: Optional[float] = None
    target_value: Optional[float] = None
    threshold_values: Dict[str, float] = field(default_factory=dict)

@dataclass
class AnalyticalContext(Node):
    """Contains metadata about analysis parameters and configuration."""
    methods_used: List[str] = field(default_factory=list)
    assumptions: Dict[str, str] = field(default_factory=dict)
    data_sources: Dict[str, str] = field(default_factory=dict)
    validation_approach: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: Optional[datetime] = None
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SystemProperty(Node):
    """Represents a system-level property or metric of the SFM."""
    property_type: str = ""
    value: Any = None
    unit: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    affected_nodes: List[uuid.UUID] = field(default_factory=list)  # Nodes that this property applies to
    contributing_relationships: List[uuid.UUID] = field(default_factory=list)  # Relationships that contribute to this property
    # id, name, and description are inherited from Node


# ───────────────────────────────────────────────
# EXPLICIT RELATIONSHIP OBJECT
# (Keeps multiplicity, weight, and dimension tags)
# ───────────────────────────────────────────────

@dataclass
class Relationship:
    """Typed edge connecting two nodes in the SFM graph."""
    source_id: uuid.UUID
    target_id: uuid.UUID
    kind: RelationshipKind
    weight: Optional[float] = 0.0         # e.g. $-value, mass, influence score
    time: Optional[TimeSlice] = None  # Temporal context of the relationship
    space: Optional[SpatialUnit] = None
    scenario: Optional[Scenario] = None
    meta: Dict[str, str] = field(default_factory=dict)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    certainty: Optional[float] = 1.0  # Confidence level (0-1)
    variability: Optional[float] = None  # Standard deviation or range

# ───────────────────────────────────────────────
# BOUNDRY/DOMAIN “GRAPH” AGGREGATE
# ───────────────────────────────────────────────

@dataclass
class SFMGraph:
    """A complete Social Fabric Matrix representation."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""
    description: Optional[str] = None
    
    # Core SFM components
    actors: Dict[uuid.UUID, Actor] = field(default_factory=dict)
    institutions: Dict[uuid.UUID, Institution] = field(default_factory=dict)
    resources: Dict[uuid.UUID, Resource] = field(default_factory=dict)
    processes: Dict[uuid.UUID, Process] = field(default_factory=dict)
    flows: Dict[uuid.UUID, Flow] = field(default_factory=dict)
    relationships: Dict[uuid.UUID, Relationship] = field(default_factory=dict)
    
    # Optional specialized components
    belief_systems: Dict[uuid.UUID, BeliefSystem] = field(default_factory=dict)
    technology_systems: Dict[uuid.UUID, TechnologySystem] = field(default_factory=dict)
    indicators: Dict[uuid.UUID, Indicator] = field(default_factory=dict)
    policies: Dict[uuid.UUID, Policy] = field(default_factory=dict)
    feedback_loops: Dict[uuid.UUID, FeedbackLoop] = field(default_factory=dict)
    system_properties: Dict[uuid.UUID, SystemProperty] = field(default_factory=dict)
    analytical_contexts: Dict[uuid.UUID, AnalyticalContext] = field(default_factory=dict)
    
    def add_node(self, node: Node) -> Node:
        """Add a node to the appropriate collection based on its type."""
        if isinstance(node, Actor):
            self.actors[node.id] = node
        elif isinstance(node, Institution) and not isinstance(node, Policy): # Policy is a subclass of Institution
            self.institutions[node.id] = node
        elif isinstance(node, Resource):
            self.resources[node.id] = node
        elif isinstance(node, Process):
            self.processes[node.id] = node
        elif isinstance(node, Flow):
            self.flows[node.id] = node
        elif isinstance(node, BeliefSystem):
            self.belief_systems[node.id] = node
        elif isinstance(node, TechnologySystem):
            self.technology_systems[node.id] = node
        elif isinstance(node, Indicator):
            self.indicators[node.id] = node
        elif isinstance(node, Policy):
            self.policies[node.id] = node
        elif isinstance(node, FeedbackLoop):
            self.feedback_loops[node.id] = node
        elif isinstance(node, SystemProperty):
            self.system_properties[node.id] = node
        elif isinstance(node, AnalyticalContext):
            self.analytical_contexts[node.id] = node
        else:
            raise TypeError(f"Unsupported node type: {type(node)}")
        
        return node
    
    def add_relationship(self, relationship: Relationship) -> Relationship:
        """Add a relationship to the SFM graph."""
        if not isinstance(relationship, Relationship):
            raise TypeError(f"Expected Relationship but got {type(relationship)}")
        
        # Ensure the relationship has an ID
        if relationship.id is None:
            relationship.id = uuid.uuid4()
        
        # Store the relationship
        self.relationships[relationship.id] = relationship
        return relationship

    def __iter__(self):
        """Iterate over all nodes in the SFMGraph."""
        for collection in [
            self.actors,
            self.institutions,
            self.resources,
            self.processes,
            self.flows,
            self.belief_systems,
            self.technology_systems,
            self.indicators,
            self.policies,
            self.feedback_loops,
            self.system_properties,
            self.analytical_contexts,
        ]:
            yield from collection.values()
