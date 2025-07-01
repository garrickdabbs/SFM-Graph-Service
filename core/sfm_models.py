"""
Core data structures for modeling F. Gregory Hayden's Social Fabric Matrix (SFM).

This module defines the foundational data classes and entities used to represent
actors, institutions, resources, processes, relationships, and other components
in SFM analysis of socio-economic systems.
"""

# sfm_schema.py
# Core data structures for modeling an F. Gregory Hayden Social Fabric Matrix (SFM)

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from core.sfm_enums import (
    InstitutionLayer,
    RelationshipKind,
    ResourceType,
    FlowNature,
    ValueCategory,
    FlowType,
    PolicyInstrumentType,
    ChangeType,
    BehaviorPatternType,
    FeedbackPolarity,
    FeedbackType,
    TemporalFunctionType,
    ValidationRuleType,
    SystemPropertyType,
    PowerResourceType,
    TechnologyReadinessLevel,
    LegitimacySource,
    PathDependencyStrength,
    ToolSkillTechnologyComplex,
    InstitutionalChangeMechanism,
)


# ───────────────────────────────────────────────
# DIMENSIONAL “META” ENTITIES
# ───────────────────────────────────────────────


@dataclass(frozen=True)
class TimeSlice:
    """Discrete period for snapshot-style SFM accounting (e.g., fiscal year, quarter)."""

    label: str  # e.g. "FY2025" or "Q1-2030"


@dataclass(frozen=True)
class SpatialUnit:
    """Hierarchical spatial identifier (nation, state, metro, census tract, etc.)."""

    code: str  # e.g. "US-WA-SEATTLE"
    name: str  # human-friendly display


@dataclass(frozen=True)
class Scenario:
    """Counterfactual or policy-design scenario name (baseline, carbon tax, UBI...)."""

    label: str


# ───────────────────────────────────────────────
# CORE NODES (ACTORS, PROCESSES, RESOURCES…)
# All inherit from a minimal “Node” base
# ───────────────────────────────────────────────


@dataclass
class Node:  # pylint: disable=too-many-instance-attributes
    """Generic graph node with a UUID primary key and free-form metadata."""

    label: str
    description: Optional[str] = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    meta: Dict[str, str] = field(default_factory=dict)
    # Versioning and data quality fields
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: Optional[datetime] = None
    certainty: Optional[float] = 1.0  # Confidence level (0-1)
    data_quality: Optional[str] = None  # Description of data quality
    previous_version_id: Optional[uuid.UUID] = None

    def __iter__(self):
        """Iterator that yields (attribute_name, attribute_value) pairs."""
        for attr_name, attr_value in self.__dict__.items():
            yield attr_name, attr_value


@dataclass
class Actor(Node):
    """Individuals, firms, agencies, communities."""

    legal_form: Optional[str] = None  # e.g. "Corporation", "Household"
    sector: Optional[str] = None  # NAICS or custom taxonomy

    # Additional SFM-relevant fields
    power_resources: Dict[str, float] = field(default_factory=dict)
    decision_making_capacity: Optional[float] = None
    institutional_affiliations: List[uuid.UUID] = field(default_factory=list)
    cognitive_frameworks: List[uuid.UUID] = field(default_factory=list)
    behavioral_patterns: List[uuid.UUID] = field(default_factory=list)


@dataclass
class Institution(Node):
    """Rules-in-use, organizations, or informal norms (Hayden’s three layers)."""

    layer: Optional[InstitutionLayer] = None

    # Additional fields for Hayden's framework
    formal_rules: List[str] = field(default_factory=list)
    informal_norms: List[str] = field(default_factory=list)
    enforcement_mechanisms: List[str] = field(default_factory=list)
    legitimacy_basis: Optional[str] = None
    change_resistance: Optional[float] = None
    path_dependencies: List[uuid.UUID] = field(default_factory=list)


