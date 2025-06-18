from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, TypeVar, Generic
import uuid
from core.sfm_models import (
    Node, Actor, Institution, Resource, Process, Flow, Relationship,
    BeliefSystem, Policy, FeedbackLoop, TechnologySystem, Indicator,
    AnalyticalContext, SystemProperty, SFMGraph, RelationshipKind, ValueCategory
)

T = TypeVar('T')

class Repository(Generic[T], ABC):
    """Base repository interface with standard CRUD operations."""
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity."""
        pass
    
    @abstractmethod
    def read(self, id: uuid.UUID) -> Optional[T]:
        """Read an entity by ID."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an entity."""
        pass
    
    @abstractmethod
    def delete(self, id: uuid.UUID) -> bool:
        """Delete an entity by ID."""
        pass
    
    @abstractmethod
    def list_all(self) -> List[T]:
        """List all entities."""
        pass
    
    @abstractmethod
    def query(self, filters: Dict[str, Any]) -> List[T]:
        """Query entities based on filters."""
        pass


class NodeRepository(Repository[T], ABC):
    """Base interface for node repositories with graph-specific operations."""
    
    @abstractmethod
    def get_related_nodes(self, node_id: uuid.UUID, 
                          relationship_kind: Optional[RelationshipKind] = None,
                          direction: str = "outgoing") -> List[Node]:
        """Get nodes related to the specified node."""
        pass
    
    @abstractmethod
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[Node]:
        """Get neighboring nodes within specified number of hops."""
        pass


class ActorRepository(NodeRepository[Actor]):
    """Repository interface for Actor entities."""
    pass


class InstitutionRepository(NodeRepository[Institution]):
    """Repository interface for Institution entities."""
    pass


class PolicyRepository(NodeRepository[Policy]):
    """Repository interface for Policy entities."""
    
    @abstractmethod
    def find_by_authority(self, authority: str) -> List[Policy]:
        """Find policies by implementing authority."""
        pass
    
    @abstractmethod
    def find_by_target_sector(self, sector: str) -> List[Policy]:
        """Find policies targeting a specific sector."""
        pass


class ResourceRepository(NodeRepository[Resource]):
    """Repository interface for Resource entities."""
    pass


class ProcessRepository(NodeRepository[Process]):
    """Repository interface for Process entities."""
    pass


class FlowRepository(NodeRepository[Flow]):
    """Repository interface for Flow entities."""
    pass


class BeliefSystemRepository(NodeRepository[BeliefSystem]):
    """Repository interface for BeliefSystem entities."""
    
    @abstractmethod
    def find_by_domain(self, domain: str) -> List[BeliefSystem]:
        """Find belief systems by domain of influence."""
        pass


class TechnologySystemRepository(NodeRepository[TechnologySystem]):
    """Repository interface for TechnologySystem entities."""
    
    @abstractmethod
    def find_by_maturity_range(self, min_maturity: float, max_maturity: float) -> List[TechnologySystem]:
        """Find technology systems within a specified maturity range."""
        pass
    
    @abstractmethod
    def find_by_compatibility(self, tech_id: str, min_compatibility: float) -> List[TechnologySystem]:
        """Find technology systems compatible with specified technology."""
        pass


class IndicatorRepository(NodeRepository[Indicator]):
    """Repository interface for Indicator entities."""
    
    @abstractmethod
    def find_by_value_category(self, category: ValueCategory) -> List[Indicator]:
        """Find indicators by value category."""
        pass
    
    @abstractmethod
    def find_by_value_range(self, min_value: float, max_value: float) -> List[Indicator]:
        """Find indicators within a specific value range."""
        pass
    
    @abstractmethod
    def find_below_threshold(self, threshold_key: str, threshold_value: float) -> List[Indicator]:
        """Find indicators below a specified threshold."""
        pass


class RelationshipRepository(Repository[Relationship]):
    """Repository interface for Relationship entities."""
    
    @abstractmethod
    def find_by_nodes(self, source_id: uuid.UUID, target_id: uuid.UUID) -> List[Relationship]:
        """Find relationships between specific nodes."""
        pass
    
    @abstractmethod
    def find_by_source(self, source_id: uuid.UUID) -> List[Relationship]:
        """Find relationships originating from a source node."""
        pass
    
    @abstractmethod
    def find_by_target(self, target_id: uuid.UUID) -> List[Relationship]:
        """Find relationships targeting a specific node."""
        pass
    
    @abstractmethod
    def find_by_kind(self, kind: RelationshipKind) -> List[Relationship]:
        """Find relationships of a specific kind."""
        pass
    
    @abstractmethod
    def find_by_certainty_range(self, min_certainty: float, max_certainty: float) -> List[Relationship]:
        """Find relationships within a specific certainty range."""
        pass
    
    @abstractmethod
    def find_high_variability(self, threshold: float) -> List[Relationship]:
        """Find relationships with variability above threshold."""
        pass


