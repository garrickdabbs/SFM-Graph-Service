"""
Base test case classes for the SFM testing framework.

This module provides the foundational test classes that all SFM tests should inherit from.
It includes setup/teardown mechanisms, test data management, and common test utilities.
"""
import pytest
import uuid
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

from core.graph import SFMGraph
from core.sfm_service import SFMService
from core.sfm_models import Node, Relationship
from core.sfm_enums import RelationshipKind
from core.core_nodes import Actor
from tests.factories.node_factory import NodeFactory
from tests.factories.relationship_factory import RelationshipFactory


class BaseTestCase:
    """Base class for all SFM test cases"""

    @pytest.fixture(autouse=True)
    def setup_test_environment(self):
        """Set up clean test environment for each test"""
        self.test_graph = SFMGraph()
        self.test_service = SFMService()
        self.mock_db = MagicMock()

        # Setup test data
        self.setup_test_data()
        yield
        # Cleanup after test
        self.cleanup_test_data()

    def setup_test_data(self):
        """Override in subclasses to set up specific test data"""
        if not hasattr(self, 'test_graph'):
            self.test_graph = SFMGraph()
        if not hasattr(self, 'test_service'):
            self.test_service = SFMService()
        if not hasattr(self, 'mock_db'):
            self.mock_db = MagicMock()

    def cleanup_test_data(self):
        """Clean up test data after each test"""
        if hasattr(self, 'test_graph'):
            self.test_graph.clear()

    def assert_node_exists(self, node_id: uuid.UUID, expected_properties: Optional[Dict] = None):
        """Assert that a node exists in the test graph"""
        assert self.test_graph.get_node_by_id(node_id) is not None, f"Node {node_id} does not exist"
        if expected_properties:
            node = self.test_graph.get_node_by_id(node_id)
            for key, value in expected_properties.items():
                assert getattr(node, key) == value, f"Property {key} mismatch"

    def assert_relationship_exists(self, source_id: str, target_id: str, relationship_type: str):
        """Assert that a relationship exists between two nodes"""
        relationships = self.test_graph.get_relationships(source_id, target_id)
        assert any(rel.relationship_type == relationship_type for rel in relationships), \
            f"Relationship {relationship_type} does not exist between {source_id} and {target_id}"

    def create_test_node(self, **kwargs) -> Node:
        """Create a test node with default or custom properties"""
        node_count = len(self.test_graph.get_all_node_ids())
        defaults = {
            'label': f'Test Actor {node_count}',
            'description': 'Test actor for testing',
            'meta': {'test_data': True}
        }
        defaults.update(kwargs)
        node = Actor(**defaults)
        self.test_graph.add_node(node)
        return node

    def create_test_relationship(self, source_node: Node, target_node: Node, **kwargs) -> Relationship:
        """Create a test relationship between two nodes"""
        defaults = {
            'source_id': source_node.id,
            'target_id': target_node.id,
            'kind': RelationshipKind.AFFECTS,
            'weight': 1.0,
            'meta': {'test_data': True}
        }
        defaults.update(kwargs)
        relationship = Relationship(**defaults)
        self.test_graph.add_relationship(relationship)
        return relationship


class GraphTestCase(BaseTestCase):
    """Specialized test case for graph operations"""

    def setup_test_data(self):
        """Set up test graph with nodes and relationships"""
        # First call parent setup
        super().setup_test_data()
        
        # Create test nodes using factories
        self.test_nodes = []
        for i in range(10):
            node = NodeFactory.create()
            self.test_nodes.append(node)
            self.test_graph.add_node(node)

        # Create test relationships
        self.test_relationships = []
        for i in range(0, 9):
            rel = RelationshipFactory.create(
                source_id=self.test_nodes[i].id,
                target_id=self.test_nodes[i + 1].id
            )
            self.test_relationships.append(rel)
            self.test_graph.add_relationship(rel)

    def assert_graph_invariants(self):
        """Assert that the graph maintains its invariants"""
        # All nodes should have valid IDs
        for node_id in self.test_graph.get_all_node_ids():
            node = self.test_graph.get_node_by_id(node_id)
            assert node.id is not None
            assert node.id == node_id

        # All relationships should reference existing nodes
        for rel in self.test_graph.relationships.values():
            assert rel.source_id in self.test_graph.get_all_node_ids(), f"Source node {rel.source_id} not found"
            assert rel.target_id in self.test_graph.get_all_node_ids(), f"Target node {rel.target_id} not found"

    def get_test_subgraph(self, node_count: int = 3) -> SFMGraph:
        """Get a subgraph for testing"""
        subgraph = SFMGraph()
        node_ids = list(self.test_graph.get_all_node_ids())
        for i in range(min(node_count, len(node_ids))):
            node = self.test_graph.get_node_by_id(node_ids[i])
            subgraph.add_node(node)
        return subgraph


class ServiceTestCase(BaseTestCase):
    """Specialized test case for service layer testing"""

    def setup_test_data(self):
        """Set up test service with mocked dependencies"""
        # Mock external dependencies
        self.mock_persistence = MagicMock()
        self.mock_query_engine = MagicMock()
        
        # Patch service dependencies
        self.persistence_patcher = patch.object(self.test_service, 'persistence', self.mock_persistence)
        self.query_patcher = patch.object(self.test_service, 'query_engine', self.mock_query_engine)
        
        self.persistence_patcher.start()
        self.query_patcher.start()

    def cleanup_test_data(self):
        """Clean up mocked dependencies"""
        if hasattr(self, 'persistence_patcher'):
            self.persistence_patcher.stop()
        if hasattr(self, 'query_patcher'):
            self.query_patcher.stop()
        super().cleanup_test_data()

    def assert_service_call(self, method_name: str, call_count: int = 1):
        """Assert that a service method was called"""
        if hasattr(self.mock_persistence, method_name):
            method = getattr(self.mock_persistence, method_name)
            assert method.call_count == call_count, f"Method {method_name} called {method.call_count} times, expected {call_count}"