@dataclass
class Policy(Institution):
    """Specific policy intervention or regulatory framework."""

    authority: Optional[str] = None  # Implementing body
    enforcement: Optional[float] = 0.0  # Strength of enforcement (0-1)
    target_sectors: List[str] = field(default_factory=list)


@dataclass
class Resource(Node):
    """Stock or asset available for use or transformation."""

    rtype: ResourceType = ResourceType.NATURAL
    unit: Optional[str] = None  # e.g. "tonnes", "person-hours"


@dataclass
class Process(Node):
    """
    Transformation activity that converts inputs to outputs 
    (production, consumption, disposal).
    """

    technology: Optional[str] = None  # e.g. "EAF-Steel-2024"
    responsible_actor_id: Optional[str] = None  # Actor that controls the process


@dataclass
class Flow(Node):  # pylint: disable=too-many-instance-attributes
    """Edge-like node representing an actual quantified transfer of resources or value."""

    nature: FlowNature = FlowNature.TRANSFER
    quantity: Optional[float] = None
    unit: Optional[str] = None
    time: Optional[TimeSlice] = None
    space: Optional[SpatialUnit] = None
    scenario: Optional[Scenario] = None

    # Additional SFM-specific fields
    flow_type: FlowType = FlowType.MATERIAL  # material, energy, information, financial, social
    source_process_id: Optional[uuid.UUID] = None
    target_process_id: Optional[uuid.UUID] = None
    transformation_coefficient: Optional[float] = None
    loss_factor: Optional[float] = None  # inefficiencies, waste

    # Hayden's value theory integration
    ceremonial_component: Optional[float] = None
    instrumental_component: Optional[float] = None
    temporal_dynamics: Optional[TemporalDynamics] = None  # Change over time


@dataclass
class BeliefSystem(Node):
    """Cultural myths, ideology or worldview that guides decision-making."""

    strength: Optional[float] = None  # Cultural embeddedness (0-1)
    domain: Optional[str] = None  # Area of society where belief operates


@dataclass
class FeedbackLoop(Node):
    """Represents a feedback loop in the Social Fabric Matrix."""

    relationships: List[uuid.UUID] = field(default_factory=list)
    description: Optional[str] = None
    polarity: Optional[FeedbackPolarity] = None  # "reinforcing" or "balancing"
    strength: Optional[float] = None  # Measure of loop strength/impact
    type: Optional[FeedbackType] = None  # e.g. "positive", "negative", "neutral"

@dataclass
class TechnologySystem(Node):
    """Coherent system of techniques, tools and knowledge."""

    maturity: Optional[float] = None  # Technology readiness level
    compatibility: Dict[str, float] = field(
        default_factory=dict
    )  # Fit with other systems


@dataclass
class Indicator(Node):
    """Measurable proxy for system performance."""

    value_category: Optional[ValueCategory] = (
        None  # Non-default field moved to the beginning
    )
    measurement_unit: Optional[str] = None  # Non-default field moved to the beginning
    current_value: Optional[float] = None
    target_value: Optional[float] = None
    threshold_values: Dict[str, float] = field(default_factory=dict)
    temporal_dynamics: Optional[TemporalDynamics] = None  # Track changes over time


@dataclass
class AnalyticalContext(Node):  # pylint: disable=too-many-instance-attributes
    """Contains metadata about analysis parameters and configuration."""

    methods_used: List[str] = field(default_factory=list)
    assumptions: Dict[str, str] = field(default_factory=dict)
    data_sources: Dict[str, str] = field(default_factory=dict)
    validation_approach: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: Optional[datetime] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    validation_rules: List[ValidationRule] = field(default_factory=list)


@dataclass
class SystemProperty(Node):
    """Represents a system-level property or metric of the SFM."""

    property_type: SystemPropertyType = SystemPropertyType.STRUCTURAL
    value: Any = None
    unit: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    affected_nodes: List[uuid.UUID] = field(
        default_factory=list
    )  # Nodes that this property applies to
    contributing_relationships: List[uuid.UUID] = field(
        default_factory=list
    )  # Relationships that contribute to this property
    # id, name, and description are inherited from Node


