"""
Unit tests for the RepositoryFactory class in db/repository_factory.py
"""

import unittest
from typing import cast, Dict, List, Optional, Any
import uuid
from db.repository_factory import RepositoryFactory
from db.abstract_repository import (
    ActorRepository, InstitutionRepository, PolicyRepository, ResourceRepository,
    ProcessRepository, FlowRepository, BeliefSystemRepository, TechnologySystemRepository,
    IndicatorRepository, RelationshipRepository, FeedbackLoopRepository,
    AnalyticalContextRepository, SystemPropertyRepository, GraphRepository
)
from core.sfm_models import (
    Actor, Institution, Policy, Resource, Process, Flow, BeliefSystem,
    TechnologySystem, Indicator, Relationship, FeedbackLoop, AnalyticalContext,
    SystemProperty, SFMGraph, RelationshipKind, ValueCategory
)


# Mock Repository Classes
class MockActorRepository(ActorRepository):
    """Mock actor repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.actors: Dict[uuid.UUID, Actor] = {}
    
    def create(self, entity: Actor) -> Actor:
        self.actors[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[Actor]:
        return self.actors.get(id)
    
    def update(self, entity: Actor) -> Actor:
        if entity.id in self.actors:
            self.actors[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.actors:
            del self.actors[id]
            return True
        return False
    
    def list_all(self) -> List[Actor]:
        return list(self.actors.values())
    
    def query(self, filters: Dict[str, Any]) -> List[Actor]:
        result = []
        for actor in self.actors.values():
            match = True
            for key, value in filters.items():
                if not hasattr(actor, key) or getattr(actor, key) != value:
                    match = False
                    break
            if match:
                result.append(actor)
        return result
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[Actor]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[Actor]:
        return []


class MockInstitutionRepository(InstitutionRepository):
    """Mock institution repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.institutions: Dict[uuid.UUID, Institution] = {}
    
    def create(self, entity: Institution) -> Institution:
        self.institutions[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[Institution]:
        return self.institutions.get(id)
    
    def update(self, entity: Institution) -> Institution:
        if entity.id in self.institutions:
            self.institutions[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.institutions:
            del self.institutions[id]
            return True
        return False
    
    def list_all(self) -> List[Institution]:
        return list(self.institutions.values())
    
    def query(self, filters: Dict[str, Any]) -> List[Institution]:
        return []
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[Institution]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[Institution]:
        return []


class MockPolicyRepository(PolicyRepository):
    """Mock policy repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.policies: Dict[uuid.UUID, Policy] = {}
    
    def create(self, entity: Policy) -> Policy:
        self.policies[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[Policy]:
        return self.policies.get(id)
    
    def update(self, entity: Policy) -> Policy:
        if entity.id in self.policies:
            self.policies[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.policies:
            del self.policies[id]
            return True
        return False
    
    def list_all(self) -> List[Policy]:
        return list(self.policies.values())
    
    def query(self, filters: Dict[str, Any]) -> List[Policy]:
        return []
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[Policy]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[Policy]:
        return []
    
    def find_by_authority(self, authority: str) -> List[Policy]:
        return []
    
    def find_by_target_sector(self, sector: str) -> List[Policy]:
        return []


class MockResourceRepository(ResourceRepository):
    """Mock resource repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.resources: Dict[uuid.UUID, Resource] = {}
    
    def create(self, entity: Resource) -> Resource:
        self.resources[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[Resource]:
        return self.resources.get(id)
    
    def update(self, entity: Resource) -> Resource:
        if entity.id in self.resources:
            self.resources[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.resources:
            del self.resources[id]
            return True
        return False
    
    def list_all(self) -> List[Resource]:
        return list(self.resources.values())
    
    def query(self, filters: Dict[str, Any]) -> List[Resource]:
        return []
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[Resource]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[Resource]:
        return []


class MockProcessRepository(ProcessRepository):
    """Mock process repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.processes: Dict[uuid.UUID, Process] = {}
    
    def create(self, entity: Process) -> Process:
        self.processes[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[Process]:
        return self.processes.get(id)
    
    def update(self, entity: Process) -> Process:
        if entity.id in self.processes:
            self.processes[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.processes:
            del self.processes[id]
            return True
        return False
    
    def list_all(self) -> List[Process]:
        return list(self.processes.values())
    
    def query(self, filters: Dict[str, Any]) -> List[Process]:
        return []
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[Process]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[Process]:
        return []


class MockFlowRepository(FlowRepository):
    """Mock flow repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.flows: Dict[uuid.UUID, Flow] = {}
    
    def create(self, entity: Flow) -> Flow:
        self.flows[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[Flow]:
        return self.flows.get(id)
    
    def update(self, entity: Flow) -> Flow:
        if entity.id in self.flows:
            self.flows[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.flows:
            del self.flows[id]
            return True
        return False
    
    def list_all(self) -> List[Flow]:
        return list(self.flows.values())
    
    def query(self, filters: Dict[str, Any]) -> List[Flow]:
        return []
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[Flow]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[Flow]:
        return []


class MockBeliefSystemRepository(BeliefSystemRepository):
    """Mock belief system repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.belief_systems: Dict[uuid.UUID, BeliefSystem] = {}
    
    def create(self, entity: BeliefSystem) -> BeliefSystem:
        self.belief_systems[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[BeliefSystem]:
        return self.belief_systems.get(id)
    
    def update(self, entity: BeliefSystem) -> BeliefSystem:
        if entity.id in self.belief_systems:
            self.belief_systems[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.belief_systems:
            del self.belief_systems[id]
            return True
        return False
    
    def list_all(self) -> List[BeliefSystem]:
        return list(self.belief_systems.values())
    
    def query(self, filters: Dict[str, Any]) -> List[BeliefSystem]:
        return []
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[BeliefSystem]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[BeliefSystem]:
        return []
    
    def find_by_domain(self, domain: str) -> List[BeliefSystem]:
        return []


class MockTechnologySystemRepository(TechnologySystemRepository):
    """Mock technology system repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.technology_systems: Dict[uuid.UUID, TechnologySystem] = {}
    
    def create(self, entity: TechnologySystem) -> TechnologySystem:
        self.technology_systems[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[TechnologySystem]:
        return self.technology_systems.get(id)
    
    def update(self, entity: TechnologySystem) -> TechnologySystem:
        if entity.id in self.technology_systems:
            self.technology_systems[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.technology_systems:
            del self.technology_systems[id]
            return True
        return False
    
    def list_all(self) -> List[TechnologySystem]:
        return list(self.technology_systems.values())
    
    def query(self, filters: Dict[str, Any]) -> List[TechnologySystem]:
        return []
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[TechnologySystem]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[TechnologySystem]:
        return []
    
    def find_by_maturity_range(self, min_maturity: float, max_maturity: float) -> List[TechnologySystem]:
        return []
    
    def find_by_compatibility(self, tech_name: str, min_compatibility: float) -> List[TechnologySystem]:
        return []


class MockIndicatorRepository(IndicatorRepository):
    """Mock indicator repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.indicators: Dict[uuid.UUID, Indicator] = {}
    
    def create(self, entity: Indicator) -> Indicator:
        self.indicators[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[Indicator]:
        return self.indicators.get(id)
    
    def update(self, entity: Indicator) -> Indicator:
        if entity.id in self.indicators:
            self.indicators[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.indicators:
            del self.indicators[id]
            return True
        return False
    
    def list_all(self) -> List[Indicator]:
        return list(self.indicators.values())
    
    def query(self, filters: Dict[str, Any]) -> List[Indicator]:
        return []
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[Indicator]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[Indicator]:
        return []
    
    def find_by_value_category(self, category: ValueCategory) -> List[Indicator]:
        return []
    
    def find_by_value_range(self, min_value: float, max_value: float) -> List[Indicator]:
        return []
    
    def find_below_threshold(self, threshold_name: str, threshold_value: float) -> List[Indicator]:
        return []


class MockRelationshipRepository(RelationshipRepository):
    """Mock relationship repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.relationships: Dict[uuid.UUID, Relationship] = {}
    
    def create(self, entity: Relationship) -> Relationship:
        self.relationships[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[Relationship]:
        return self.relationships.get(id)
    
    def update(self, entity: Relationship) -> Relationship:
        if entity.id in self.relationships:
            self.relationships[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.relationships:
            del self.relationships[id]
            return True
        return False
    
    def list_all(self) -> List[Relationship]:
        return list(self.relationships.values())
    
    def query(self, filters: Dict[str, Any]) -> List[Relationship]:
        return []
    
    def find_by_nodes(self, source_id: uuid.UUID, target_id: uuid.UUID) -> List[Relationship]:
        return []
    
    def find_by_source(self, source_id: uuid.UUID) -> List[Relationship]:
        return []
    
    def find_by_target(self, target_id: uuid.UUID) -> List[Relationship]:
        return []
    
    def find_by_kind(self, kind: RelationshipKind) -> List[Relationship]:
        return []
    
    def find_by_certainty_range(self, min_certainty: float, max_certainty: float) -> List[Relationship]:
        return []
    
    def find_high_variability(self, threshold: float) -> List[Relationship]:
        return []


class MockFeedbackLoopRepository(FeedbackLoopRepository):
    """Mock feedback loop repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.feedback_loops: Dict[uuid.UUID, FeedbackLoop] = {}
    
    def create(self, entity: FeedbackLoop) -> FeedbackLoop:
        self.feedback_loops[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[FeedbackLoop]:
        return self.feedback_loops.get(id)
    
    def update(self, entity: FeedbackLoop) -> FeedbackLoop:
        if entity.id in self.feedback_loops:
            self.feedback_loops[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.feedback_loops:
            del self.feedback_loops[id]
            return True
        return False
    
    def list_all(self) -> List[FeedbackLoop]:
        return list(self.feedback_loops.values())
    
    def query(self, filters: Dict[str, Any]) -> List[FeedbackLoop]:
        return []
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[FeedbackLoop]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[FeedbackLoop]:
        return []
    
    # Missing abstract method implementations
    def find_by_strength_range(self, min_strength: float, max_strength: float) -> List[FeedbackLoop]:
        """Stub implementation for finding feedback loops by strength range."""
        return []
    
    def find_by_type(self, loop_type: str) -> List[FeedbackLoop]:
        """Stub implementation for finding feedback loops by type."""
        return []
    
    def find_containing_relationship(self, relationship_id: uuid.UUID) -> List[FeedbackLoop]:
        """Stub implementation for finding feedback loops containing a specific relationship."""
        return []


class MockAnalyticalContextRepository(AnalyticalContextRepository):
    """Mock analytical context repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.contexts: Dict[uuid.UUID, AnalyticalContext] = {}
    
    def create(self, entity: AnalyticalContext) -> AnalyticalContext:
        self.contexts[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[AnalyticalContext]:
        return self.contexts.get(id)
    
    def update(self, entity: AnalyticalContext) -> AnalyticalContext:
        if entity.id in self.contexts:
            self.contexts[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.contexts:
            del self.contexts[id]
            return True
        return False
    
    def list_all(self) -> List[AnalyticalContext]:
        return list(self.contexts.values())
    
    def query(self, filters: Dict[str, Any]) -> List[AnalyticalContext]:
        return []
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[AnalyticalContext]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[AnalyticalContext]:
        return []
    
    # Additional stub methods for AnalyticalContextRepository
    def find_by_method(self, method: str) -> List[AnalyticalContext]:
        """Stub implementation for finding contexts by analysis method."""
        return []
    
    def find_by_date_range(self, start_date: Any, end_date: Any) -> List[AnalyticalContext]:
        """Stub implementation for finding contexts by date range."""
        return []
    
    def find_by_validation_approach(self, approach: str) -> List[AnalyticalContext]:
        """Stub implementation for finding contexts by validation approach."""
        return []


class MockSystemPropertyRepository(SystemPropertyRepository):
    """Mock system property repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.properties: Dict[uuid.UUID, SystemProperty] = {}
    
    def create(self, entity: SystemProperty) -> SystemProperty:
        self.properties[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[SystemProperty]:
        return self.properties.get(id)
    
    def update(self, entity: SystemProperty) -> SystemProperty:
        if entity.id in self.properties:
            self.properties[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.properties:
            del self.properties[id]
            return True
        return False
    
    def list_all(self) -> List[SystemProperty]:
        return list(self.properties.values())
    
    def query(self, filters: Dict[str, Any]) -> List[SystemProperty]:
        return []
    
    def get_related_nodes(self, node_id: uuid.UUID, relationship_kind: Optional[RelationshipKind] = None, direction: str = "outgoing") -> List[SystemProperty]:
        return []
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[SystemProperty]:
        return []
    
    # Additional stub methods for SystemPropertyRepository
    def find_by_property_type(self, property_type: str) -> List[SystemProperty]:
        """Stub implementation for finding properties by type."""
        return []
    
    def find_by_scope(self, scope: str) -> List[SystemProperty]:
        """Stub implementation for finding properties by scope."""
        return []
    
    def find_emergent_properties(self) -> List[SystemProperty]:
        """Stub implementation for finding emergent properties."""
        return []
    
    def find_by_stability_range(self, min_stability: float, max_stability: float) -> List[SystemProperty]:
        """Stub implementation for finding properties by stability range."""
        return []
    
    # Missing abstract method implementations
    def find_by_affected_node(self, node_id: uuid.UUID) -> List[SystemProperty]:
        """Stub implementation for finding system properties that affect a specific node."""
        return []
    
    def find_by_contributing_relationship(self, relationship_id: uuid.UUID) -> List[SystemProperty]:
        """Stub implementation for finding system properties that are influenced by a specific relationship."""
        return []


class MockGraphRepository(GraphRepository):
    """Mock graph repository for testing."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.graphs: Dict[uuid.UUID, SFMGraph] = {}
    
    def create(self, entity: SFMGraph) -> SFMGraph:
        self.graphs[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[SFMGraph]:
        return self.graphs.get(id)
    
    def update(self, entity: SFMGraph) -> SFMGraph:
        if entity.id in self.graphs:
            self.graphs[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.graphs:
            del self.graphs[id]
            return True
        return False
    
    def list_all(self) -> List[SFMGraph]:
        return list(self.graphs.values())
    
    def query(self, filters: Dict[str, Any]) -> List[SFMGraph]:
        return []
    
    def save_graph(self, sfm_graph: SFMGraph) -> None:
        self.graphs[sfm_graph.id] = sfm_graph
    
    def load_graph(self, graph_id: Optional[str] = None) -> Optional[SFMGraph]:
        if graph_id:
            return self.graphs.get(uuid.UUID(graph_id))
        return list(self.graphs.values())[0] if self.graphs else None
    
    def clear_graph(self) -> None:
        self.graphs.clear()
    
    def find_paths(self, source_id: uuid.UUID, target_id: uuid.UUID, max_length: Optional[int] = None) -> List[List[uuid.UUID]]:
        return []
    
    def detect_cycles(self, start_node_id: Optional[uuid.UUID] = None) -> List[List[uuid.UUID]]:
        return []
    
    def get_subgraph(self, node_ids: List[uuid.UUID]) -> Optional[SFMGraph]:
        return SFMGraph(name="Test Subgraph")
    
    def calculate_centrality(self, centrality_type: str = "betweenness") -> Dict[uuid.UUID, float]:
        return {}
    
    def find_communities(self) -> List[List[uuid.UUID]]:
        return []
    
    def get_delivery_matrix(self) -> Dict[uuid.UUID, Dict[uuid.UUID, float]]:
        return {}
    
    def identify_feedback_loops(self) -> List[FeedbackLoop]:
        return []
    
    def extract_belief_network(self) -> Optional[SFMGraph]:
        return SFMGraph(name="Belief Network")
    
    def extract_policy_network(self) -> Optional[SFMGraph]:
        return SFMGraph(name="Policy Network")
    
    def calculate_indicator_impacts(self, policy_id: uuid.UUID) -> Dict[uuid.UUID, float]:
        return {}
    
    def find_critical_nodes(self, criteria: str = "betweenness") -> List[uuid.UUID]:
        return []


# Test Classes
class TestRepositoryRegistration(unittest.TestCase):
    """Test repository registration methods."""
    
    def setUp(self):
        """Clear registrations before each test."""
        RepositoryFactory._implementations = {
            'actor': {},
            'institution': {},
            'policy': {},
            'resource': {},
            'process': {},
            'flow': {},
            'belief_system': {},
            'technology_system': {},
            'indicator': {},
            'relationship': {},
            'feedback_loop': {},
            'analytical_context': {},
            'system_property': {},
            'graph': {}
        }
    
    def test_register_actor_repository(self):
        """Test registering an actor repository."""
        RepositoryFactory.register_actor_repository("test", MockActorRepository)
        self.assertIn("test", RepositoryFactory._implementations['actor'])
        self.assertEqual(RepositoryFactory._implementations['actor']['test'], MockActorRepository)
    
    def test_register_institution_repository(self):
        """Test registering an institution repository."""
        RepositoryFactory.register_institution_repository("test", MockInstitutionRepository)
        self.assertIn("test", RepositoryFactory._implementations['institution'])
        self.assertEqual(RepositoryFactory._implementations['institution']['test'], MockInstitutionRepository)
    
    def test_register_policy_repository(self):
        """Test registering a policy repository."""
        RepositoryFactory.register_policy_repository("test", MockPolicyRepository)
        self.assertIn("test", RepositoryFactory._implementations['policy'])
        self.assertEqual(RepositoryFactory._implementations['policy']['test'], MockPolicyRepository)
    
    def test_register_resource_repository(self):
        """Test registering a resource repository."""
        RepositoryFactory.register_resource_repository("test", MockResourceRepository)
        self.assertIn("test", RepositoryFactory._implementations['resource'])
        self.assertEqual(RepositoryFactory._implementations['resource']['test'], MockResourceRepository)
    
    def test_register_process_repository(self):
        """Test registering a process repository."""
        RepositoryFactory.register_process_repository("test", MockProcessRepository)
        self.assertIn("test", RepositoryFactory._implementations['process'])
        self.assertEqual(RepositoryFactory._implementations['process']['test'], MockProcessRepository)
    
    def test_register_flow_repository(self):
        """Test registering a flow repository."""
        RepositoryFactory.register_flow_repository("test", MockFlowRepository)
        self.assertIn("test", RepositoryFactory._implementations['flow'])
        self.assertEqual(RepositoryFactory._implementations['flow']['test'], MockFlowRepository)
    
    def test_register_belief_system_repository(self):
        """Test registering a belief system repository."""
        RepositoryFactory.register_belief_system_repository("test", MockBeliefSystemRepository)
        self.assertIn("test", RepositoryFactory._implementations['belief_system'])
        self.assertEqual(RepositoryFactory._implementations['belief_system']['test'], MockBeliefSystemRepository)
    
    def test_register_technology_system_repository(self):
        """Test registering a technology system repository."""
        RepositoryFactory.register_technology_system_repository("test", MockTechnologySystemRepository)
        self.assertIn("test", RepositoryFactory._implementations['technology_system'])
        self.assertEqual(RepositoryFactory._implementations['technology_system']['test'], MockTechnologySystemRepository)
    
    def test_register_indicator_repository(self):
        """Test registering an indicator repository."""
        RepositoryFactory.register_indicator_repository("test", MockIndicatorRepository)
        self.assertIn("test", RepositoryFactory._implementations['indicator'])
        self.assertEqual(RepositoryFactory._implementations['indicator']['test'], MockIndicatorRepository)
    
    def test_register_relationship_repository(self):
        """Test registering a relationship repository."""
        RepositoryFactory.register_relationship_repository("test", MockRelationshipRepository)
        self.assertIn("test", RepositoryFactory._implementations['relationship'])
        self.assertEqual(RepositoryFactory._implementations['relationship']['test'], MockRelationshipRepository)
    
    def test_register_feedback_loop_repository(self):
        """Test registering a feedback loop repository."""
        RepositoryFactory.register_feedback_loop_repository("test", MockFeedbackLoopRepository)
        self.assertIn("test", RepositoryFactory._implementations['feedback_loop'])
        self.assertEqual(RepositoryFactory._implementations['feedback_loop']['test'], MockFeedbackLoopRepository)
    
    def test_register_analytical_context_repository(self):
        """Test registering an analytical context repository."""
        RepositoryFactory.register_analytical_context_repository("test", MockAnalyticalContextRepository)
        self.assertIn("test", RepositoryFactory._implementations['analytical_context'])
        self.assertEqual(RepositoryFactory._implementations['analytical_context']['test'], MockAnalyticalContextRepository)
    
    def test_register_system_property_repository(self):
        """Test registering a system property repository."""
        RepositoryFactory.register_system_property_repository("test", MockSystemPropertyRepository)
        self.assertIn("test", RepositoryFactory._implementations['system_property'])
        self.assertEqual(RepositoryFactory._implementations['system_property']['test'], MockSystemPropertyRepository)
    
    def test_register_graph_repository(self):
        """Test registering a graph repository."""
        RepositoryFactory.register_graph_repository("test", MockGraphRepository)
        self.assertIn("test", RepositoryFactory._implementations['graph'])
        self.assertEqual(RepositoryFactory._implementations['graph']['test'], MockGraphRepository)


class TestRepositoryCreation(unittest.TestCase):
    """Test repository creation methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Clear registrations
        RepositoryFactory._implementations = {
            'actor': {},
            'institution': {},
            'policy': {},
            'resource': {},
            'process': {},
            'flow': {},
            'belief_system': {},
            'technology_system': {},
            'indicator': {},
            'relationship': {},
            'feedback_loop': {},
            'analytical_context': {},
            'system_property': {},
            'graph': {}
        }
        
        # Register all mock repositories
        RepositoryFactory.register_actor_repository("test", MockActorRepository)
        RepositoryFactory.register_institution_repository("test", MockInstitutionRepository)
        RepositoryFactory.register_policy_repository("test", MockPolicyRepository)
        RepositoryFactory.register_resource_repository("test", MockResourceRepository)
        RepositoryFactory.register_process_repository("test", MockProcessRepository)
        RepositoryFactory.register_flow_repository("test", MockFlowRepository)
        RepositoryFactory.register_belief_system_repository("test", MockBeliefSystemRepository)
        RepositoryFactory.register_technology_system_repository("test", MockTechnologySystemRepository)
        RepositoryFactory.register_indicator_repository("test", MockIndicatorRepository)
        RepositoryFactory.register_relationship_repository("test", MockRelationshipRepository)
        RepositoryFactory.register_feedback_loop_repository("test", MockFeedbackLoopRepository)
        RepositoryFactory.register_analytical_context_repository("test", MockAnalyticalContextRepository)
        RepositoryFactory.register_system_property_repository("test", MockSystemPropertyRepository)
        RepositoryFactory.register_graph_repository("test", MockGraphRepository)
    
    def test_get_actor_repository(self):
        """Test getting an actor repository."""
        repo = RepositoryFactory.get_actor_repository("test")
        self.assertIsInstance(repo, MockActorRepository)
    
    def test_get_actor_repository_with_kwargs(self):
        """Test getting an actor repository with kwargs."""
        test_kwargs = {"database_url": "test://localhost"}
        repo = RepositoryFactory.get_actor_repository("test", **test_kwargs)
        mock_repo = cast(MockActorRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_institution_repository(self):
        """Test getting an institution repository."""
        repo = RepositoryFactory.get_institution_repository("test")
        self.assertIsInstance(repo, MockInstitutionRepository)
    
    def test_get_institution_repository_with_kwargs(self):
        """Test getting an institution repository with kwargs."""
        test_kwargs = {"connection_pool": 5}
        repo = RepositoryFactory.get_institution_repository("test", **test_kwargs)
        mock_repo = cast(MockInstitutionRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_policy_repository(self):
        """Test getting a policy repository."""
        repo = RepositoryFactory.get_policy_repository("test")
        self.assertIsInstance(repo, MockPolicyRepository)
    
    def test_get_policy_repository_with_kwargs(self):
        """Test getting a policy repository with kwargs."""
        test_kwargs = {"timeout": 30}
        repo = RepositoryFactory.get_policy_repository("test", **test_kwargs)
        mock_repo = cast(MockPolicyRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_resource_repository(self):
        """Test getting a resource repository."""
        repo = RepositoryFactory.get_resource_repository("test")
        self.assertIsInstance(repo, MockResourceRepository)
    
    def test_get_resource_repository_with_kwargs(self):
        """Test getting a resource repository with kwargs."""
        test_kwargs = {"cache_size": 100}
        repo = RepositoryFactory.get_resource_repository("test", **test_kwargs)
        mock_repo = cast(MockResourceRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_process_repository(self):
        """Test getting a process repository."""
        repo = RepositoryFactory.get_process_repository("test")
        self.assertIsInstance(repo, MockProcessRepository)
    
    def test_get_process_repository_with_kwargs(self):
        """Test getting a process repository with kwargs."""
        test_kwargs = {"max_retries": 3}
        repo = RepositoryFactory.get_process_repository("test", **test_kwargs)
        mock_repo = cast(MockProcessRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_flow_repository(self):
        """Test getting a flow repository."""
        repo = RepositoryFactory.get_flow_repository("test")
        self.assertIsInstance(repo, MockFlowRepository)
    
    def test_get_flow_repository_with_kwargs(self):
        """Test getting a flow repository with kwargs."""
        test_kwargs = {"batch_size": 50}
        repo = RepositoryFactory.get_flow_repository("test", **test_kwargs)
        mock_repo = cast(MockFlowRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_belief_system_repository(self):
        """Test getting a belief system repository."""
        repo = RepositoryFactory.get_belief_system_repository("test")
        self.assertIsInstance(repo, MockBeliefSystemRepository)
    
    def test_get_belief_system_repository_with_kwargs(self):
        """Test getting a belief system repository with kwargs."""
        test_kwargs = {"index_name": "beliefs"}
        repo = RepositoryFactory.get_belief_system_repository("test", **test_kwargs)
        mock_repo = cast(MockBeliefSystemRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_technology_system_repository(self):
        """Test getting a technology system repository."""
        repo = RepositoryFactory.get_technology_system_repository("test")
        self.assertIsInstance(repo, MockTechnologySystemRepository)
    
    def test_get_technology_system_repository_with_kwargs(self):
        """Test getting a technology system repository with kwargs."""
        test_kwargs = {"compatibility_threshold": 0.5}
        repo = RepositoryFactory.get_technology_system_repository("test", **test_kwargs)
        mock_repo = cast(MockTechnologySystemRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_indicator_repository(self):
        """Test getting an indicator repository."""
        repo = RepositoryFactory.get_indicator_repository("test")
        self.assertIsInstance(repo, MockIndicatorRepository)
    
    def test_get_indicator_repository_with_kwargs(self):
        """Test getting an indicator repository with kwargs."""
        test_kwargs = {"measurement_precision": 2}
        repo = RepositoryFactory.get_indicator_repository("test", **test_kwargs)
        mock_repo = cast(MockIndicatorRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_relationship_repository(self):
        """Test getting a relationship repository."""
        repo = RepositoryFactory.get_relationship_repository("test")
        self.assertIsInstance(repo, MockRelationshipRepository)
    
    def test_get_relationship_repository_with_kwargs(self):
        """Test getting a relationship repository with kwargs."""
        test_kwargs = {"edge_limit": 1000}
        repo = RepositoryFactory.get_relationship_repository("test", **test_kwargs)
        mock_repo = cast(MockRelationshipRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_feedback_loop_repository(self):
        """Test getting a feedback loop repository."""
        repo = RepositoryFactory.get_feedback_loop_repository("test")
        self.assertIsInstance(repo, MockFeedbackLoopRepository)
    
    def test_get_feedback_loop_repository_with_kwargs(self):
        """Test getting a feedback loop repository with kwargs."""
        test_kwargs = {"loop_detection_depth": 5}
        repo = RepositoryFactory.get_feedback_loop_repository("test", **test_kwargs)
        mock_repo = cast(MockFeedbackLoopRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_analytical_context_repository(self):
        """Test getting an analytical context repository."""
        repo = RepositoryFactory.get_analytical_context_repository("test")
        self.assertIsInstance(repo, MockAnalyticalContextRepository)
    
    def test_get_analytical_context_repository_with_kwargs(self):
        """Test getting an analytical context repository with kwargs."""
        test_kwargs = {"analysis_cache_ttl": 3600}
        repo = RepositoryFactory.get_analytical_context_repository("test", **test_kwargs)
        mock_repo = cast(MockAnalyticalContextRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_system_property_repository(self):
        """Test getting a system property repository."""
        repo = RepositoryFactory.get_system_property_repository("test")
        self.assertIsInstance(repo, MockSystemPropertyRepository)
    
    def test_get_system_property_repository_with_kwargs(self):
        """Test getting a system property repository with kwargs."""
        test_kwargs = {"property_validation": True}
        repo = RepositoryFactory.get_system_property_repository("test", **test_kwargs)
        mock_repo = cast(MockSystemPropertyRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)
    
    def test_get_graph_repository(self):
        """Test getting a graph repository."""
        repo = RepositoryFactory.get_graph_repository("test")
        self.assertIsInstance(repo, MockGraphRepository)
    
    def test_get_graph_repository_with_kwargs(self):
        """Test getting a graph repository with kwargs."""
        test_kwargs = {"connection_string": "neo4j://localhost", "max_connections": 10}
        repo = RepositoryFactory.get_graph_repository("test", **test_kwargs)
        mock_repo = cast(MockGraphRepository, repo)
        self.assertEqual(mock_repo.kwargs, test_kwargs)


class TestRepositoryCreationErrors(unittest.TestCase):
    """Test error handling in repository creation."""
    
    def setUp(self):
        """Clear registrations before each test."""
        RepositoryFactory._implementations = {
            'actor': {},
            'institution': {},
            'policy': {},
            'resource': {},
            'process': {},
            'flow': {},
            'belief_system': {},
            'technology_system': {},
            'indicator': {},
            'relationship': {},
            'feedback_loop': {},
            'analytical_context': {},
            'system_property': {},
            'graph': {}
        }
    
    def test_get_nonexistent_actor_repository(self):
        """Test getting a nonexistent actor repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_actor_repository("nonexistent")
        self.assertIn("No actor repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_institution_repository(self):
        """Test getting a nonexistent institution repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_institution_repository("nonexistent")
        self.assertIn("No institution repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_policy_repository(self):
        """Test getting a nonexistent policy repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_policy_repository("nonexistent")
        self.assertIn("No policy repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_resource_repository(self):
        """Test getting a nonexistent resource repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_resource_repository("nonexistent")
        self.assertIn("No resource repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_process_repository(self):
        """Test getting a nonexistent process repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_process_repository("nonexistent")
        self.assertIn("No process repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_flow_repository(self):
        """Test getting a nonexistent flow repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_flow_repository("nonexistent")
        self.assertIn("No flow repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_belief_system_repository(self):
        """Test getting a nonexistent belief system repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_belief_system_repository("nonexistent")
        self.assertIn("No belief system repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_technology_system_repository(self):
        """Test getting a nonexistent technology system repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_technology_system_repository("nonexistent")
        self.assertIn("No technology system repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_indicator_repository(self):
        """Test getting a nonexistent indicator repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_indicator_repository("nonexistent")
        self.assertIn("No indicator repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_relationship_repository(self):
        """Test getting a nonexistent relationship repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_relationship_repository("nonexistent")
        self.assertIn("No relationship repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_feedback_loop_repository(self):
        """Test getting a nonexistent feedback loop repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_feedback_loop_repository("nonexistent")
        self.assertIn("No feedback loop repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_analytical_context_repository(self):
        """Test getting a nonexistent analytical context repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_analytical_context_repository("nonexistent")
        self.assertIn("No analytical context repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_system_property_repository(self):
        """Test getting a nonexistent system property repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_system_property_repository("nonexistent")
        self.assertIn("No system property repository registered for provider: nonexistent", str(context.exception))
    
    def test_get_nonexistent_graph_repository(self):
        """Test getting a nonexistent graph repository raises ValueError."""
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.get_graph_repository("nonexistent")
        self.assertIn("No graph repository registered for provider: nonexistent", str(context.exception))


if __name__ == '__main__':
    unittest.main()