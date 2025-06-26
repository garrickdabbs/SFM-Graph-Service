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
from datetime import datetime

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

    # ═══════════════════════════════════════════════════════════════════════════
    # ENHANCED TEMPORAL ANALYSIS
    # ═══════════════════════════════════════════════════════════════════════════

    @abstractmethod
    def analyze_temporal_changes(
        self, time_slice_graphs: List[Tuple[datetime, SFMGraph]]
    ) -> Dict[str, Any]:
        """Analyze changes across multiple time slices of the graph."""
        pass

    @abstractmethod
    def detect_structural_changes(
        self, reference_graph: SFMGraph, comparison_graph: SFMGraph
    ) -> Dict[str, Any]:
        """Detect structural changes between two graph states."""
        pass

    # ═══════════════════════════════════════════════════════════════════════════
    # RISK ASSESSMENT AND VULNERABILITY ANALYSIS
    # ═══════════════════════════════════════════════════════════════════════════

    @abstractmethod
    def assess_network_vulnerabilities(self) -> Dict[str, Any]:
        """Comprehensive vulnerability assessment of the network."""
        pass

    @abstractmethod
    def simulate_node_failure_impact(
        self, node_ids: List[uuid.UUID], failure_mode: str = "cascade"
    ) -> Dict[str, Any]:
        """Simulate the impact of node failures on network connectivity."""
        pass

    # ═══════════════════════════════════════════════════════════════════════════
    # ADVANCED FLOW ANALYSIS
    # ═══════════════════════════════════════════════════════════════════════════

    @abstractmethod
    def analyze_flow_patterns(
        self, flow_type: FlowNature, time_window: Optional[Tuple[datetime, datetime]] = None
    ) -> Dict[str, Any]:
        """Analyze patterns in resource or value flows."""
        pass

    @abstractmethod
    def identify_flow_inefficiencies(self) -> Dict[str, Any]:
        """Identify inefficiencies in flow patterns."""
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

    def analyze_temporal_changes(
        self, time_slice_graphs: List[Tuple[datetime, SFMGraph]]
    ) -> Dict[str, Any]:
        """Analyze changes across multiple time slices of the graph."""
        if len(time_slice_graphs) < 2:
            return {"error": "Need at least 2 time slices for temporal analysis"}

        analysis = {
            "time_periods": len(time_slice_graphs),
            "node_evolution": {},
            "relationship_evolution": {},
            "structural_changes": {},
            "growth_metrics": {}
        }

        # Track node changes
        for i in range(1, len(time_slice_graphs)):
            prev_time, prev_graph = time_slice_graphs[i-1]
            curr_time, curr_graph = time_slice_graphs[i]
            
            prev_nodes = set(node.id for node in prev_graph)
            curr_nodes = set(node.id for node in curr_graph)
            
            added_nodes = curr_nodes - prev_nodes
            removed_nodes = prev_nodes - curr_nodes
            
            period_key = f"{prev_time.isoformat()}_{curr_time.isoformat()}"
            analysis["node_evolution"][period_key] = {
                "added": len(added_nodes),
                "removed": len(removed_nodes),
                "stable": len(prev_nodes & curr_nodes)
            }

        return analysis

    def detect_structural_changes(
        self, reference_graph: SFMGraph, comparison_graph: SFMGraph
    ) -> Dict[str, Any]:
        """Detect structural changes between two graph states."""
        import networkx as nx
        
        # Build NetworkX graphs for comparison
        ref_nx = self._build_networkx_from_graph(reference_graph)
        comp_nx = self._build_networkx_from_graph(comparison_graph)
        
        changes = {
            "density_change": nx.density(comp_nx) - nx.density(ref_nx),
            "node_count_change": comp_nx.number_of_nodes() - ref_nx.number_of_nodes(),
            "edge_count_change": comp_nx.number_of_edges() - ref_nx.number_of_edges(),
            "centrality_shifts": {},
            "new_communities": [],
            "disbanded_communities": []
        }

        # Analyze centrality shifts for common nodes
        common_nodes = set(ref_nx.nodes()) & set(comp_nx.nodes())
        if common_nodes:
            ref_centrality = nx.betweenness_centrality(ref_nx)
            comp_centrality = nx.betweenness_centrality(comp_nx)
            
            for node in common_nodes:
                shift = comp_centrality.get(node, 0) - ref_centrality.get(node, 0)
                if abs(shift) > 0.1:  # Significant shift threshold
                    changes["centrality_shifts"][str(node)] = shift

        return changes

    def assess_network_vulnerabilities(self) -> Dict[str, Any]:
        """Comprehensive vulnerability assessment of the network."""
        import networkx as nx
        
        vulnerabilities = {
            "critical_nodes": [],
            "single_points_of_failure": [],
            "fragmentation_risk": 0.0,
            "cascade_failure_risk": 0.0,
            "resilience_score": 0.0,
            "mitigation_recommendations": []
        }

        # Identify critical nodes (high betweenness centrality)
        centrality = nx.betweenness_centrality(self.nx_graph)
        critical_threshold = sorted(centrality.values())[-max(1, len(centrality) // 20)]
        vulnerabilities["critical_nodes"] = [
            {"node_id": str(node_id), "centrality": score}
            for node_id, score in centrality.items()
            if score >= critical_threshold
        ]

        # Find single points of failure (articulation points)
        if not self.nx_graph.is_directed():
            simple_graph = self.nx_graph
        else:
            simple_graph = self.nx_graph.to_undirected()
            
        articulation_points = list(nx.articulation_points(simple_graph))
        vulnerabilities["single_points_of_failure"] = [str(node) for node in articulation_points]

        # Calculate fragmentation risk
        if len(articulation_points) > 0:
            vulnerabilities["fragmentation_risk"] = len(articulation_points) / len(self.nx_graph.nodes())

        # Calculate resilience score
        connectivity = nx.node_connectivity(simple_graph) if simple_graph.number_of_nodes() > 1 else 0
        density = nx.density(self.nx_graph)
        vulnerabilities["resilience_score"] = (connectivity + density) / 2

        # Generate mitigation recommendations
        if vulnerabilities["fragmentation_risk"] > 0.1:
            vulnerabilities["mitigation_recommendations"].append(
                "High fragmentation risk detected. Consider adding redundant connections."
            )
        if len(vulnerabilities["critical_nodes"]) > len(self.nx_graph.nodes()) * 0.2:
            vulnerabilities["mitigation_recommendations"].append(
                "Many critical nodes detected. Consider distributing centrality more evenly."
            )

        return vulnerabilities

    def simulate_node_failure_impact(
        self, node_ids: List[uuid.UUID], failure_mode: str = "cascade"
    ) -> Dict[str, Any]:
        """Simulate the impact of node failures on network connectivity."""
        import networkx as nx
        
        original_components = nx.number_weakly_connected_components(self.nx_graph)
        original_largest_component = len(max(nx.weakly_connected_components(self.nx_graph), key=len))
        
        # Create a copy of the graph for simulation
        sim_graph = self.nx_graph.copy()
        
        impact_results = {
            "failed_nodes": [str(nid) for nid in node_ids],
            "failure_mode": failure_mode,
            "connectivity_impact": {},
            "isolated_nodes": [],
            "affected_components": 0,
            "cascading_failures": []
        }

        # Remove the failed nodes
        sim_graph.remove_nodes_from(node_ids)
        
        # Analyze impact
        new_components = nx.number_weakly_connected_components(sim_graph)
        if sim_graph.number_of_nodes() > 0:
            new_largest_component = len(max(nx.weakly_connected_components(sim_graph), key=len))
        else:
            new_largest_component = 0
            
        impact_results["connectivity_impact"] = {
            "original_components": original_components,
            "new_components": new_components,
            "component_increase": new_components - original_components,
            "largest_component_size_change": new_largest_component - original_largest_component,
            "connectivity_loss_percentage": 
                (original_largest_component - new_largest_component) / original_largest_component * 100
                if original_largest_component > 0 else 0
        }

        # Identify newly isolated nodes
        isolated = [node for node in sim_graph.nodes() if len(list(sim_graph.neighbors(node))) == 0]
        impact_results["isolated_nodes"] = [str(node) for node in isolated]
        
        # Simulate cascading failures if requested
        if failure_mode == "cascade":
            cascade_nodes = []
            # Simple cascade model: remove nodes that lose significant connections
            for node in list(sim_graph.nodes()):
                sim_node_degree = len(list(sim_graph.neighbors(node)))
                orig_node_degree = len(list(self.nx_graph.neighbors(node)))
                if sim_node_degree < orig_node_degree * 0.3:  # Lost 70% of connections
                    cascade_nodes.append(node)
                    sim_graph.remove_node(node)
            
            impact_results["cascading_failures"] = [str(node) for node in cascade_nodes]

        return impact_results

    def analyze_flow_patterns(
        self, flow_type: FlowNature, time_window: Optional[Tuple[datetime, datetime]] = None
    ) -> Dict[str, Any]:
        """Analyze patterns in resource or value flows."""
        flow_analysis = {
            "flow_type": flow_type.value,
            "total_flows": 0,
            "flow_distribution": {},
            "major_pathways": [],
            "flow_concentrations": [],
            "temporal_patterns": {}
        }

        # Get flows of the specified type
        relevant_flows = []
        for rel in self.nx_graph.edges(data=True):
            edge_data = rel[2]
            if hasattr(edge_data.get("data"), "flow_nature"):
                if edge_data["data"].flow_nature == flow_type:
                    relevant_flows.append(rel)

        flow_analysis["total_flows"] = len(relevant_flows)

        # Analyze flow distribution by node type
        node_flow_counts = {}
        for source, target, data in relevant_flows:
            source_type = type(self.nx_graph.nodes[source]["data"]).__name__
            target_type = type(self.nx_graph.nodes[target]["data"]).__name__
            
            flow_key = f"{source_type} -> {target_type}"
            node_flow_counts[flow_key] = node_flow_counts.get(flow_key, 0) + 1

        flow_analysis["flow_distribution"] = node_flow_counts

        # Identify major flow pathways (high-volume routes)
        pathway_volumes = {}
        for source, target, data in relevant_flows:
            pathway_key = f"{source} -> {target}"
            volume = data.get("weight", 1.0)
            pathway_volumes[pathway_key] = pathway_volumes.get(pathway_key, 0) + volume

        # Sort and get top pathways
        sorted_pathways = sorted(pathway_volumes.items(), key=lambda x: x[1], reverse=True)
        flow_analysis["major_pathways"] = sorted_pathways[:10]  # Top 10 pathways

        return flow_analysis

    def identify_flow_inefficiencies(self) -> Dict[str, Any]:
        """Identify inefficiencies in flow patterns."""
        import networkx as nx
        
        inefficiencies = {
            "redundant_paths": [],
            "flow_imbalances": [],
            "underutilized_connections": [],
            "optimization_opportunities": []
        }

        # Find redundant paths (multiple paths with similar flows)
        node_pairs_with_multiple_paths = []
        for source in self.nx_graph.nodes():
            for target in self.nx_graph.nodes():
                if source != target:
                    try:
                        paths = list(nx.all_simple_paths(
                            self.nx_graph, source, target, cutoff=3
                        ))
                        if len(paths) > 1:
                            node_pairs_with_multiple_paths.append((source, target, len(paths)))
                    except nx.NetworkXNoPath:
                        continue

        inefficiencies["redundant_paths"] = [
            {"source": str(s), "target": str(t), "path_count": count}
            for s, t, count in node_pairs_with_multiple_paths[:10]  # Top 10
        ]

        # Identify flow imbalances (nodes with very high in-degree vs out-degree)
        for node in self.nx_graph.nodes():
            in_degree = len(list(self.nx_graph.predecessors(node)))
            out_degree = len(list(self.nx_graph.successors(node)))
            
            if in_degree > 0 and out_degree > 0:
                imbalance_ratio = abs(in_degree - out_degree) / max(in_degree, out_degree)
                if imbalance_ratio > 0.7:  # High imbalance threshold
                    inefficiencies["flow_imbalances"].append({
                        "node": str(node),
                        "in_degree": in_degree,
                        "out_degree": out_degree,
                        "imbalance_ratio": imbalance_ratio
                    })

        return inefficiencies

    def _build_networkx_from_graph(self, sfm_graph: SFMGraph):
        """Helper method to build NetworkX graph from SFMGraph."""
        import networkx as nx
        
        G = nx.MultiDiGraph()
        
        # Add nodes
        for node in sfm_graph:
            G.add_node(node.id, data=node, type=type(node).__name__)
        
        # Add relationships as edges
        for rel in sfm_graph.relationships.values():
            G.add_edge(
                rel.source_id,
                rel.target_id,
                key=rel.id,
                data=rel,
                kind=rel.kind,
                weight=rel.weight or 1.0,
            )
        
        return G


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