@dataclass
class ValueSystem(Node):
    """Hierarchical value structure that guides institutional behavior."""

    parent_values: List[uuid.UUID] = field(default_factory=list)
    priority_weight: Optional[float] = None
    cultural_domain: Optional[str] = None
    legitimacy_source: Optional[str] = None  # tradition, charisma, legal-rational


@dataclass
class CeremonialBehavior(Node):
    """Hayden's ceremonial behaviors that resist change."""

    rigidity_level: Optional[float] = None
    tradition_strength: Optional[float] = None
    resistance_to_change: Optional[float] = None


@dataclass
class InstrumentalBehavior(Node):
    """Problem-solving, adaptive behaviors."""

    efficiency_measure: Optional[float] = None
    adaptability_score: Optional[float] = None
    innovation_potential: Optional[float] = None


@dataclass
class PolicyInstrument(Node):
    """Specific tools used to implement policies."""

    instrument_type: PolicyInstrumentType = PolicyInstrumentType.REGULATORY  # regulatory, economic, voluntary, information
    target_behavior: Optional[str] = None
    compliance_mechanism: Optional[str] = None
    effectiveness_measure: Optional[float] = None


@dataclass
class GovernanceStructure(Institution):
    """Formal and informal governance arrangements."""

    decision_making_process: Optional[str] = None
    power_distribution: Dict[str, float] = field(default_factory=dict)
    accountability_mechanisms: List[str] = field(default_factory=list)


@dataclass
class ValueFlow(Flow):
    """Tracks value creation, capture, and distribution."""

    value_created: Optional[float] = None
    value_captured: Optional[float] = None
    beneficiary_actors: List[uuid.UUID] = field(default_factory=list)
    distributional_impact: Dict[str, float] = field(default_factory=dict)


@dataclass
class ChangeProcess(Node):
    """Models institutional and technological change over time."""

    change_type: ChangeType = ChangeType.EVOLUTIONARY  # evolutionary, revolutionary, cyclical
    change_agents: List[uuid.UUID] = field(default_factory=list)
    resistance_factors: List[uuid.UUID] = field(default_factory=list)
    change_trajectory: List[TimeSlice] = field(default_factory=list)
    success_probability: Optional[float] = None
    temporal_dynamics: Optional[TemporalDynamics] = None  # Detailed change over time


@dataclass
class CognitiveFramework(Node):
    """Mental models and worldviews that shape perception."""

    framing_effects: Dict[str, str] = field(default_factory=dict)
    cognitive_biases: List[str] = field(default_factory=list)
    information_filters: List[str] = field(default_factory=list)
    learning_capacity: Optional[float] = None


@dataclass
class BehavioralPattern(Node):
    """Recurring patterns of behavior in the social fabric."""

    pattern_type: BehaviorPatternType = BehaviorPatternType.HABITUAL  # habitual, strategic, adaptive, resistant
    frequency: Optional[float] = None
    predictability: Optional[float] = None
    context_dependency: List[str] = field(default_factory=list)


# ───────────────────────────────────────────────
# BASE CLASSES AND MIXINS
# ───────────────────────────────────────────────


@dataclass
class TemporalDynamics:
    """Models change over time for any value."""

    start_time: TimeSlice
    end_time: Optional[TimeSlice] = None
    function_type: TemporalFunctionType = TemporalFunctionType.LINEAR  # linear, exponential, logistic, etc.
    parameters: Dict[str, float] = field(default_factory=dict)


@dataclass
class ValidationRule:
    """Defines a validation rule for data integrity."""

    rule_type: ValidationRuleType  # e.g., "range", "sum", "required", "unique"
    target_field: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    error_message: str = ""


