"""
Base classes for performance testing.

This module provides the foundation for performance tests that measure
system performance, scalability, and resource usage.
"""
import pytest
import time
import psutil
import threading
from typing import Dict, List, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import MagicMock

from tests.framework.base_test import BaseTestCase
from tests.factories.node_factory import GraphFactory


class PerformanceTestCase(BaseTestCase):
    """Base class for performance tests"""

    def setup_test_data(self):
        """Set up performance test data"""
        # Create larger test datasets
        self.small_graph = GraphFactory.create_small_graph(nodes=100, relationships=200)
        self.medium_graph = GraphFactory.create_large_graph(nodes=1000, relationships=2000)
        self.large_graph = GraphFactory.create_large_graph(nodes=10000, relationships=20000)

    @pytest.fixture(autouse=True)
    def setup_performance_monitoring(self):
        """Set up performance monitoring"""
        # Record initial system state
        self.initial_memory = psutil.Process().memory_info().rss
        self.initial_cpu = psutil.cpu_percent(interval=None)
        
        # Performance metrics storage
        self.performance_metrics = {
            'execution_times': [],
            'memory_usage': [],
            'cpu_usage': [],
            'throughput': []
        }
        
        yield
        
        # Report final metrics
        self.report_performance_metrics()

    def report_performance_metrics(self):
        """Report performance metrics at the end of test"""
        final_memory = psutil.Process().memory_info().rss
        memory_increase = final_memory - self.initial_memory
        
        print(f"\n=== Performance Metrics ===")
        print(f"Memory increase: {memory_increase / 1024 / 1024:.2f} MB")
        print(f"Execution times: {self.performance_metrics['execution_times']}")
        print(f"Average execution time: {self.get_average_execution_time():.3f}s")
        print(f"Peak memory usage: {max(self.performance_metrics['memory_usage'], default=0) / 1024 / 1024:.2f} MB")

    def measure_execution_time(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Measure execution time of a function"""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = e
            success = False
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        execution_time = end_time - start_time
        memory_used = end_memory - start_memory
        
        # Store metrics
        self.performance_metrics['execution_times'].append(execution_time)
        self.performance_metrics['memory_usage'].append(memory_used)
        
        return {
            'result': result,
            'success': success,
            'execution_time': execution_time,
            'memory_used': memory_used,
            'start_time': start_time,
            'end_time': end_time
        }

    def run_load_test(self, operation: Callable, concurrent_users: int = 10, 
                      duration: int = 30, *args, **kwargs) -> Dict[str, Any]:
        """Run a load test with multiple concurrent users"""
        start_time = time.time()
        end_time = start_time + duration
        
        results = []
        errors = []
        
        def worker():
            """Worker function for concurrent execution"""
            local_results = []
            local_errors = []
            
            while time.time() < end_time:
                try:
                    result = self.measure_execution_time(operation, *args, **kwargs)
                    local_results.append(result)
                    if not result['success']:
                        local_errors.append(result['result'])
                except Exception as e:
                    local_errors.append(e)
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.001)
            
            return local_results, local_errors
        
        # Run concurrent workers
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(worker) for _ in range(concurrent_users)]
            
            for future in as_completed(futures):
                worker_results, worker_errors = future.result()
                results.extend(worker_results)
                errors.extend(worker_errors)
        
        # Calculate metrics
        successful_operations = [r for r in results if r['success']]
        total_operations = len(results)
        total_time = time.time() - start_time
        
        return {
            'total_operations': total_operations,
            'successful_operations': len(successful_operations),
            'error_count': len(errors),
            'total_time': total_time,
            'throughput': total_operations / total_time if total_time > 0 else 0,
            'avg_response_time': sum(r['execution_time'] for r in successful_operations) / len(successful_operations) if successful_operations else 0,
            'min_response_time': min(r['execution_time'] for r in successful_operations) if successful_operations else 0,
            'max_response_time': max(r['execution_time'] for r in successful_operations) if successful_operations else 0,
            'errors': errors[:10]  # Store first 10 errors
        }

    def get_average_execution_time(self) -> float:
        """Get average execution time from recorded metrics"""
        times = self.performance_metrics['execution_times']
        return sum(times) / len(times) if times else 0

    def assert_performance_threshold(self, execution_time: float, threshold: float, 
                                   operation_name: str = "Operation"):
        """Assert that execution time is below threshold"""
        assert execution_time < threshold, \
            f"{operation_name} took {execution_time:.3f}s, expected < {threshold}s"

    def assert_throughput_threshold(self, throughput: float, threshold: float, 
                                  operation_name: str = "Operation"):
        """Assert that throughput is above threshold"""
        assert throughput > threshold, \
            f"{operation_name} throughput {throughput:.2f} ops/sec, expected > {threshold} ops/sec"

    def create_large_test_dataset(self, nodes: int = 10000, relationships: int = 50000):
        """Create large dataset for performance testing"""
        self.large_test_graph = GraphFactory.create_large_graph(nodes, relationships)
        
        # Add to test graph
        for node in self.large_test_graph.nodes.values():
            self.test_graph.add_node(node)
        
        for rel in self.large_test_graph.relationships.values():
            self.test_graph.add_relationship(rel)


class LoadTestCase(PerformanceTestCase):
    """Specialized test case for load testing"""

    def setup_test_data(self):
        """Set up load test data"""
        super().setup_test_data()
        
        # Create test scenarios
        self.load_scenarios = {
            'light_load': {'users': 10, 'duration': 30},
            'medium_load': {'users': 50, 'duration': 60},
            'heavy_load': {'users': 100, 'duration': 120}
        }

    def run_load_scenario(self, scenario_name: str, operation: Callable, 
                         *args, **kwargs) -> Dict[str, Any]:
        """Run a predefined load scenario"""
        scenario = self.load_scenarios[scenario_name]
        return self.run_load_test(
            operation, 
            concurrent_users=scenario['users'],
            duration=scenario['duration'],
            *args, **kwargs
        )

    def simulate_user_session(self, operations: List[Callable], 
                             session_duration: int = 60) -> List[Dict[str, Any]]:
        """Simulate a user session with multiple operations"""
        start_time = time.time()
        end_time = start_time + session_duration
        
        results = []
        
        while time.time() < end_time:
            # Randomly select an operation
            import random
            operation = random.choice(operations)
            
            result = self.measure_execution_time(operation)
            results.append(result)
            
            # Random delay between operations (0.1 to 2 seconds)
            time.sleep(random.uniform(0.1, 2.0))
        
        return results


class StressTestCase(PerformanceTestCase):
    """Specialized test case for stress testing"""

    def setup_test_data(self):
        """Set up stress test data"""
        super().setup_test_data()
        
        # Create extreme test scenarios
        self.stress_scenarios = {
            'memory_stress': {'nodes': 50000, 'relationships': 100000},
            'cpu_stress': {'concurrent_operations': 200, 'duration': 300},
            'connection_stress': {'concurrent_connections': 1000}
        }

    def run_memory_stress_test(self, max_memory_mb: int = 500) -> Dict[str, Any]:
        """Run memory stress test"""
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Gradually increase memory usage
        test_data = []
        current_memory = initial_memory
        
        while current_memory - initial_memory < max_memory_mb:
            # Create more test data
            graph = GraphFactory.create_large_graph(nodes=1000, relationships=2000)
            test_data.append(graph)
            
            current_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Check if system is still responsive
            start_time = time.time()
            _ = len(test_data)  # Simple operation
            response_time = time.time() - start_time
            
            if response_time > 1.0:  # System becoming unresponsive
                break
        
        peak_memory = current_memory
        memory_increase = peak_memory - initial_memory
        
        return {
            'initial_memory_mb': initial_memory,
            'peak_memory_mb': peak_memory,
            'memory_increase_mb': memory_increase,
            'objects_created': len(test_data),
            'system_responsive': response_time < 1.0
        }

    def run_cpu_stress_test(self, duration: int = 60) -> Dict[str, Any]:
        """Run CPU stress test"""
        import multiprocessing
        
        def cpu_intensive_task():
            """CPU-intensive task"""
            end_time = time.time() + duration
            operations = 0
            
            while time.time() < end_time:
                # Perform CPU-intensive calculation
                _ = sum(i * i for i in range(1000))
                operations += 1
            
            return operations
        
        # Monitor CPU usage
        cpu_usage = []
        
        def monitor_cpu():
            """Monitor CPU usage during test"""
            while time.time() < end_time:
                cpu_usage.append(psutil.cpu_percent(interval=0.1))
        
        # Start monitoring
        end_time = time.time() + duration
        monitor_thread = threading.Thread(target=monitor_cpu)
        monitor_thread.start()
        
        # Run CPU-intensive tasks
        num_processes = multiprocessing.cpu_count()
        with ThreadPoolExecutor(max_workers=num_processes) as executor:
            futures = [executor.submit(cpu_intensive_task) for _ in range(num_processes)]
            total_operations = sum(future.result() for future in as_completed(futures))
        
        monitor_thread.join()
        
        return {
            'total_operations': total_operations,
            'operations_per_second': total_operations / duration,
            'avg_cpu_usage': sum(cpu_usage) / len(cpu_usage) if cpu_usage else 0,
            'max_cpu_usage': max(cpu_usage) if cpu_usage else 0,
            'min_cpu_usage': min(cpu_usage) if cpu_usage else 0
        }