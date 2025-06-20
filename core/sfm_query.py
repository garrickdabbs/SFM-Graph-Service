"""
Abstract query layer for Social Fabric Matrix (SFM) analysis.
Provides high-level analytical queries with support for different graph storage backends.
Default implementation uses NetworkX for graph analysis.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Tuple, Any, Union
import uuid
from dataclasses import dataclass
from enum import Enum

from core.sfm_models import (
    Node,
    Actor,
    Institution,
    Resource,
    Policy,
    Flow,
    Relationship,
    SFMGraph,
    RelationshipKind,
)
from core.sfm_enums import ResourceType, FlowNature


class AnalysisType(Enum):
    """Types of SFM analysis supported."""

    CENTRALITY = "centrality"
    INFLUENCE = "influence"
    DEPENDENCY = "dependency"
    FLOW_ANALYSIS = "flow_analysis"
    NETWORK_STRUCTURE = "network_structure"
    POLICY_IMPACT = "policy_impact"
    SCENARIO_COMPARISON = "scenario_comparison"


@dataclass
class QueryResult:
    """Container for query results with metadata."""

    data: Any
    query_type: str
    parameters: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: str


@dataclass
class NodeMetrics:
    """Metrics for individual nodes in the SFM."""

    node_id: uuid.UUID
    centrality_scores: Dict[str, float]
    influence_score: float
    dependency_score: float
    connectivity: int
    node_type: str


@dataclass
class FlowAnalysis:
    """Analysis results for resource/value flows."""

    flow_paths: List[List[uuid.UUID]]
    bottlenecks: List[uuid.UUID]
    flow_volumes: Dict[uuid.UUID, float]
    efficiency_metrics: Dict[str, float]


class SFMQueryEngine(ABC):
    """Abstract base class for SFM analytical queries."""

    def __init__(self, graph: SFMGraph):
        self.graph = graph

    # ─── NODE ANALYSIS ───

    @abstractmethod
    def get_node_centrality(
        self, node_id: uuid.UUID, centrality_type: str = "betweenness"
    ) -> float:
        """Calculate centrality measures for a node."""
        pass

    @abstractmethod
    def get_most_central_nodes(
        self,
        node_type: Optional[type] = None,
        centrality_type: str = "betweenness",
        limit: int = 10,
    ) -> List[Tuple[uuid.UUID, float]]:
        """Get the most central nodes by type."""
        pass

    @abstractmethod
    def get_node_neighbors(
        self,
        node_id: uuid.UUID,
        relationship_kinds: Optional[List[RelationshipKind]] = None,
        distance: int = 1,
    ) -> List[uuid.UUID]:
        """Get neighboring nodes within specified distance."""
        pass

    # ─── RELATIONSHIP ANALYSIS ───

    @abstractmethod
    def find_shortest_path(
        self,
        source_id: uuid.UUID,
        target_id: uuid.UUID,
        relationship_kinds: Optional[List[RelationshipKind]] = None,
    ) -> Optional[List[uuid.UUID]]:
        """Find shortest path between two nodes."""
        pass

    @abstractmethod
    def get_relationship_strength(
        self, source_id: uuid.UUID, target_id: uuid.UUID
    ) -> float:
        """Calculate aggregate relationship strength between nodes."""
        pass

    @abstractmethod
    def find_cycles(self, max_length: int = 10) -> List[List[uuid.UUID]]:
        """Find cycles in the graph (feedback loops)."""
        pass

    # ─── FLOW ANALYSIS ───

    @abstractmethod
    def trace_resource_flows(
        self,
        resource_type: ResourceType,
        source_actors: Optional[List[uuid.UUID]] = None,
    ) -> FlowAnalysis:
        """Trace flows of specific resource types through the network."""
        pass

    @abstractmethod
    def identify_bottlenecks(self, flow_type: FlowNature) -> List[uuid.UUID]:
        """Identify bottleneck nodes in flow networks."""
        pass

    @abstractmethod
    def calculate_flow_efficiency(
        self, source_id: uuid.UUID, target_id: uuid.UUID
    ) -> float:
        """Calculate efficiency of flows between nodes."""
        pass

    # ─── POLICY ANALYSIS ───

    @abstractmethod
    def analyze_policy_impact(
        self, policy_id: uuid.UUID, impact_radius: int = 3
    ) -> Dict[str, Any]:
        """Analyze the network impact of a policy intervention."""
        pass

    @abstractmethod
    def identify_policy_targets(self, policy_id: uuid.UUID) -> List[uuid.UUID]:
        """Identify nodes directly and indirectly affected by a policy."""
        pass

    @abstractmethod
    def compare_policy_scenarios(
        self, scenario_graphs: List[SFMGraph]
    ) -> Dict[str, Any]:
        """Compare multiple policy scenarios."""
        pass

    # ─── STRUCTURAL ANALYSIS ───

    @abstractmethod
    def get_network_density(self) -> float:
        """Calculate overall network density."""
        pass

    @abstractmethod
    def identify_communities(
        self, algorithm: str = "louvain"
    ) -> Dict[int, List[uuid.UUID]]:
        """Identify communities/clusters in the network."""
        pass

    @abstractmethod
    def get_structural_holes(self) -> List[uuid.UUID]:
        """Identify nodes that bridge structural holes."""
        pass

    # ─── COMPOSITE QUERIES ───

    @abstractmethod
    def comprehensive_node_analysis(self, node_id: uuid.UUID) -> NodeMetrics:
        """Comprehensive analysis of a single node."""
        pass

    @abstractmethod
    def system_vulnerability_analysis(self) -> Dict[str, Any]:
        """Analyze system-wide vulnerabilities and resilience."""
        pass


class NetworkXSFMQueryEngine(SFMQueryEngine):
    """NetworkX-based implementation of SFM query engine."""

    def __init__(self, graph: SFMGraph):
        super().__init__(graph)
        self.nx_graph = self._build_networkx_graph()

    def _build_networkx_graph(self):
        """Convert SFMGraph to NetworkX graph for analysis."""
        import networkx as nx

        # Create directed multigraph to handle multiple relationships
        G = nx.MultiDiGraph()

        # Add all nodes
        for node in self.graph:
            G.add_node(node.id, data=node, type=type(node).__name__)

        # Add all relationships as edges
        for rel in self.graph.relationships.values():
            G.add_edge(
                rel.source_id,
                rel.target_id,
                key=rel.id,
                data=rel,
                kind=rel.kind,
                weight=rel.weight or 1.0,
            )

        return G

    def get_node_centrality(
        self, node_id: uuid.UUID, centrality_type: str = "betweenness"
    ) -> float:
        """Calculate centrality measures for a node."""
        import networkx as nx

        if centrality_type == "betweenness":
            centrality = nx.betweenness_centrality(self.nx_graph)
        elif centrality_type == "closeness":
            centrality = nx.closeness_centrality(self.nx_graph)
        elif centrality_type == "degree":
            centrality = nx.degree_centrality(self.nx_graph)
        elif centrality_type == "eigenvector":
            try:
                centrality = nx.eigenvector_centrality(self.nx_graph, max_iter=1000)
            except nx.NetworkXError:
                # Fallback for convergence issues
                centrality = nx.degree_centrality(self.nx_graph)
        else:
            raise ValueError(f"Unsupported centrality type: {centrality_type}")

        return centrality.get(node_id, 0.0)

    def get_most_central_nodes(
        self,
        node_type: Optional[type] = None,
        centrality_type: str = "betweenness",
        limit: int = 10,
    ) -> List[Tuple[uuid.UUID, float]]:
        """Get the most central nodes by type."""
        import networkx as nx

        # Calculate centrality for all nodes
        if centrality_type == "betweenness":
            centrality = nx.betweenness_centrality(self.nx_graph)
        elif centrality_type == "closeness":
            centrality = nx.closeness_centrality(self.nx_graph)
        elif centrality_type == "degree":
            centrality = nx.degree_centrality(self.nx_graph)
        elif centrality_type == "eigenvector":
            try:
                centrality = nx.eigenvector_centrality(self.nx_graph, max_iter=1000)
            except nx.NetworkXError:
                centrality = nx.degree_centrality(self.nx_graph)
        else:
            raise ValueError(f"Unsupported centrality type: {centrality_type}")

        # Filter by node type if specified
        if node_type:
            filtered_centrality = {
                node_id: score
                for node_id, score in centrality.items()
                if isinstance(self.nx_graph.nodes[node_id]["data"], node_type)
            }
        else:
            filtered_centrality = centrality

        # Sort and return top nodes
        sorted_nodes = sorted(
            filtered_centrality.items(), key=lambda x: x[1], reverse=True
        )
        return sorted_nodes[:limit]

    def get_node_neighbors(
        self,
        node_id: uuid.UUID,
        relationship_kinds: Optional[List[RelationshipKind]] = None,
        distance: int = 1,
    ) -> List[uuid.UUID]:
        """Get neighboring nodes within specified distance."""
        import networkx as nx

        if distance == 1:
            # Direct neighbors
            if relationship_kinds:
                neighbors = []
                for neighbor in self.nx_graph.neighbors(node_id):
                    for edge_data in self.nx_graph[node_id][neighbor].values():
                        if edge_data.get("kind") in relationship_kinds:
                            neighbors.append(neighbor)
                            break
                return list(set(neighbors))
            else:
                return list(self.nx_graph.neighbors(node_id))
        else:
            # Multi-hop neighbors
            if relationship_kinds:
                # Create subgraph with only desired relationship types
                edges_to_keep = []
                for u, v, key, data in self.nx_graph.edges(keys=True, data=True):
                    if data.get("kind") in relationship_kinds:
                        edges_to_keep.append((u, v, key))

                subgraph = self.nx_graph.edge_subgraph(edges_to_keep)
                try:
                    neighbors = set()
                    for target in subgraph.nodes():
                        if target != node_id:
                            try:
                                path_length = nx.shortest_path_length(
                                    subgraph, node_id, target
                                )
                                if path_length <= distance:
                                    neighbors.add(target)
                            except nx.NetworkXNoPath:
                                continue
                    return list(neighbors)
                except nx.NetworkXError:
                    return []
            else:
                # All relationships
                try:
                    ego_graph = nx.ego_graph(self.nx_graph, node_id, radius=distance)
                    return [n for n in ego_graph.nodes() if n != node_id]
                except nx.NetworkXError:
                    return []

    def find_shortest_path(
        self,
        source_id: uuid.UUID,
        target_id: uuid.UUID,
        relationship_kinds: Optional[List[RelationshipKind]] = None,
    ) -> Optional[List[uuid.UUID]]:
        """Find shortest path between two nodes."""
        import networkx as nx

        try:
            if relationship_kinds:
                # Create subgraph with only desired relationship types
                edges_to_keep = []
                for u, v, key, data in self.nx_graph.edges(keys=True, data=True):
                    if data.get("kind") in relationship_kinds:
                        edges_to_keep.append((u, v, key))

                subgraph = self.nx_graph.edge_subgraph(edges_to_keep)
                path = nx.shortest_path(subgraph, source_id, target_id)
                if isinstance(path, list):
                    return path
                else:
                    return None
            else:
                path = nx.shortest_path(self.nx_graph, source_id, target_id)
                if isinstance(path, list):
                    return path
                else:
                    return None
        except nx.NetworkXNoPath:
            return None

    def get_relationship_strength(
        self, source_id: uuid.UUID, target_id: uuid.UUID
    ) -> float:
        """Calculate aggregate relationship strength between nodes."""
        if not self.nx_graph.has_edge(source_id, target_id):
            return 0.0

        total_weight = 0.0
        edge_count = 0

        for edge_data in self.nx_graph[source_id][target_id].values():
            weight = edge_data.get("weight", 1.0)
            total_weight += weight
            edge_count += 1

        return total_weight / edge_count if edge_count > 0 else 0.0

    def find_cycles(self, max_length: int = 10) -> List[List[uuid.UUID]]:
        """Find cycles in the graph (feedback loops)."""
        import networkx as nx

        try:
            cycles = []
            # Find simple cycles up to max_length
            for cycle in nx.simple_cycles(self.nx_graph):
                if len(cycle) <= max_length:
                    cycles.append(cycle)
            return cycles
        except nx.NetworkXError:
            return []

    def trace_resource_flows(
        self,
        resource_type: ResourceType,
        source_actors: Optional[List[uuid.UUID]] = None,
    ) -> FlowAnalysis:
        """Trace flows of specific resource types through the network."""
        # This is a simplified implementation - would need more sophisticated flow analysis
        flow_paths = []
        bottlenecks = []
        flow_volumes = {}

        # Find resource nodes of the specified type
        resource_nodes = [
            node_id
            for node_id, node_data in self.nx_graph.nodes(data=True)
            if (
                isinstance(node_data["data"], Resource)
                and node_data["data"].rtype == resource_type
            )
        ]

        # Trace flows from resource nodes
        for resource_id in resource_nodes:
            # Find flows connected to this resource
            for neighbor in self.nx_graph.neighbors(resource_id):
                for edge_data in self.nx_graph[resource_id][neighbor].values():
                    if isinstance(edge_data["data"], Relationship):
                        rel = edge_data["data"]
                        if rel.kind in [
                            RelationshipKind.PRODUCES,
                            RelationshipKind.USES,
                            RelationshipKind.EXCHANGES_WITH,
                        ]:
                            flow_volumes[rel.id] = rel.weight or 1.0

        return FlowAnalysis(
            flow_paths=flow_paths,
            bottlenecks=bottlenecks,
            flow_volumes=flow_volumes,
            efficiency_metrics={},
        )

    def identify_bottlenecks(self, flow_type: FlowNature) -> List[uuid.UUID]:
        """Identify bottleneck nodes in flow networks."""
        import networkx as nx

        # Use betweenness centrality as a proxy for bottlenecks
        centrality = nx.betweenness_centrality(self.nx_graph)

        # Get top 10% of nodes by centrality
        threshold = sorted(centrality.values())[-max(1, len(centrality) // 10)]
        bottlenecks = [
            node_id for node_id, score in centrality.items() if score >= threshold
        ]

        return bottlenecks

    def calculate_flow_efficiency(
        self, source_id: uuid.UUID, target_id: uuid.UUID
    ) -> float:
        """Calculate efficiency of flows between nodes."""
        try:
            shortest_path_length = (
                len(self.find_shortest_path(source_id, target_id) or []) - 1
            )
            if shortest_path_length <= 0:
                return 0.0

            # Simple efficiency metric: inverse of path length
            return 1.0 / shortest_path_length
        except:
            return 0.0

    def analyze_policy_impact(
        self, policy_id: uuid.UUID, impact_radius: int = 3
    ) -> Dict[str, Any]:
        """Analyze the network impact of a policy intervention."""
        import networkx as nx

        # Get nodes within impact radius
        try:
            ego_graph = nx.ego_graph(self.nx_graph, policy_id, radius=impact_radius)
            affected_nodes = list(ego_graph.nodes())

            # Categorize affected nodes by type
            impact_analysis = {
                "total_affected_nodes": len(affected_nodes)
                - 1,  # Exclude policy node itself
                "affected_actors": [],
                "affected_institutions": [],
                "affected_resources": [],
                "network_metrics": {
                    "density": nx.density(ego_graph),
                    "centrality": nx.betweenness_centrality(ego_graph).get(
                        policy_id, 0.0
                    ),
                },
            }

            for node_id in affected_nodes:
                if node_id == policy_id:
                    continue

                node_data = self.nx_graph.nodes[node_id]["data"]
                if isinstance(node_data, Actor):
                    impact_analysis["affected_actors"].append(node_id)
                elif isinstance(node_data, Institution):
                    impact_analysis["affected_institutions"].append(node_id)
                elif isinstance(node_data, Resource):
                    impact_analysis["affected_resources"].append(node_id)

            return impact_analysis

        except nx.NetworkXError:
            return {"error": "Policy node not found or network error"}

    def identify_policy_targets(self, policy_id: uuid.UUID) -> List[uuid.UUID]:
        """Identify nodes directly and indirectly affected by a policy."""
        targets = []

        # Direct targets (immediate neighbors)
        direct_targets = self.get_node_neighbors(policy_id, distance=1)
        targets.extend(direct_targets)

        # Indirect targets (2-hop neighbors)
        indirect_targets = self.get_node_neighbors(policy_id, distance=2)
        targets.extend([t for t in indirect_targets if t not in direct_targets])

        return list(set(targets))

    def compare_policy_scenarios(
        self, scenario_graphs: List[SFMGraph]
    ) -> Dict[str, Any]:
        """Compare multiple policy scenarios."""
        # This would require more sophisticated scenario comparison logic
        comparison = {
            "scenario_count": len(scenario_graphs),
            "node_count_comparison": [len(g) for g in scenario_graphs],
            "relationship_count_comparison": [
                len(g.relationships) for g in scenario_graphs
            ],
        }
        return comparison

    def get_network_density(self) -> float:
        """Calculate overall network density."""
        import networkx as nx

        return nx.density(self.nx_graph)

    def identify_communities(
        self, algorithm: str = "louvain"
    ) -> Dict[int, List[uuid.UUID]]:
        """Identify communities/clusters in the network."""
        # This would require community detection algorithms
        # For now, return a simple placeholder
        return {0: list(self.nx_graph.nodes())}

    def get_structural_holes(self) -> List[uuid.UUID]:
        """Identify nodes that bridge structural holes."""
        import networkx as nx

        # Use betweenness centrality as a proxy for structural holes
        centrality = nx.betweenness_centrality(self.nx_graph)

        # Nodes with high betweenness centrality often bridge structural holes
        threshold = sorted(centrality.values())[
            -max(1, len(centrality) // 20)
        ]  # Top 5%
        structural_bridges = [
            node_id for node_id, score in centrality.items() if score >= threshold
        ]

        return structural_bridges

    def comprehensive_node_analysis(self, node_id: uuid.UUID) -> NodeMetrics:
        """Comprehensive analysis of a single node."""
        centrality_scores = {
            "betweenness": self.get_node_centrality(node_id, "betweenness"),
            "closeness": self.get_node_centrality(node_id, "closeness"),
            "degree": self.get_node_centrality(node_id, "degree"),
        }

        # Calculate influence and dependency scores
        neighbors = self.get_node_neighbors(node_id)
        influence_score = len(
            [n for n in neighbors if self.nx_graph.has_edge(node_id, n)]
        )
        dependency_score = len(
            [n for n in neighbors if self.nx_graph.has_edge(n, node_id)]
        )

        return NodeMetrics(
            node_id=node_id,
            centrality_scores=centrality_scores,
            influence_score=influence_score / len(neighbors) if neighbors else 0.0,
            dependency_score=dependency_score / len(neighbors) if neighbors else 0.0,            connectivity=len(neighbors),
            node_type=type(self.nx_graph.nodes[node_id]["data"]).__name__,
        )

    def system_vulnerability_analysis(self) -> Dict[str, Any]:
        """Analyze system-wide vulnerabilities and resilience."""
        import networkx as nx

        # Convert multigraph to simple graph for clustering analysis
        simple_graph = nx.Graph(self.nx_graph.to_undirected())
        
        # Calculate various network resilience metrics
        analysis = {
            "network_density": self.get_network_density(),
            "average_clustering": nx.average_clustering(simple_graph) if simple_graph.number_of_nodes() > 0 else 0.0,
            "number_of_components": nx.number_weakly_connected_components(
                self.nx_graph
            ),
            "critical_nodes": self.get_structural_holes(),
            "bottlenecks": self.identify_bottlenecks(FlowNature.TRANSFER),
        }

        return analysis


class SFMQueryFactory:
    """Factory for creating SFM query engines."""

    @staticmethod
    def create_query_engine(
        graph: SFMGraph, backend: str = "networkx"
    ) -> SFMQueryEngine:
        """Create a query engine for the specified backend."""
        if backend.lower() == "networkx":
            return NetworkXSFMQueryEngine(graph)
        else:
            raise ValueError(f"Unsupported backend: {backend}")