@dataclass
class ModelMetadata:  # pylint: disable=too-many-instance-attributes
    """Documentation about the model itself."""

    version: str
    authors: List[str] = field(default_factory=list)
    creation_date: datetime = field(default_factory=datetime.now)
    last_modified: Optional[datetime] = None
    citation: Optional[str] = None
    license: str = "MIT"
    description: str = ""
    change_log: List[str] = field(default_factory=list)


# ───────────────────────────────────────────────
# EXPLICIT RELATIONSHIP OBJECT
# (Keeps multiplicity, weight, and dimension tags)
# ───────────────────────────────────────────────


@dataclass
class Relationship:  # pylint: disable=too-many-instance-attributes
    """Typed edge connecting two nodes in the SFM graph."""

    source_id: uuid.UUID
    target_id: uuid.UUID
    kind: RelationshipKind
    weight: Optional[float] = 0.0  # e.g. $-value, mass, influence score
    time: Optional[TimeSlice] = None  # Temporal context of the relationship
    space: Optional[SpatialUnit] = None
    scenario: Optional[Scenario] = None
    meta: Dict[str, str] = field(default_factory=dict)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    certainty: Optional[float] = 1.0  # Confidence level (0-1)
    variability: Optional[float] = None  # Standard deviation or range
    # Versioning and data quality fields
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: Optional[datetime] = None
    data_quality: Optional[str] = None  # Description of data quality
    previous_version_id: Optional[uuid.UUID] = None
    temporal_dynamics: Optional[TemporalDynamics] = None  # Change over time


# ───────────────────────────────────────────────
# BOUNDRY/DOMAIN “GRAPH” AGGREGATE
# ───────────────────────────────────────────────


