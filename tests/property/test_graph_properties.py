"""
Property-based tests for graph operations.

This module tests graph invariants and properties using Hypothesis
to generate test data and verify system behavior.
"""
import pytest
from hypothesis import given, strategies as st, assume, settings
from tests.property.property_base import PropertyTestCase, small_graphs, medium_graphs, properties_dict


class TestGraphProperties(PropertyTestCase):
    """Test graph properties and invariants"""

    @given(small_graphs)
    @settings(max_examples=50)
    def test_graph_invariants(self, graph_data):
        """Test that graph operations maintain invariants"""
        nodes, relationships = graph_data
        assume(len(nodes) > 0)  # Ensure we have at least one node
        
        graph = self.create_graph_from_data(nodes, relationships)

        # Graph invariants
        assert graph.node_count() == len(set(nodes))
        assert graph.relationship_count() <= len(relationships)

        # Test operations maintain invariants
        for node_id in list(graph.nodes.keys())[:5]:  # Test first 5 nodes
            neighbors = graph.get_neighbors(node_id)
            # All neighbors should exist in the graph
            for neighbor in neighbors:
                assert neighbor.id in graph.nodes, f"Neighbor {neighbor.id} not found in graph"

    @given(
        nodes=st.lists(st.text(min_size=1, max_size=20), min_size=1, max_size=50),
        node_type=st.sampled_from(['organization', 'person', 'institution'])
    )
    @settings(max_examples=30)
    def test_node_addition_properties(self, nodes, node_type):
        """Test properties of node addition"""
        from core.base_nodes import Node
        
        graph = self.create_graph_from_data([], [])
        initial_count = graph.node_count()
        
        # Add nodes
        added_nodes = []
        for i, node_name in enumerate(nodes):
            node = Node(
                id=f"prop_node_{i}",
                name=node_name,
                node_type=node_type,
                properties={'test_data': True}
            )
            graph.add_node(node)
            added_nodes.append(node)
        
        # Properties after addition
        assert graph.node_count() == initial_count + len(added_nodes)
        
        # All added nodes should be retrievable
        for node in added_nodes:
            retrieved_node = graph.get_node(node.id)
            assert retrieved_node is not None
            assert retrieved_node.name == node.name
            assert retrieved_node.node_type == node.node_type

    @given(
        st.lists(
            st.tuples(
                st.text(min_size=1, max_size=20),  # source name
                st.text(min_size=1, max_size=20),  # target name
                st.sampled_from(['influences', 'depends_on', 'partners_with'])  # relationship type
            ),
            min_size=1,
            max_size=20
        )
    )
    @settings(max_examples=30)
    def test_relationship_addition_properties(self, relationship_data):
        """Test properties of relationship addition"""
        from core.base_nodes import Node
        from core.relationships import Relationship
        
        graph = self.create_graph_from_data([], [])
        
        # Create nodes first
        nodes = {}
        for i, (source_name, target_name, _) in enumerate(relationship_data):
            for name in [source_name, target_name]:
                if name not in nodes:
                    node = Node(
                        id=f"prop_node_{name}_{i}",
                        name=name,
                        node_type="test_type",
                        properties={'test_data': True}
                    )
                    graph.add_node(node)
                    nodes[name] = node
        
        initial_rel_count = graph.relationship_count()
        
        # Add relationships
        added_relationships = []
        for i, (source_name, target_name, rel_type) in enumerate(relationship_data):
            source_node = nodes[source_name]
            target_node = nodes[target_name]
            
            # Skip self-loops
            if source_node.id != target_node.id:
                rel = Relationship(
                    id=f"prop_rel_{i}",
                    source_id=source_node.id,
                    target_id=target_node.id,
                    relationship_type=rel_type,
                    properties={'test_data': True}
                )
                graph.add_relationship(rel)
                added_relationships.append(rel)
        
        # Properties after addition
        assert graph.relationship_count() == initial_rel_count + len(added_relationships)
        
        # All added relationships should be retrievable
        for rel in added_relationships:
            retrieved_rel = graph.get_relationship(rel.id)
            assert retrieved_rel is not None
            assert retrieved_rel.source_id == rel.source_id
            assert retrieved_rel.target_id == rel.target_id

    @given(medium_graphs)
    @settings(max_examples=20, deadline=2000)
    def test_graph_traversal_properties(self, graph_data):
        """Test properties of graph traversal operations"""
        nodes, relationships = graph_data
        assume(len(nodes) > 5)  # Ensure we have enough nodes for meaningful traversal
        
        graph = self.create_graph_from_data(nodes, relationships)
        
        # Test neighbor queries
        for node_id in list(graph.nodes.keys())[:5]:
            neighbors = graph.get_neighbors(node_id)
            
            # Properties of neighbors
            for neighbor in neighbors:
                # Neighbor should be reachable from original node
                assert neighbor.id in graph.nodes
                
                # There should be a relationship connecting them
                relationships_to_neighbor = graph.get_relationships(node_id, neighbor.id)
                relationships_from_neighbor = graph.get_relationships(neighbor.id, node_id)
                
                assert len(relationships_to_neighbor) > 0 or len(relationships_from_neighbor) > 0

    @given(
        node_count=st.integers(min_value=3, max_value=20),
        operations=st.lists(
            st.one_of(
                st.tuples(st.just('add_node'), st.text(min_size=1, max_size=20)),
                st.tuples(st.just('remove_node'), st.integers(min_value=0, max_value=19)),
                st.tuples(st.just('add_relationship'), st.integers(min_value=0, max_value=19), st.integers(min_value=0, max_value=19))
            ),
            min_size=1,
            max_size=10
        )
    )
    @settings(max_examples=20)
    def test_graph_modification_properties(self, node_count, operations):
        """Test properties of graph modifications"""
        from core.base_nodes import Node
        from core.relationships import Relationship
        
        # Create initial graph
        initial_nodes = [f"node_{i}" for i in range(node_count)]
        graph = self.create_graph_from_data(initial_nodes, [])
        
        # Apply operations
        for operation in operations:
            op_type = operation[0]
            
            if op_type == 'add_node':
                node_name = operation[1]
                node = Node(
                    id=f"new_node_{node_name}",
                    name=node_name,
                    node_type="test_type",
                    properties={'test_data': True}
                )
                graph.add_node(node)
            
            elif op_type == 'remove_node':
                node_index = operation[1]
                node_ids = list(graph.nodes.keys())
                if node_index < len(node_ids):
                    node_id = node_ids[node_index]
                    graph.remove_node(node_id)
            
            elif op_type == 'add_relationship':
                source_idx, target_idx = operation[1], operation[2]
                node_ids = list(graph.nodes.keys())
                if (source_idx < len(node_ids) and target_idx < len(node_ids) and 
                    source_idx != target_idx):
                    source_id = node_ids[source_idx]
                    target_id = node_ids[target_idx]
                    rel = Relationship(
                        id=f"new_rel_{source_idx}_{target_idx}",
                        source_id=source_id,
                        target_id=target_id,
                        relationship_type="test_relationship",
                        properties={'test_data': True}
                    )
                    graph.add_relationship(rel)
            
            # Assert invariants after each operation
            self.assert_graph_invariants(graph)

    @given(
        nodes=st.lists(st.text(min_size=1, max_size=20), min_size=2, max_size=10),
        properties_list=st.lists(properties_dict, min_size=2, max_size=10)
    )
    @settings(max_examples=20)
    def test_node_property_invariants(self, nodes, properties_list):
        """Test that node properties are maintained correctly"""
        from core.base_nodes import Node
        
        # Ensure we have enough properties for each node
        assume(len(properties_list) >= len(nodes))
        
        graph = self.create_graph_from_data([], [])
        
        # Add nodes with properties
        for i, node_name in enumerate(nodes):
            node_props = properties_list[i % len(properties_list)]
            node = Node(
                id=f"prop_node_{i}",
                name=node_name,
                node_type="test_type",
                properties=node_props
            )
            graph.add_node(node)
        
        # Verify properties are maintained
        for node in graph.nodes.values():
            retrieved_node = graph.get_node(node.id)
            assert retrieved_node is not None
            assert retrieved_node.properties == node.properties
            
            # Properties should be serializable
            import json
            try:
                json.dumps(retrieved_node.properties)
            except (TypeError, ValueError):
                pytest.fail(f"Node properties are not JSON serializable: {retrieved_node.properties}")

    @given(small_graphs)
    @settings(max_examples=30)
    def test_graph_consistency_after_operations(self, graph_data):
        """Test that graph remains consistent after various operations"""
        nodes, relationships = graph_data
        assume(len(nodes) > 0)
        
        graph = self.create_graph_from_data(nodes, relationships)
        
        # Record initial state
        initial_node_count = graph.node_count()
        initial_rel_count = graph.relationship_count()
        
        # Perform read operations (should not change state)
        for node_id in list(graph.nodes.keys())[:3]:
            _ = graph.get_node(node_id)
            _ = graph.get_neighbors(node_id)
        
        # State should be unchanged
        assert graph.node_count() == initial_node_count
        assert graph.relationship_count() == initial_rel_count
        
        # Graph should still be valid
        self.assert_graph_invariants(graph)