"""
Load testing scenarios for SFM system.

This module contains specific load tests for different system components
and operations under various load conditions.
"""
import pytest
from tests.performance.performance_base import LoadTestCase
from tests.factories.node_factory import NodeFactory, RelationshipFactory


class TestQueryPerformance(LoadTestCase):
    """Test query performance under load"""

    @pytest.mark.performance
    def test_node_query_performance(self):
        """Test node query performance under load"""
        # Setup large dataset
        self.create_large_test_dataset(nodes=10000, relationships=50000)

        # Define test scenarios
        scenarios = {
            'single_node_lookup': self.single_node_lookup,
            'neighbor_query': self.neighbor_query,
            'path_finding_query': self.path_finding_query,
            'aggregation_query': self.aggregation_query
        }

        results = {}
        for scenario_name, scenario_func in scenarios.items():
            print(f"\nRunning {scenario_name} load test...")
            results[scenario_name] = self.run_load_scenario('medium_load', scenario_func)

        # Assert performance requirements
        self.assert_performance_threshold(
            results['single_node_lookup']['avg_response_time'], 
            0.1, 
            "Single node lookup"
        )
        self.assert_performance_threshold(
            results['neighbor_query']['avg_response_time'], 
            0.5, 
            "Neighbor query"
        )
        self.assert_performance_threshold(
            results['path_finding_query']['avg_response_time'], 
            2.0, 
            "Path finding query"
        )

        # Assert throughput requirements
        self.assert_throughput_threshold(
            results['single_node_lookup']['throughput'], 
            100, 
            "Single node lookup"
        )

    def single_node_lookup(self):
        """Single node lookup operation"""
        import random
        node_ids = list(self.test_graph.nodes.keys())
        if node_ids:
            node_id = random.choice(node_ids)
            return self.test_graph.get_node(node_id)
        return None

    def neighbor_query(self):
        """Neighbor query operation"""
        import random
        node_ids = list(self.test_graph.nodes.keys())
        if node_ids:
            node_id = random.choice(node_ids)
            return self.test_graph.get_neighbors(node_id)
        return []

    def path_finding_query(self):
        """Path finding query operation"""
        import random
        node_ids = list(self.test_graph.nodes.keys())
        if len(node_ids) >= 2:
            source_id = random.choice(node_ids)
            target_id = random.choice(node_ids)
            return self.test_graph.find_path(source_id, target_id)
        return None

    def aggregation_query(self):
        """Aggregation query operation"""
        # Count nodes by type
        node_counts = {}
        for node in self.test_graph.nodes.values():
            node_type = node.node_type
            node_counts[node_type] = node_counts.get(node_type, 0) + 1
        return node_counts

    @pytest.mark.performance
    def test_write_performance(self):
        """Test write operation performance under load"""
        def create_node_operation():
            """Create node operation"""
            node = NodeFactory.create()
            self.test_graph.add_node(node)
            return node

        def create_relationship_operation():
            """Create relationship operation"""
            node_ids = list(self.test_graph.nodes.keys())
            if len(node_ids) >= 2:
                import random
                source_id = random.choice(node_ids)
                target_id = random.choice(node_ids)
                rel = RelationshipFactory.create(source_id=source_id, target_id=target_id)
                self.test_graph.add_relationship(rel)
                return rel
            return None

        # Test node creation performance
        node_results = self.run_load_scenario('light_load', create_node_operation)
        self.assert_performance_threshold(
            node_results['avg_response_time'], 
            0.05, 
            "Node creation"
        )

        # Test relationship creation performance
        rel_results = self.run_load_scenario('light_load', create_relationship_operation)
        self.assert_performance_threshold(
            rel_results['avg_response_time'], 
            0.1, 
            "Relationship creation"
        )

    @pytest.mark.performance
    def test_mixed_workload_performance(self):
        """Test mixed read/write workload performance"""
        self.create_large_test_dataset(nodes=5000, relationships=10000)

        operations = [
            self.single_node_lookup,
            self.neighbor_query,
            lambda: NodeFactory.create(),
            lambda: RelationshipFactory.create()
        ]

        # Simulate realistic user sessions
        session_results = []
        for _ in range(10):
            session_result = self.simulate_user_session(operations, session_duration=30)
            session_results.extend(session_result)

        # Calculate overall performance
        successful_operations = [r for r in session_results if r['success']]
        avg_response_time = sum(r['execution_time'] for r in successful_operations) / len(successful_operations)

        self.assert_performance_threshold(
            avg_response_time, 
            0.5, 
            "Mixed workload"
        )

        # Check error rate
        error_rate = (len(session_results) - len(successful_operations)) / len(session_results)
        assert error_rate < 0.05, f"Error rate {error_rate:.2%} exceeds 5% threshold"


