import uuid
import numpy as np
from typing import Dict, List, Optional, Any, cast, TypeVar, Type, Generic
import networkx as nx
from core.sfm_models import (
    Node, Actor, Institution, Resource, Process, Flow, Relationship,
    BeliefSystem, Policy, FeedbackLoop, TechnologySystem, Indicator,
    AnalyticalContext, SystemProperty,
    SFMGraph, RelationshipKind, ValueCategory
)
from db.abstract_repository import (
    ActorRepository, InstitutionRepository, ResourceRepository,
    ProcessRepository, FlowRepository, RelationshipRepository, GraphRepository,
    PolicyRepository, BeliefSystemRepository, TechnologySystemRepository,
    IndicatorRepository, FeedbackLoopRepository, AnalyticalContextRepository,
    SystemPropertyRepository
)

T = TypeVar('T', bound=Node)

class NetworkXNodeRepository(Generic[T]):
    """Base implementation for Node repositories using NetworkX."""
    
    def __init__(self, graph: nx.MultiDiGraph, node_type: Type[T]):
        self.graph = graph
        self.node_type = node_type
        self.entity_name = node_type.__name__.lower()
    
    def create(self, entity: T) -> T:
        """Create a new entity in the graph."""
        if self.graph.has_node(entity.id):
            raise ValueError(f"Entity with id {entity.id} already exists")
        
        self.graph.add_node(entity.id, **{
            'entity': entity, 
            'type': self.entity_name,
            'label': entity.label
        })
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[T]:
        """Read an entity by ID."""
        if not self.graph.has_node(id):
            return None
        
        node_data = self.graph.nodes[id]
        if node_data.get('type') != self.entity_name:
            return None
        
        return cast(T, node_data['entity'])
    
    def update(self, entity: T) -> T:
        """Update an entity."""
        if not self.graph.has_node(entity.id):
            raise ValueError(f"No {self.entity_name} with id {entity.id} exists")
        
        node_data = self.graph.nodes[entity.id]
        if node_data.get('type') != self.entity_name:
            raise ValueError(f"Node {entity.id} is not a {self.entity_name}")
        
        # Update the stored entity and label
        self.graph.nodes[entity.id]['entity'] = entity
        self.graph.nodes[entity.id]['label'] = entity.label
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        """Delete an entity by ID."""
        if not self.graph.has_node(id):
            return False
        
        node_data = self.graph.nodes[id]
        if node_data.get('type') != self.entity_name:
            return False
        
        self.graph.remove_node(id)
        return True
    
    def list_all(self) -> List[T]:
        """List all entities of this type."""
        result = []
        for node_id, data in self.graph.nodes(data=True):
            if data.get('type') == self.entity_name:
                result.append(cast(T, data['entity']))
        return result
    
    def query(self, filters: Dict[str, Any]) -> List[T]:
        """Query entities based on property filters."""
        result = []
        for node_id, data in self.graph.nodes(data=True):
            if data.get('type') != self.entity_name:
                continue
            
            entity = cast(T, data['entity'])
            match = True
            
            for key, value in filters.items():
                if not hasattr(entity, key) or getattr(entity, key) != value:
                    match = False
                    break
            
            if match:
                result.append(entity)
        
        return result
    
    def get_related_nodes(self, node_id: uuid.UUID, 
                          relationship_kind: Optional[RelationshipKind] = None,
                          direction: str = "outgoing") -> List[Node]:
        """Get nodes related to the specified node."""
        if not self.graph.has_node(node_id):
            return []
        
        related_nodes = []
        
        if direction in ("outgoing", "both"):
            for _, target_id, edge_data in self.graph.out_edges(node_id, data=True):
                if self._matches_relationship_filter(edge_data, relationship_kind):
                    if self.graph.has_node(target_id):
                        related_nodes.append(self.graph.nodes[target_id]['entity'])
        
        if direction in ("incoming", "both"):
            for source_id, _, edge_data in self.graph.in_edges(node_id, data=True):
                if self._matches_relationship_filter(edge_data, relationship_kind):
                    if self.graph.has_node(source_id):
                        related_nodes.append(self.graph.nodes[source_id]['entity'])
        
        return related_nodes
    
    def get_neighbors(self, node_id: uuid.UUID, max_hops: int = 1) -> List[Node]:
        """Get neighboring nodes within specified number of hops."""
        if not self.graph.has_node(node_id) or max_hops < 1:
            return []
        
        visited = set()
        current_level = {node_id}
        
        for _ in range(max_hops):
            next_level = set()
            for node in current_level:
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in visited:
                        next_level.add(neighbor)
                        visited.add(neighbor)
            current_level = next_level
            if not current_level:
                break
        
        neighbors = []
        for neighbor_id in visited:
            if self.graph.has_node(neighbor_id):
                neighbors.append(self.graph.nodes[neighbor_id]['entity'])
        
        return neighbors
    
    def _matches_relationship_filter(self, edge_data: Dict, relationship_kind: Optional[RelationshipKind]) -> bool:
        """Check if an edge matches the relationship kind filter."""
        if relationship_kind is None:
            return True
        
        relationship = edge_data.get('relationship')
        if relationship is None:
            return False
        
        return relationship.kind == relationship_kind


