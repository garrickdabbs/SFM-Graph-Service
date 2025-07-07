"""
Graph structure and network metrics for SFM modeling.

This module defines the SFMGraph class that aggregates all SFM entities
and the NetworkMetrics class for network analysis.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Iterator

from core.base_nodes import Node
from core.core_nodes import (
    Actor, Institution, Policy, Resource, Process, Flow, ValueFlow, GovernanceStructure
)
from core.specialized_nodes import (
    BeliefSystem, TechnologySystem, Indicator, FeedbackLoop, SystemProperty,
    AnalyticalContext, PolicyInstrument
)
from core.behavioral_nodes import (
    ValueSystem, CeremonialBehavior, InstrumentalBehavior, ChangeProcess,
    CognitiveFramework, BehavioralPattern
)
from core.relationships import Relationship
from core.metadata_models import ModelMetadata, ValidationRule
from core.sfm_enums import EnumValidator
from datetime import datetime


@dataclass
class NetworkMetrics(Node):
    """Captures network analysis metrics for nodes or subgraphs."""

    centrality_measures: Dict[str, float] = field(default_factory=lambda: {})
    clustering_coefficient: Optional[float] = None
    path_lengths: Dict[uuid.UUID, float] = field(default_factory=lambda: {})
    community_assignment: Optional[str] = None


@dataclass
class SFMGraph:  # pylint: disable=too-many-instance-attributes
    """A complete Social Fabric Matrix representation."""

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""
    description: Optional[str] = None

    # Core SFM components
    actors: Dict[uuid.UUID, Actor] = field(default_factory=lambda: {})
    institutions: Dict[uuid.UUID, Institution] = field(default_factory=lambda: {})
    resources: Dict[uuid.UUID, Resource] = field(default_factory=lambda: {})
    processes: Dict[uuid.UUID, Process] = field(default_factory=lambda: {})
    flows: Dict[uuid.UUID, Flow] = field(default_factory=lambda: {})
    relationships: Dict[uuid.UUID, Relationship] = field(default_factory=lambda: {})
    # Optional specialized components
    belief_systems: Dict[uuid.UUID, BeliefSystem] = field(default_factory=lambda: {})
    technology_systems: Dict[uuid.UUID, TechnologySystem] = field(default_factory=lambda: {})
    indicators: Dict[uuid.UUID, Indicator] = field(default_factory=lambda: {})
    policies: Dict[uuid.UUID, Policy] = field(default_factory=lambda: {})
    feedback_loops: Dict[uuid.UUID, FeedbackLoop] = field(default_factory=lambda: {})
    system_properties: Dict[uuid.UUID, SystemProperty] = field(default_factory=lambda: {})
    analytical_contexts: Dict[uuid.UUID, AnalyticalContext] = field(default_factory=lambda: {})
    policy_instruments: Dict[uuid.UUID, PolicyInstrument] = field(default_factory=lambda: {})
    governance_structures: Dict[uuid.UUID, GovernanceStructure] = field(default_factory=lambda: {})

    # Hayden's enhanced SFM components
    value_systems: Dict[uuid.UUID, ValueSystem] = field(default_factory=lambda: {})
    ceremonial_behaviors: Dict[uuid.UUID, CeremonialBehavior] = field(default_factory=lambda: {})
    instrumental_behaviors: Dict[uuid.UUID, InstrumentalBehavior] = field(default_factory=lambda: {})
    change_processes: Dict[uuid.UUID, ChangeProcess] = field(default_factory=lambda: {})
    cognitive_frameworks: Dict[uuid.UUID, CognitiveFramework] = field(default_factory=lambda: {})
    behavioral_patterns: Dict[uuid.UUID, BehavioralPattern] = field(default_factory=lambda: {})
    value_flows: Dict[uuid.UUID, ValueFlow] = field(default_factory=lambda: {})
    network_metrics: Dict[uuid.UUID, NetworkMetrics] = field(default_factory=lambda: {})

    # Model metadata
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: Optional[datetime] = None
    data_quality: Optional[str] = None  # Description of data quality
    previous_version_id: Optional[uuid.UUID] = None
    model_metadata: Optional[ModelMetadata] = None
    validation_rules: List[ValidationRule] = field(default_factory=lambda: [])

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
        """Add a relationship to the SFM graph with validation."""

        # Perform SFM-specific validation if both nodes exist
        source_node = self._find_node_by_id(relationship.source_id)
        target_node = self._find_node_by_id(relationship.target_id)

        if source_node and target_node:
            source_type = source_node.__class__.__name__
            target_type = target_node.__class__.__name__

            # Validate the relationship context
            EnumValidator.validate_relationship_context(
                relationship.kind, source_type, target_type
            )

        # Store the relationship
        self.relationships[relationship.id] = relationship
        return relationship

    def _find_node_by_id(self, node_id: uuid.UUID) -> Optional[Node]:
        """Find a node by its ID across all node collections."""
        for node in self:
            if node.id == node_id:
                return node
        return None

    def __iter__(self) -> Iterator[Node]:
        """Iterate over all nodes in the SFMGraph."""
        yield from self.actors.values()
        yield from self.institutions.values()
        yield from self.resources.values()
        yield from self.processes.values()
        yield from self.flows.values()
        yield from self.belief_systems.values()
        yield from self.technology_systems.values()
        yield from self.indicators.values()
        yield from self.policies.values()
        yield from self.feedback_loops.values()
        yield from self.system_properties.values()
        yield from self.analytical_contexts.values()
        yield from self.policy_instruments.values()
        yield from self.governance_structures.values()
        yield from self.value_systems.values()
        yield from self.ceremonial_behaviors.values()
        yield from self.instrumental_behaviors.values()
        yield from self.change_processes.values()
        yield from self.cognitive_frameworks.values()
        yield from self.behavioral_patterns.values()
        yield from self.value_flows.values()
        yield from self.network_metrics.values()

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

    def clear(self) -> None:
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