class FeedbackLoopRepository(Repository[FeedbackLoop]):
    """Repository interface for FeedbackLoop entities."""
    
    @abstractmethod
    def find_by_type(self, loop_type: str) -> List[FeedbackLoop]:
        """Find feedback loops by type (reinforcing or balancing)."""
        pass
    
    @abstractmethod
    def find_containing_relationship(self, relationship_id: uuid.UUID) -> List[FeedbackLoop]:
        """Find feedback loops containing a specific relationship."""
        pass
    
    @abstractmethod
    def find_by_strength_range(self, min_strength: float, max_strength: float) -> List[FeedbackLoop]:
        """Find feedback loops within a specific strength range."""
        pass


class AnalyticalContextRepository(Repository[AnalyticalContext]):
    """Repository interface for AnalyticalContext entities."""
    
    @abstractmethod
    def find_by_method(self, method: str) -> List[AnalyticalContext]:
        """Find analytical contexts using a specific method."""
        pass


class SystemPropertyRepository(Repository[SystemProperty]):
    """Repository interface for SystemProperty entities."""
    
    @abstractmethod
    def find_by_affected_node(self, node_id: uuid.UUID) -> List[SystemProperty]:
        """Find system properties affecting a specific node."""
        pass
    
    @abstractmethod
    def find_by_contributing_relationship(self, relationship_id: uuid.UUID) -> List[SystemProperty]:
        """Find system properties influenced by a specific relationship."""
        pass


class GraphRepository(ABC):
    """Repository interface for complete SFM graphs with advanced analysis."""
    
    @abstractmethod
    def save_graph(self, sfm_graph: SFMGraph) -> None:
        """Save a complete SFM graph."""
        pass
    
    @abstractmethod
    def load_graph(self, graph_id: Optional[str] = None) -> SFMGraph:
        """Load a complete SFM graph."""
        pass
    
    @abstractmethod
    def clear_graph(self) -> None:
        """Clear all graph data."""
        pass
    
    @abstractmethod
    def find_paths(self, source_id: uuid.UUID, target_id: uuid.UUID, 
                   max_length: Optional[int] = None) -> List[List[uuid.UUID]]:
        """Find all paths between source and target nodes."""
        pass
    
    @abstractmethod
    def detect_cycles(self, start_node_id: Optional[uuid.UUID] = None) -> List[List[uuid.UUID]]:
        """Detect cycles in the graph."""
        pass
    
    @abstractmethod
    def get_subgraph(self, node_ids: List[uuid.UUID]) -> SFMGraph:
        """Extract a subgraph containing only specified nodes and their relationships."""
        pass
    
    @abstractmethod
    def calculate_centrality(self, centrality_type: str = "betweenness") -> Dict[uuid.UUID, float]:
        """Calculate centrality measures for nodes."""
        pass
    
    @abstractmethod
    def find_communities(self) -> List[List[uuid.UUID]]:
        """Detect communities/clusters in the graph."""
        pass
    
    @abstractmethod
    def get_delivery_matrix(self) -> Dict[uuid.UUID, Dict[uuid.UUID, float]]:
        """Generate the delivery matrix representation of flows."""
        pass
    
    @abstractmethod
    def identify_feedback_loops(self) -> List[FeedbackLoop]:
        """Identify feedback loops in the system."""
        pass
    
    @abstractmethod
    def extract_belief_network(self) -> SFMGraph:
        """Extract subgraph of belief systems and their relationships."""
        pass
    
    @abstractmethod
    def extract_policy_network(self) -> SFMGraph:
        """Extract subgraph of policies and affected entities."""
        pass
    
    @abstractmethod
    def calculate_indicator_impacts(self, policy_id: uuid.UUID) -> Dict[uuid.UUID, float]:
        """Calculate how a policy affects various indicators."""
        pass
    
    @abstractmethod
    def find_critical_nodes(self, criteria: str = "betweenness") -> List[uuid.UUID]:
        """Identify critical nodes based on specified criteria."""
        pass