# Concrete implementations for each node type
class NetworkXActorRepository(NetworkXNodeRepository[Actor], ActorRepository):
    def __init__(self, graph: nx.MultiDiGraph):
        super().__init__(graph, Actor)


class NetworkXInstitutionRepository(NetworkXNodeRepository[Institution], InstitutionRepository):
    def __init__(self, graph: nx.MultiDiGraph):
        super().__init__(graph, Institution)


class NetworkXPolicyRepository(NetworkXNodeRepository[Policy], PolicyRepository):
    def __init__(self, graph: nx.MultiDiGraph):
        super().__init__(graph, Policy)
    
    def find_by_authority(self, authority: str) -> List[Policy]:
        """Find policies by implementing authority."""
        return self.query({"authority": authority})
    
    def find_by_target_sector(self, sector: str) -> List[Policy]:
        """Find policies targeting a specific sector."""
        result = []
        for policy in self.list_all():
            if hasattr(policy, 'target_sectors') and sector in policy.target_sectors:
                result.append(policy)
        return result


class NetworkXResourceRepository(NetworkXNodeRepository[Resource], ResourceRepository):
    def __init__(self, graph: nx.MultiDiGraph):
        super().__init__(graph, Resource)


class NetworkXProcessRepository(NetworkXNodeRepository[Process], ProcessRepository):
    def __init__(self, graph: nx.MultiDiGraph):
        super().__init__(graph, Process)


class NetworkXFlowRepository(NetworkXNodeRepository[Flow], FlowRepository):
    def __init__(self, graph: nx.MultiDiGraph):
        super().__init__(graph, Flow)


class NetworkXBeliefSystemRepository(NetworkXNodeRepository[BeliefSystem], BeliefSystemRepository):
    def __init__(self, graph: nx.MultiDiGraph):
        super().__init__(graph, BeliefSystem)
    
    def find_by_domain(self, domain: str) -> List[BeliefSystem]:
        """Find belief systems by domain of influence."""
        return self.query({"domain": domain})


class NetworkXTechnologySystemRepository(NetworkXNodeRepository[TechnologySystem], TechnologySystemRepository):
    def __init__(self, graph: nx.MultiDiGraph):
        super().__init__(graph, TechnologySystem)
    
    def find_by_maturity_range(self, min_maturity: float, max_maturity: float) -> List[TechnologySystem]:
        """Find technology systems within a specified maturity range."""
        result = []
        for tech in self.list_all():
            if hasattr(tech, 'maturity') and tech.maturity is not None:
                if min_maturity <= tech.maturity <= max_maturity:
                    result.append(tech)
        return result
    
    def find_by_compatibility(self, tech_id: str, min_compatibility: float) -> List[TechnologySystem]:
        """Find technology systems compatible with specified technology."""
        result = []
        for tech in self.list_all():
            if hasattr(tech, 'compatibility') and tech.compatibility:
                compatibility = tech.compatibility.get(tech_id)
                if compatibility is not None and compatibility >= min_compatibility:
                    result.append(tech)
        return result