class TestScalabilityPerformance(LoadTestCase):
    """Test system scalability under increasing load"""

    @pytest.mark.performance
    def test_horizontal_scaling(self):
        """Test performance with increasing number of concurrent users"""
        operation = self.single_node_lookup
        self.create_large_test_dataset(nodes=1000, relationships=2000)

        # Test with increasing load
        user_counts = [10, 25, 50, 100]
        results = {}

        for user_count in user_counts:
            print(f"\nTesting with {user_count} concurrent users...")
            result = self.run_load_test(
                operation, 
                concurrent_users=user_count, 
                duration=30
            )
            results[user_count] = result

        # Check that performance degrades gracefully
        prev_avg_time = 0
        for user_count in user_counts:
            avg_time = results[user_count]['avg_response_time']
            
            # Response time should not increase by more than 3x
            if prev_avg_time > 0:
                degradation_ratio = avg_time / prev_avg_time
                assert degradation_ratio < 3.0, \
                    f"Performance degraded by {degradation_ratio:.1f}x from {prev_avg_time:.3f}s to {avg_time:.3f}s"
            
            prev_avg_time = avg_time

    @pytest.mark.performance
    def test_vertical_scaling(self):
        """Test performance with increasing data size"""
        operation = self.single_node_lookup
        
        # Test with increasing data sizes
        data_sizes = [
            (100, 200),    # Small
            (1000, 2000),  # Medium
            (5000, 10000), # Large
            (10000, 20000) # Very Large
        ]
        
        results = {}
        
        for nodes, relationships in data_sizes:
            print(f"\nTesting with {nodes} nodes and {relationships} relationships...")
            
            # Create fresh test data
            self.cleanup_test_data()
            self.setup_test_data()
            self.create_large_test_dataset(nodes=nodes, relationships=relationships)
            
            result = self.run_load_test(
                operation, 
                concurrent_users=25, 
                duration=30
            )
            results[(nodes, relationships)] = result

        # Check that performance scales reasonably
        base_time = results[(100, 200)]['avg_response_time']
        
        for (nodes, relationships), result in results.items():
            avg_time = result['avg_response_time']
            data_size_ratio = nodes / 100
            
            # Response time should not increase faster than O(log n)
            expected_max_time = base_time * (1 + 0.5 * data_size_ratio)
            assert avg_time < expected_max_time, \
                f"Performance with {nodes} nodes: {avg_time:.3f}s exceeds expected {expected_max_time:.3f}s"

    @pytest.mark.performance
    def test_memory_scaling(self):
        """Test memory usage with increasing data size"""
        import psutil
        
        data_sizes = [1000, 5000, 10000, 25000]
        memory_usage = {}
        
        for size in data_sizes:
            print(f"\nTesting memory usage with {size} nodes...")
            
            # Clean up previous data
            self.cleanup_test_data()
            self.setup_test_data()
            
            # Measure memory before creating data
            initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Create test data
            self.create_large_test_dataset(nodes=size, relationships=size * 2)
            
            # Measure memory after creating data
            final_memory = psutil.Process().memory_info().rss / 1024 / 1024
            memory_increase = final_memory - initial_memory
            
            memory_usage[size] = {
                'initial_memory_mb': initial_memory,
                'final_memory_mb': final_memory,
                'memory_increase_mb': memory_increase,
                'memory_per_node_kb': (memory_increase * 1024) / size
            }

        # Check that memory usage scales linearly
        base_memory_per_node = memory_usage[1000]['memory_per_node_kb']
        
        for size, usage in memory_usage.items():
            if size > 1000:
                memory_per_node = usage['memory_per_node_kb']
                
                # Memory per node should not increase by more than 50%
                ratio = memory_per_node / base_memory_per_node
                assert ratio < 1.5, \
                    f"Memory per node increased by {ratio:.1f}x for {size} nodes"