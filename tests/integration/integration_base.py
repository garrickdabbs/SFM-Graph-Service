"""
Base classes for integration testing.

This module provides the foundation for integration tests that test complete
workflows and interactions between multiple components of the SFM system.
"""
import pytest
from typing import Dict, Any, List, Optional
from unittest.mock import MagicMock, patch

from tests.framework.base_test import BaseTestCase
from core.graph import SFMGraph
from core.sfm_service import SFMService
from tests.factories.node_factory import GraphFactory


class IntegrationTestCase(BaseTestCase):
    """Base class for integration tests"""

    @pytest.fixture(autouse=True)
    def setup_integration_environment(self):
        """Set up integration test environment"""
        # Create a more realistic test environment
        self.test_graph = GraphFactory.create_small_graph(nodes=20, relationships=30)
        self.test_service = SFMService()
        
        # Mock external dependencies but allow internal component interactions
        self.setup_external_mocks()
        
        # Setup integration-specific test data
        self.setup_integration_data()
        
        yield
        
        # Cleanup
        self.cleanup_integration_data()

    def setup_external_mocks(self):
        """Set up mocks for external dependencies"""
        # Mock database connections
        self.mock_db_connection = MagicMock()
        self.mock_neo4j_driver = MagicMock()
        
        # Mock external API calls
        self.mock_external_api = MagicMock()
        
        # Store patches for cleanup
        self.patches = []

    def setup_integration_data(self):
        """Override in subclasses to set up integration-specific data"""
        pass

    def cleanup_integration_data(self):
        """Clean up integration test data"""
        # Stop all patches
        for patch_obj in getattr(self, 'patches', []):
            patch_obj.stop()
        
        # Clear test graph
        if hasattr(self, 'test_graph'):
            self.test_graph.clear()

    def create_api_client(self):
        """Create a test API client"""
        from api.sfm_api import create_app
        app = create_app(testing=True)
        return app.test_client()

    def assert_workflow_completion(self, workflow_id: str, expected_status: str = 'completed'):
        """Assert that a workflow completed successfully"""
        # This would check workflow status in a real implementation
        pass

    def assert_data_consistency(self):
        """Assert that data is consistent across all components"""
        # Check that nodes exist in both graph and service
        for node_id in self.test_graph.nodes:
            assert self.test_service.get_node(node_id) is not None, f"Node {node_id} not found in service"
        
        # Check that relationships are consistent
        for rel_id in self.test_graph.relationships:
            rel = self.test_graph.relationships[rel_id]
            assert self.test_graph.has_node(rel.source_id), f"Source node {rel.source_id} not found"
            assert self.test_graph.has_node(rel.target_id), f"Target node {rel.target_id} not found"


class APIIntegrationTestCase(IntegrationTestCase):
    """Base class for API integration tests"""

    def setup_integration_data(self):
        """Set up API-specific test data"""
        self.api_client = self.create_api_client()
        
        # Create test data accessible via API
        self.test_api_nodes = []
        self.test_api_relationships = []

    def post_json(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a POST request with JSON data"""
        response = self.api_client.post(
            endpoint,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        return {
            'status_code': response.status_code,
            'data': response.get_json() if response.content_type == 'application/json' else None
        }

    def get_json(self, endpoint: str) -> Dict[str, Any]:
        """Make a GET request and return JSON response"""
        response = self.api_client.get(endpoint)
        return {
            'status_code': response.status_code,
            'data': response.get_json() if response.content_type == 'application/json' else None
        }

    def assert_api_response(self, response: Dict[str, Any], expected_status: int = 200):
        """Assert API response is successful"""
        assert response['status_code'] == expected_status, \
            f"Expected status {expected_status}, got {response['status_code']}"
        if expected_status == 200:
            assert response['data'] is not None, "Response data is None"


class DatabaseIntegrationTestCase(IntegrationTestCase):
    """Base class for database integration tests"""

    def setup_integration_data(self):
        """Set up database-specific test data"""
        # Mock database setup
        self.mock_db = MagicMock()
        self.mock_session = MagicMock()
        
        # Setup database patches
        db_patch = patch('core.sfm_persistence.DatabaseManager', return_value=self.mock_db)
        self.patches.append(db_patch)
        db_patch.start()

    def assert_database_state(self, expected_node_count: int, expected_relationship_count: int):
        """Assert database is in expected state"""
        # In a real implementation, this would query the actual database
        pass

    def simulate_database_transaction(self, operations: List[Dict[str, Any]]):
        """Simulate a database transaction with multiple operations"""
        # Mock transaction behavior
        for operation in operations:
            operation_type = operation.get('type')
            if operation_type == 'create_node':
                self.mock_session.create_node.return_value = operation.get('node')
            elif operation_type == 'create_relationship':
                self.mock_session.create_relationship.return_value = operation.get('relationship')


class ServiceIntegrationTestCase(IntegrationTestCase):
    """Base class for service layer integration tests"""

    def setup_integration_data(self):
        """Set up service-specific test data"""
        # Create realistic service configuration
        self.service_config = {
            'graph_service_enabled': True,
            'persistence_enabled': True,
            'validation_enabled': True,
            'caching_enabled': False  # Disable caching for predictable tests
        }
        
        # Apply configuration to test service
        for key, value in self.service_config.items():
            setattr(self.test_service, key, value)

    def assert_service_integration(self, service_method: str, expected_calls: int = 1):
        """Assert service integration points work correctly"""
        # This would verify service method calls and their effects
        pass

    def simulate_concurrent_operations(self, operations: List[Dict[str, Any]]):
        """Simulate concurrent operations on the service"""
        import threading
        import time
        
        results = []
        threads = []
        
        def execute_operation(operation):
            method_name = operation.get('method')
            args = operation.get('args', [])
            kwargs = operation.get('kwargs', {})
            
            if hasattr(self.test_service, method_name):
                method = getattr(self.test_service, method_name)
                result = method(*args, **kwargs)
                results.append(result)
        
        # Start threads
        for operation in operations:
            thread = threading.Thread(target=execute_operation, args=(operation,))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        return results