class NetworkXIndicatorRepository(NetworkXNodeRepository[Indicator], IndicatorRepository):
    def __init__(self, graph: nx.MultiDiGraph):
        super().__init__(graph, Indicator)
    
    def find_by_value_category(self, category: ValueCategory) -> List[Indicator]:
        """Find indicators by value category."""
        return self.query({"value_category": category})
    
    def find_by_value_range(self, min_value: float, max_value: float) -> List[Indicator]:
        """Find indicators within a specific value range."""
        result = []
        for indicator in self.list_all():
            if hasattr(indicator, 'current_value') and indicator.current_value is not None:
                if min_value <= indicator.current_value <= max_value:
                    result.append(indicator)
        return result
    
    def find_below_threshold(self, threshold_key: str, threshold_value: float) -> List[Indicator]:
        """Find indicators below a specified threshold."""
        result = []
        for indicator in self.list_all():
            if hasattr(indicator, 'threshold_values') and indicator.threshold_values:
                stored_threshold = indicator.threshold_values.get(threshold_key)
                if (stored_threshold is not None and 
                    hasattr(indicator, 'current_value') and 
                    indicator.current_value is not None and 
                    indicator.current_value < threshold_value):
                    result.append(indicator)
        return result


class NetworkXRelationshipRepository(RelationshipRepository):
    """Repository for Relationship entities using NetworkX."""
    
    def __init__(self, graph: nx.MultiDiGraph):
        self.graph = graph
    
    def create(self, entity: Relationship) -> Relationship:
        """Create a relationship in the graph."""
        if not self.graph.has_node(entity.source_id) or not self.graph.has_node(entity.target_id):
            raise ValueError("Source or target node does not exist")
        
        self.graph.add_edge(
            entity.source_id, 
            entity.target_id, 
            key=entity.id,
            relationship=entity,
            kind=entity.kind.name,
            weight=entity.weight or 0.0
        )
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[Relationship]:
        """Read a relationship by ID."""
        for u, v, key, data in self.graph.edges(keys=True, data=True):
            if key == id:
                return data.get('relationship')
        return None
    
    def update(self, entity: Relationship) -> Relationship:
        """Update a relationship."""
        for u, v, key, data in self.graph.edges(keys=True, data=True):
            if key == entity.id:
                data['relationship'] = entity
                data['kind'] = entity.kind.name
                data['weight'] = entity.weight or 0.0
                return entity
        
        raise ValueError(f"No relationship with id {entity.id} exists")
    
    def delete(self, id: uuid.UUID) -> bool:
        """Delete a relationship by ID."""
        for u, v, key in list(self.graph.edges(keys=True)):
            if key == id:
                self.graph.remove_edge(u, v, key)
                return True
        return False
    
    def list_all(self) -> List[Relationship]:
        """List all relationships."""
        result = []
        for _, _, data in self.graph.edges(data=True):
            if 'relationship' in data:
                result.append(data['relationship'])
        return result
    
    def query(self, filters: Dict[str, Any]) -> List[Relationship]:
        """Query relationships based on filters."""
        result = []
        for _, _, data in self.graph.edges(data=True):
            if 'relationship' not in data:
                continue
            
            entity = data['relationship']
            match = True
            
            for key, value in filters.items():
                if not hasattr(entity, key) or getattr(entity, key) != value:
                    match = False
                    break
            
            if match:
                result.append(entity)
        
        return result
    
    def find_by_nodes(self, source_id: uuid.UUID, target_id: uuid.UUID) -> List[Relationship]:
        """Find relationships between specific nodes."""
        result = []
        if self.graph.has_edge(source_id, target_id):
            edge_data = self.graph.get_edge_data(source_id, target_id)
            for key, data in edge_data.items():
                if 'relationship' in data:
                    result.append(data['relationship'])
        return result
    
    def find_by_source(self, source_id: uuid.UUID) -> List[Relationship]:
        """Find relationships originating from a source node."""
        result = []
        for _, _, data in self.graph.out_edges(source_id, data=True):
            if 'relationship' in data:
                result.append(data['relationship'])
        return result
    
    def find_by_target(self, target_id: uuid.UUID) -> List[Relationship]:
        """Find relationships targeting a specific node."""
        result = []
        for _, _, data in self.graph.in_edges(target_id, data=True):
            if 'relationship' in data:
                result.append(data['relationship'])
        return result
    
    def find_by_kind(self, kind: RelationshipKind) -> List[Relationship]:
        """Find relationships of a specific kind."""
        return self.query({'kind': kind})
    
    def find_by_certainty_range(self, min_certainty: float, max_certainty: float) -> List[Relationship]:
        """Find relationships within a specific certainty range."""
        result = []
        for _, _, data in self.graph.edges(data=True):
            if 'relationship' not in data:
                continue
            
            relationship = data['relationship']
            if (hasattr(relationship, 'certainty') and 
                relationship.certainty is not None and
                min_certainty <= relationship.certainty <= max_certainty):
                result.append(relationship)
        
        return result
    
    def find_high_variability(self, threshold: float) -> List[Relationship]:
        """Find relationships with variability above threshold."""
        result = []
        for _, _, data in self.graph.edges(data=True):
            if 'relationship' not in data:
                continue
            
            relationship = data['relationship']
            if (hasattr(relationship, 'variability') and 
                relationship.variability is not None and
                relationship.variability > threshold):
                result.append(relationship)
        
        return result