@dataclass
class SFMGraph:  # pylint: disable=too-many-instance-attributes
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
    analytical_contexts: Dict[uuid.UUID, AnalyticalContext] = field(
        default_factory=dict
    )
    policy_instruments: Dict[uuid.UUID, PolicyInstrument] = field(default_factory=dict)
    governance_structures: Dict[uuid.UUID, GovernanceStructure] = field(
        default_factory=dict
    )

    # Hayden's enhanced SFM components
    value_systems: Dict[uuid.UUID, ValueSystem] = field(default_factory=dict)
    ceremonial_behaviors: Dict[uuid.UUID, CeremonialBehavior] = field(
        default_factory=dict
    )
    instrumental_behaviors: Dict[uuid.UUID, InstrumentalBehavior] = field(
        default_factory=dict
    )
    change_processes: Dict[uuid.UUID, ChangeProcess] = field(default_factory=dict)
    cognitive_frameworks: Dict[uuid.UUID, CognitiveFramework] = field(
        default_factory=dict
    )
    behavioral_patterns: Dict[uuid.UUID, BehavioralPattern] = field(
        default_factory=dict
    )
    value_flows: Dict[uuid.UUID, ValueFlow] = field(default_factory=dict)
    network_metrics: Dict[uuid.UUID, NetworkMetrics] = field(default_factory=dict)

    # Model metadata
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: Optional[datetime] = None
    data_quality: Optional[str] = None  # Description of data quality
    previous_version_id: Optional[uuid.UUID] = None
    model_metadata: Optional[ModelMetadata] = None
    validation_rules: List[ValidationRule] = field(default_factory=list)
    network_metrics: Dict[uuid.UUID, NetworkMetrics] = field(default_factory=dict)

    def add_node(self, node: Node) -> Node:  # pylint: disable=too-many-branches
        """Add a node to the appropriate collection based on its type."""
        # Handle most specific types first to avoid inheritance conflicts
        if isinstance(node, ValueFlow):
            self.value_flows[node.id] = node
        elif isinstance(node, GovernanceStructure):
            self.governance_structures[node.id] = node
        elif isinstance(node, Policy):
            self.policies[node.id] = node
        elif isinstance(
            node, Institution
        ):  # Check Institution after Policy since Policy inherits from Institution
            self.institutions[node.id] = node
        elif isinstance(node, Actor):
            self.actors[node.id] = node
        elif isinstance(node, Resource):
            self.resources[node.id] = node
        elif isinstance(node, Process):
            self.processes[node.id] = node
        elif isinstance(
            node, Flow
        ):  # Check Flow after ValueFlow since ValueFlow inherits from Flow
            self.flows[node.id] = node
        elif isinstance(node, BeliefSystem):
            self.belief_systems[node.id] = node
        elif isinstance(node, TechnologySystem):
            self.technology_systems[node.id] = node
        elif isinstance(node, Indicator):
            self.indicators[node.id] = node
        elif isinstance(node, FeedbackLoop):
            self.feedback_loops[node.id] = node
        elif isinstance(node, SystemProperty):
            self.system_properties[node.id] = node
        elif isinstance(node, AnalyticalContext):
            self.analytical_contexts[node.id] = node
        elif isinstance(node, ValueSystem):
            self.value_systems[node.id] = node
        elif isinstance(node, CeremonialBehavior):
            self.ceremonial_behaviors[node.id] = node
        elif isinstance(node, InstrumentalBehavior):
            self.instrumental_behaviors[node.id] = node
        elif isinstance(node, PolicyInstrument):
            self.policy_instruments[node.id] = node
        elif isinstance(node, ChangeProcess):
            self.change_processes[node.id] = node
        elif isinstance(node, CognitiveFramework):
            self.cognitive_frameworks[node.id] = node
        elif isinstance(node, BehavioralPattern):
            self.behavioral_patterns[node.id] = node
        elif isinstance(node, NetworkMetrics):
            self.network_metrics[node.id] = node
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
            self.policy_instruments,
            self.governance_structures,
            self.value_systems,
            self.ceremonial_behaviors,
            self.instrumental_behaviors,
            self.change_processes,
            self.cognitive_frameworks,
            self.behavioral_patterns,
            self.value_flows,
            self.network_metrics,
        ]:
            yield from collection.values()

    def __len__(self) -> int:
        """Return the total number of nodes in the graph."""
        return (
            len(self.actors)
            + len(self.institutions)
            + len(self.resources)
            + len(self.processes)
            + len(self.flows)
            + len(self.belief_systems)
            + len(self.technology_systems)
            + len(self.indicators)
            + len(self.policies)
            + len(self.feedback_loops)
            + len(self.system_properties)
            + len(self.analytical_contexts)
            + len(self.policy_instruments)
            + len(self.governance_structures)
            + len(self.value_systems)
            + len(self.ceremonial_behaviors)
            + len(self.instrumental_behaviors)
            + len(self.change_processes)
            + len(self.cognitive_frameworks)
            + len(self.behavioral_patterns)
            + len(self.value_flows)
            + len(self.network_metrics)
        )

    def clear(self):
        """Clear all nodes and relationships from the graph."""
        self.actors.clear()
        self.institutions.clear()
        self.resources.clear()
        self.processes.clear()
        self.flows.clear()
        self.belief_systems.clear()
        self.technology_systems.clear()
        self.indicators.clear()
        self.policies.clear()
        self.feedback_loops.clear()
        self.system_properties.clear()
        self.analytical_contexts.clear()
        self.policy_instruments.clear()
        self.governance_structures.clear()
        self.value_systems.clear()
        self.ceremonial_behaviors.clear()
        self.instrumental_behaviors.clear()
        self.change_processes.clear()
        self.cognitive_frameworks.clear()
        self.behavioral_patterns.clear()
        self.value_flows.clear()
        self.network_metrics.clear()
        self.relationships.clear()
        self.network_metrics.clear()


@dataclass
class NetworkMetrics(Node):
    """Captures network analysis metrics for nodes or subgraphs."""

    centrality_measures: Dict[str, float] = field(default_factory=dict)
    clustering_coefficient: Optional[float] = None
    path_lengths: Dict[uuid.UUID, float] = field(default_factory=dict)
    community_assignment: Optional[str] = None
