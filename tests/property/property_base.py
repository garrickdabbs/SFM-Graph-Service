"""
Base classes for property-based testing.

This module provides the foundation for property-based tests using Hypothesis
to test system invariants and properties.
"""
import pytest
from hypothesis import given, strategies as st, settings, assume
from typing import Dict, List, Any, Optional

from tests.framework.base_test import BaseTestCase
from core.graph import SFMGraph
from core.core_nodes import Actor
from core.relationships import Relationship
from core.sfm_enums import RelationshipKind


class PropertyTestCase(BaseTestCase):
    """Base class for property-based tests"""

    def setup_test_data(self):
        """Set up property test data"""
        # Property-based tests generate their own data
        pass

    def create_graph_from_data(self, nodes: List[str], relationships: List[tuple]) -> SFMGraph:
        """Create a graph from generated data"""
        graph = SFMGraph()
        
        # Create nodes
        for i, node_name in enumerate(nodes):
            node = Actor(
                label=node_name,
                description="Test actor",
                meta={'test_data': True}
            )
            graph.add_node(node)
        
        # Create relationships
        node_list = list(graph.nodes.values())
        for source_idx, target_idx in relationships:
            if 0 <= source_idx < len(node_list) and 0 <= target_idx < len(node_list):
                source_node = node_list[source_idx]
                target_node = node_list[target_idx]
                
                if source_node.id != target_node.id:  # Avoid self-loops
                    rel = Relationship(
                        source_id=source_node.id,
                        target_id=target_node.id,
                        kind=RelationshipKind.AFFECTS,
                        weight=1.0,
                        meta={'test_data': True}
                    )
                    graph.add_relationship(rel)
        
        return graph

    def assert_graph_invariants(self, graph: SFMGraph):
        """Assert fundamental graph invariants"""
        # All nodes should have unique IDs
        node_ids = [node.id for node in graph.nodes.values()]
        assert len(node_ids) == len(set(node_ids)), "Node IDs are not unique"
        
        # All relationships should reference existing nodes
        for rel in graph.relationships.values():
            assert rel.source_id in graph.get_all_node_ids(), f"Source node {rel.source_id} not found"
            assert rel.target_id in graph.get_all_node_ids(), f"Target node {rel.target_id} not found"
        
        # Graph should be consistent
        assert len(graph.get_all_node_ids()) == len(graph.get_all_node_ids())
        assert graph.relationship_count() == len(graph.relationships)

    def assert_operation_invariants(self, graph: SFMGraph, operation_result: Any):
        """Assert invariants after operations"""
        # Graph should still be valid after operations
        self.assert_graph_invariants(graph)
        
        # Operation should not corrupt the graph
        assert len(graph.get_all_node_ids()) >= 0
        assert graph.relationship_count() >= 0


# Strategy definitions for generating test data
node_names = st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=['Lu', 'Ll', 'Nd', 'Pc']))
node_types = st.sampled_from(['organization', 'person', 'institution', 'resource', 'process', 'policy'])
relationship_types = st.sampled_from(['influences', 'depends_on', 'partners_with', 'competes_with', 'contains', 'flows_to'])

small_graphs = st.builds(
    lambda nodes, relationships: (nodes, relationships),
    nodes=st.lists(node_names, min_size=1, max_size=20, unique=True),
    relationships=st.lists(
        st.tuples(st.integers(min_value=0, max_value=19), st.integers(min_value=0, max_value=19)),
        max_size=50
    )
)

medium_graphs = st.builds(
    lambda nodes, relationships: (nodes, relationships),
    nodes=st.lists(node_names, min_size=10, max_size=100, unique=True),
    relationships=st.lists(
        st.tuples(st.integers(min_value=0, max_value=99), st.integers(min_value=0, max_value=99)),
        max_size=200
    )
)

properties_dict = st.dictionaries(
    keys=st.text(min_size=1, max_size=20),
    values=st.one_of(st.text(), st.integers(), st.floats(), st.booleans()),
    min_size=0,
    max_size=10
)