class NetworkXGraphRepository(GraphRepository):
    """Repository for complete SFM graphs using NetworkX."""
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self._setup_repositories()
    
    def _setup_repositories(self):
        """Setup individual repositories that share the same graph."""
        # Node repositories
        self.actor_repo = NetworkXActorRepository(self.graph)
        self.institution_repo = NetworkXInstitutionRepository(self.graph)
        self.policy_repo = NetworkXPolicyRepository(self.graph)
        self.resource_repo = NetworkXResourceRepository(self.graph)
        self.process_repo = NetworkXProcessRepository(self.graph)
        self.flow_repo = NetworkXFlowRepository(self.graph)
        self.belief_system_repo = NetworkXBeliefSystemRepository(self.graph)
        self.technology_system_repo = NetworkXTechnologySystemRepository(self.graph)
        self.indicator_repo = NetworkXIndicatorRepository(self.graph)
        
        # Relationship repository
        self.relationship_repo = NetworkXRelationshipRepository(self.graph)
    
    def save_graph(self, sfm_graph: SFMGraph) -> None:
        """Save a complete SFM graph."""
        self.clear_graph()
        
        # Add all nodes
        for actor in sfm_graph.actors.values():
            self.actor_repo.create(actor)
        
        for institution in sfm_graph.institutions.values():
            if isinstance(institution, Policy):
                self.policy_repo.create(institution)
            else:
                self.institution_repo.create(institution)
        
        for resource in sfm_graph.resources.values():
            self.resource_repo.create(resource)
        
        for process in sfm_graph.processes.values():
            self.process_repo.create(process)
        
        for flow in sfm_graph.flows.values():
            self.flow_repo.create(flow)
        
        # Add specialized node types if they exist in the graph
        if hasattr(sfm_graph, 'belief_systems'):
            for belief_system in sfm_graph.belief_systems.values():
                self.belief_system_repo.create(belief_system)
        
        if hasattr(sfm_graph, 'technology_systems'):
            for tech_system in sfm_graph.technology_systems.values():
                self.technology_system_repo.create(tech_system)
        
        if hasattr(sfm_graph, 'indicators'):
            for indicator in sfm_graph.indicators.values():
                self.indicator_repo.create(indicator)
        
        # Add all relationships
        for relationship in sfm_graph.relationships.values():
            try:
                self.relationship_repo.create(relationship)
            except ValueError:
                # Skip relationships where source or target doesn't exist
                continue
    
    def load_graph(self, graph_id: Optional[str] = None) -> SFMGraph:
        """Load a complete SFM graph."""
        sfm_graph = SFMGraph()
        
        # Load all nodes
        for actor in self.actor_repo.list_all():
            sfm_graph.actors[actor.id] = actor
        
        for institution in self.institution_repo.list_all():
            if isinstance(institution, Policy):
                if not hasattr(sfm_graph, 'policies'):
                    sfm_graph.policies = {}
                sfm_graph.policies[institution.id] = institution
            else:
                sfm_graph.institutions[institution.id] = institution
        
        for resource in self.resource_repo.list_all():
            sfm_graph.resources[resource.id] = resource
        
        for process in self.process_repo.list_all():
            sfm_graph.processes[process.id] = process
        
        for flow in self.flow_repo.list_all():
            sfm_graph.flows[flow.id] = flow
        
        # Load specialized node types
        belief_systems = self.belief_system_repo.list_all()
        if belief_systems:
            sfm_graph.belief_systems = {bs.id: bs for bs in belief_systems}
        
        tech_systems = self.technology_system_repo.list_all()
        if tech_systems:
            sfm_graph.technology_systems = {ts.id: ts for ts in tech_systems}
        
        indicators = self.indicator_repo.list_all()
        if indicators:
            sfm_graph.indicators = {ind.id: ind for ind in indicators}
        
        # Load all relationships
        for relationship in self.relationship_repo.list_all():
            sfm_graph.relationships[relationship.id] = relationship
        
        return sfm_graph
    
    def clear_graph(self) -> None:
        """Clear all graph data."""
        self.graph.clear()
    
    def find_paths(self, source_id: uuid.UUID, target_id: uuid.UUID, 
                   max_length: Optional[int] = None) -> List[List[uuid.UUID]]:
        """Find all paths between source and target nodes."""
        if not self.graph.has_node(source_id) or not self.graph.has_node(target_id):
            return []
        
        try:
            paths = []
            for path in nx.all_simple_paths(self.graph, source_id, target_id, cutoff=max_length):
                paths.append(list(path))
            return paths
        except nx.NetworkXNoPath:
            return []
    
    def detect_cycles(self, start_node_id: Optional[uuid.UUID] = None) -> List[List[uuid.UUID]]:
        """Detect cycles in the graph."""
        cycles = list(nx.simple_cycles(self.graph))
        
        if start_node_id is not None:
            # Filter cycles that include the start node
            cycles = [cycle for cycle in cycles if start_node_id in cycle]
        
        return cycles
    
    def get_subgraph(self, node_ids: List[uuid.UUID]) -> SFMGraph:
        """Extract a subgraph containing only specified nodes and their relationships."""
        # Create subgraph
        subgraph = self.graph.subgraph(node_ids).copy()
        
        # Create a new repository with this subgraph
        repo = NetworkXGraphRepository()
        repo.graph = subgraph
        repo._setup_repositories()
        
        # Convert to SFMGraph and return
        return repo.load_graph()
    
    def calculate_centrality(self, centrality_type: str = "betweenness") -> Dict[uuid.UUID, float]:
        """Calculate centrality measures for nodes."""
        if centrality_type == "betweenness":
            return dict(nx.betweenness_centrality(self.graph))
        elif centrality_type == "closeness":
            return dict(nx.closeness_centrality(self.graph))
        elif centrality_type == "degree":
            return dict(nx.degree_centrality(self.graph))
        elif centrality_type == "eigenvector":
            try:
                return dict(nx.eigenvector_centrality(self.graph))
            except nx.NetworkXError:
                # Handle convergence issues
                return {}
        else:
            raise ValueError(f"Unsupported centrality type: {centrality_type}")
    
    def find_communities(self) -> List[List[uuid.UUID]]:
        """Detect communities/clusters in the graph."""
        # Convert to undirected for community detection
        undirected = self.graph.to_undirected()
        
        try:
            # Use Louvain method if available
            import networkx.algorithms.community as nx_comm
            communities = nx_comm.louvain_communities(undirected)
            return [list(community) for community in communities] # type: ignore
        except ImportError:
            # Fallback to connected components
            return [list(component) for component in nx.connected_components(undirected)]
    
    def get_delivery_matrix(self) -> Dict[uuid.UUID, Dict[uuid.UUID, float]]:
        """Generate the delivery matrix representation of flows."""
        delivery_matrix = {}
        
        # Initialize empty dictionaries for each node
        for node_id in self.graph.nodes():
            delivery_matrix[node_id] = {}
        
        # Fill in the matrix with flow weights
        for source_id, target_id, data in self.graph.edges(data=True):
            relationship = data.get('relationship')
            if relationship is not None:
                # Use weight if available, otherwise 1.0 as default
                weight = relationship.weight if hasattr(relationship, 'weight') and relationship.weight is not None else 1.0
                delivery_matrix[source_id][target_id] = weight
        
        return delivery_matrix
    
    def identify_feedback_loops(self) -> List[FeedbackLoop]:
        """Identify feedback loops in the system."""
        cycles = self.detect_cycles()
        feedback_loops = []
        
        for cycle_idx, cycle in enumerate(cycles):
            # For each cycle, find the relationships that form it
            relationships = []
            for i in range(len(cycle)):
                source_id = cycle[i]
                target_id = cycle[(i + 1) % len(cycle)]  # Wrap around to first node
                
                # Find relationships between these nodes
                if self.graph.has_edge(source_id, target_id):
                    edge_data = self.graph.get_edge_data(source_id, target_id)
                    for key, data in edge_data.items():
                        if 'relationship' in data:
                            relationships.append(data['relationship'].id)
                            break  # Take the first relationship found
            
            # Calculate the cycle strength (product of weights)
            strength = 1.0
            negative_count = 0
            
            for rel_id in relationships:
                rel = self.relationship_repo.read(rel_id)
                if rel and hasattr(rel, 'weight') and rel.weight is not None:
                    strength *= abs(rel.weight)
                    if rel.weight < 0:
                        negative_count += 1
            
            # Determine if reinforcing (even number of negative relationships) or balancing
            loop_type = "reinforcing" if negative_count % 2 == 0 else "balancing"
            
            # Create a FeedbackLoop object
            loop = FeedbackLoop(
                label=f"Feedback Loop {cycle_idx + 1}",
                relationships=relationships,
                type=loop_type,
                strength=strength
            )
            feedback_loops.append(loop)
        
        return feedback_loops
    
    def extract_belief_network(self) -> SFMGraph:
        """Extract subgraph of belief systems and their relationships."""
        # Find all nodes that are belief systems
        belief_nodes = []
        for node_id, data in self.graph.nodes(data=True):
            entity = data.get('entity')
            if entity and isinstance(entity, BeliefSystem):
                belief_nodes.append(node_id)
        
        # Find nodes directly connected to belief systems
        connected_nodes = set(belief_nodes)
        for belief_id in belief_nodes:
            for node_id in self.graph.successors(belief_id):
                connected_nodes.add(node_id)
            for node_id in self.graph.predecessors(belief_id):
                connected_nodes.add(node_id)
        
        # Extract the subgraph
        return self.get_subgraph(list(connected_nodes))
    
    def extract_policy_network(self) -> SFMGraph:
        """Extract subgraph of policies and affected entities."""
        # Find all nodes that are policies
        policy_nodes = []
        for node_id, data in self.graph.nodes(data=True):
            entity = data.get('entity')
            if entity and isinstance(entity, Policy):
                policy_nodes.append(node_id)
        
        # Find nodes directly connected to policies
        connected_nodes = set(policy_nodes)
        for policy_id in policy_nodes:
            for node_id in self.graph.successors(policy_id):
                connected_nodes.add(node_id)
            for node_id in self.graph.predecessors(policy_id):
                connected_nodes.add(node_id)
        
        # Extract the subgraph
        return self.get_subgraph(list(connected_nodes))
    
    def calculate_indicator_impacts(self, policy_id: uuid.UUID) -> Dict[uuid.UUID, float]:
        """Calculate how a policy affects various indicators."""
        impacts = {}
        
        # Check if policy exists
        if not self.graph.has_node(policy_id):
            return impacts
        
        # Find all indicators in the graph
        indicators = []
        for node_id, data in self.graph.nodes(data=True):
            entity = data.get('entity')
            if entity and isinstance(entity, Indicator):
                indicators.append(node_id)
        
        # For each indicator, find paths from policy to indicator
        for indicator_id in indicators:
            paths = self.find_paths(policy_id, indicator_id)
            if not paths:
                impacts[indicator_id] = 0.0  # No impact if no path exists
                continue
            
            # Calculate impact as the sum of path impacts
            total_impact = 0.0
            for path in paths:
                path_impact = 1.0
                # Multiply weights along the path
                for i in range(len(path) - 1):
                    source_id = path[i]
                    target_id = path[i + 1]
                    if self.graph.has_edge(source_id, target_id):
                        edge_data = self.graph.get_edge_data(source_id, target_id)
                        # Use the first relationship found
                        for key, data in edge_data.items():
                            rel = data.get('relationship')
                            if rel and hasattr(rel, 'weight') and rel.weight is not None:
                                path_impact *= rel.weight
                                break
                
                total_impact += path_impact
            
            impacts[indicator_id] = total_impact
        
        return impacts
    
    def find_critical_nodes(self, criteria: str = "betweenness") -> List[uuid.UUID]:
        """Identify critical nodes based on specified criteria."""
        if criteria == "betweenness":
            centrality = self.calculate_centrality("betweenness")
        elif criteria == "degree":
            centrality = self.calculate_centrality("degree")
        else:
            raise ValueError(f"Unsupported criteria: {criteria}")
        
        # Sort nodes by centrality value
        sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        
        # Return node IDs in descending order of centrality
        return [node_id for node_id, _ in sorted_nodes]


