"""
Example test demonstrating the comprehensive testing framework.

This module shows how to use the various testing framework components
to write effective tests for the SFM system.
"""
import pytest
from tests.framework.base_test import BaseTestCase, GraphTestCase, ServiceTestCase
from tests.integration.integration_base import IntegrationTestCase
from tests.performance.performance_base import PerformanceTestCase
from tests.property.property_base import PropertyTestCase, small_graphs
from tests.factories.node_factory import NodeFactory, OrganizationNodeFactory, PersonNodeFactory
from tests.factories.relationship_factory import RelationshipFactory
from hypothesis import given


class TestFrameworkExample(BaseTestCase):
    """Example showing BaseTestCase usage"""
    
    def test_basic_node_creation(self):
        """Test basic node creation using the framework"""
        node = self.create_test_node()
        assert node.id is not None
        assert node.label.startswith('Test Actor')
        self.assert_node_exists(node.id)
    
    def test_node_with_relationship(self):
        """Test creating nodes with relationships"""
        node1 = self.create_test_node()
        node2 = self.create_test_node()
        
        relationship = self.create_test_relationship(node1, node2)
        assert relationship.source_id == node1.id
        assert relationship.target_id == node2.id


class TestFrameworkGraphExample(GraphTestCase):
    """Example showing GraphTestCase usage"""
    
    def test_graph_structure(self):
        """Test graph structure and invariants"""
        # The setup_test_data method creates a graph with test nodes and relationships
        assert len(self.test_graph.get_all_node_ids()) == 10
        self.assert_graph_invariants()
    
    def test_subgraph_creation(self):
        """Test subgraph creation"""
        subgraph = self.get_test_subgraph(node_count=3)
        assert len(subgraph.get_all_node_ids()) == 3


class TestFrameworkFactoryExample(BaseTestCase):
    """Example showing factory usage"""
    
    def test_node_factories(self):
        """Test different node factory types"""
        # Test generic node factory
        node = NodeFactory.create()
        assert node.id is not None
        
        # Test specialized factories
        org = OrganizationNodeFactory.create()
        assert org.meta.get('node_type') == 'organization'
        
        person = PersonNodeFactory.create()
        assert person.meta.get('node_type') == 'person'
    
    def test_relationship_factory(self):
        """Test relationship factory"""
        rel = RelationshipFactory.create()
        assert rel.source_id is not None
        assert rel.target_id is not None
        assert rel.kind is not None


class TestFrameworkPropertyExample(PropertyTestCase):
    """Example showing property-based testing"""
    
    @given(small_graphs)
    def test_graph_properties(self, graph_data):
        """Test graph properties with generated data"""
        nodes, relationships = graph_data
        if len(nodes) == 0:
            return  # Skip empty graphs
        
        graph = self.create_graph_from_data(nodes, relationships)
        
        # Test basic invariants
        assert len(graph.get_all_node_ids()) == len(set(nodes))
        self.assert_graph_invariants(graph)


class TestFrameworkPerformanceExample(PerformanceTestCase):
    """Example showing performance testing"""
    
    @pytest.mark.performance
    def test_node_creation_performance(self):
        """Test node creation performance"""
        def create_node():
            return NodeFactory.create()
        
        # Measure execution time
        result = self.measure_execution_time(create_node)
        
        # Assert reasonable performance
        self.assert_performance_threshold(result['execution_time'], 0.1, "Node creation")
    
    @pytest.mark.performance
    def test_batch_operations_performance(self):
        """Test batch operations performance"""
        def create_batch():
            return [NodeFactory.create() for _ in range(100)]
        
        # Run load test
        results = self.run_load_test(create_batch, concurrent_users=5, duration=10)
        
        # Assert throughput
        self.assert_throughput_threshold(results['throughput'], 1.0, "Batch operations")


if __name__ == '__main__':
    # Run the examples
    print("Running framework examples...")
    
    # Test basic framework
    test = TestFrameworkExample()
    test.setup_test_data()
    test.test_basic_node_creation()
    print("✓ Basic test passed")
    
    # Test graph framework
    graph_test = TestFrameworkGraphExample()
    graph_test.setup_test_data()
    graph_test.test_graph_structure()
    print("✓ Graph test passed")
    
    # Test factories
    factory_test = TestFrameworkFactoryExample()
    factory_test.setup_test_data()
    factory_test.test_node_factories()
    print("✓ Factory test passed")
    
    print("All framework examples passed!")