# Standalone implementations for repositories that don't use the graph directly
class NetworkXFeedbackLoopRepository(FeedbackLoopRepository):
    """Repository for FeedbackLoop entities using an in-memory dictionary."""
    
    def __init__(self, graph: nx.MultiDiGraph):
        self.graph = graph
        self.loops = {}  # Dictionary to store feedback loops by ID
        
    def create(self, entity: FeedbackLoop) -> FeedbackLoop:
        """Create a new feedback loop."""
        if entity.id in self.loops:
            raise ValueError(f"FeedbackLoop with id {entity.id} already exists")
        
        # Verify all relationships exist in the graph
        for rel_id in entity.relationships:
            if not self._relationship_exists(rel_id):
                raise ValueError(f"Relationship {rel_id} not found in the graph")
        
        self.loops[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[FeedbackLoop]:
        """Retrieve a feedback loop by ID."""
        return self.loops.get(id)
    
    def update(self, entity: FeedbackLoop) -> FeedbackLoop:
        """Update a feedback loop."""
        if entity.id not in self.loops:
            raise ValueError(f"No FeedbackLoop with id {entity.id} exists")
        
        # Verify all relationships exist in the graph
        for rel_id in entity.relationships:
            if not self._relationship_exists(rel_id):
                raise ValueError(f"Relationship {rel_id} not found in the graph")
        
        self.loops[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        """Delete a feedback loop by ID."""
        if id in self.loops:
            del self.loops[id]
            return True
        return False
    
    def list_all(self) -> List[FeedbackLoop]:
        """Return all feedback loops."""
        return list(self.loops.values())
    
    def query(self, filters: Dict[str, Any]) -> List[FeedbackLoop]:
        """Query feedback loops based on property filters."""
        result = []
        for loop in self.loops.values():
            match = True
            
            for key, value in filters.items():
                if not hasattr(loop, key) or getattr(loop, key) != value:
                    match = False
                    break
            
            if match:
                result.append(loop)
        
        return result
    
    def find_by_type(self, loop_type: str) -> List[FeedbackLoop]:
        """Find feedback loops by type (reinforcing or balancing)."""
        return self.query({"type": loop_type})
    
    def find_containing_relationship(self, relationship_id: uuid.UUID) -> List[FeedbackLoop]:
        """Find feedback loops containing a specific relationship."""
        result = []
        for loop in self.loops.values():
            if relationship_id in loop.relationships:
                result.append(loop)
        return result
    
    def find_by_strength_range(self, min_strength: float, max_strength: float) -> List[FeedbackLoop]:
        """Find feedback loops within a specific strength range."""
        result = []
        for loop in self.loops.values():
            if hasattr(loop, 'strength') and loop.strength is not None:
                if min_strength <= loop.strength <= max_strength:
                    result.append(loop)
        return result
    
    def _relationship_exists(self, relationship_id: uuid.UUID) -> bool:
        """Check if a relationship exists in the graph."""
        for _, _, key, _ in self.graph.edges(keys=True, data=True):
            if key == relationship_id:
                return True
        return False


class NetworkXAnalyticalContextRepository(AnalyticalContextRepository):
    """Repository for AnalyticalContext metadata using an in-memory dictionary."""
    
    def __init__(self):
        self.contexts = {}  # Dictionary to store analytical contexts by ID
    
    def create(self, entity: AnalyticalContext) -> AnalyticalContext:
        """Create a new analytical context."""
        if entity.id in self.contexts:
            raise ValueError(f"AnalyticalContext with id {entity.id} already exists")
        
        self.contexts[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[AnalyticalContext]:
        """Retrieve an analytical context by ID."""
        return self.contexts.get(id)
    
    def update(self, entity: AnalyticalContext) -> AnalyticalContext:
        """Update an analytical context."""
        if entity.id not in self.contexts:
            raise ValueError(f"No AnalyticalContext with id {entity.id} exists")
        
        self.contexts[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        """Delete an analytical context by ID."""
        if id in self.contexts:
            del self.contexts[id]
            return True
        return False
    
    def list_all(self) -> List[AnalyticalContext]:
        """Return all analytical contexts."""
        return list(self.contexts.values())
    
    def query(self, filters: Dict[str, Any]) -> List[AnalyticalContext]:
        """Query analytical contexts based on property filters."""
        result = []
        for context in self.contexts.values():
            match = True
            
            for key, value in filters.items():
                if not hasattr(context, key) or getattr(context, key) != value:
                    match = False
                    break
            
            if match:
                result.append(context)
        
        return result
    
    def find_by_method(self, method: str) -> List[AnalyticalContext]:
        """Find analytical contexts using a specific method."""
        result = []
        for context in self.contexts.values():
            if hasattr(context, 'methods_used') and method in context.methods_used:
                result.append(context)
        return result


class NetworkXSystemPropertyRepository(SystemPropertyRepository):
    """Repository for SystemProperty entities using an in-memory dictionary."""
    
    def __init__(self):
        self.properties = {}  # Dictionary to store system properties by ID
    
    def create(self, entity: SystemProperty) -> SystemProperty:
        """Create a new system property."""
        if entity.id in self.properties:
            raise ValueError(f"SystemProperty with id {entity.id} already exists")
        
        self.properties[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[SystemProperty]:
        """Retrieve a system property by ID."""
        return self.properties.get(id)
    
    def update(self, entity: SystemProperty) -> SystemProperty:
        """Update a system property."""
        if entity.id not in self.properties:
            raise ValueError(f"No SystemProperty with id {entity.id} exists")
        
        self.properties[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        """Delete a system property by ID."""
        if id in self.properties:
            del self.properties[id]
            return True
        return False
    
    def list_all(self) -> List[SystemProperty]:
        """Return all system properties."""
        return list(self.properties.values())
    
    def query(self, filters: Dict[str, Any]) -> List[SystemProperty]:
        """Query system properties based on property filters."""
        result = []
        for prop in self.properties.values():
            match = True
            
            for key, value in filters.items():
                if not hasattr(prop, key) or getattr(prop, key) != value:
                    match = False
                    break
            
            if match:
                result.append(prop)
        
        return result
    
    def find_by_affected_node(self, node_id: uuid.UUID) -> List[SystemProperty]:
        """Find system properties affecting a specific node."""
        result = []
        for prop in self.properties.values():
            if hasattr(prop, 'affected_nodes') and node_id in prop.affected_nodes:
                result.append(prop)
        return result
    
    def find_by_contributing_relationship(self, relationship_id: uuid.UUID) -> List[SystemProperty]:
        """Find system properties influenced by a specific relationship."""
        result = []
        for prop in self.properties.values():
            if hasattr(prop, 'contributing_relationships') and relationship_id in prop.contributing_relationships:
                result.append(prop)
        return result