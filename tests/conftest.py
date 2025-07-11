"""
Comprehensive test configuration for SFM system.

This module provides centralized configuration for all test types
including fixtures, test data, and test environment setup.
"""
import pytest
import tempfile
import os
from typing import Dict, Any, List
from unittest.mock import MagicMock

from tests.factories.node_factory import NodeFactory, OrganizationNodeFactory, PersonNodeFactory, GraphFactory
from tests.factories.relationship_factory import RelationshipFactory
from core.graph import SFMGraph
from core.sfm_service import SFMService


@pytest.fixture(scope="session")
def test_database():
    """Set up test database for the entire test session"""
    # In a real implementation, this would set up a test database
    mock_db = MagicMock()
    mock_db.connection_string = "test://localhost/test_db"
    mock_db.is_connected = True
    
    yield mock_db
    
    # Cleanup
    mock_db.close()


@pytest.fixture(scope="function")
def clean_database(test_database):
    """Ensure clean database state for each test"""
    # In a real implementation, this would truncate tables
    test_database.truncate_all_tables = MagicMock()
    test_database.truncate_all_tables()
    
    yield test_database


@pytest.fixture
def api_client():
    """Create test API client"""
    from api.sfm_api import create_app
    app = create_app(testing=True)
    
    # Configure for testing
    app.config['TESTING'] = True
    app.config['DATABASE_URL'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_graph():
    """Create a clean test graph for each test"""
    graph = SFMGraph()
    yield graph
    graph.clear()


@pytest.fixture
def small_test_graph():
    """Create small test graph with predefined data"""
    return GraphFactory.create_small_graph(nodes=5, relationships=7)


@pytest.fixture
def medium_test_graph():
    """Create medium test graph with predefined data"""
    return GraphFactory.create_small_graph(nodes=50, relationships=100)


@pytest.fixture
def large_test_graph():
    """Create large test graph for performance testing"""
    return GraphFactory.create_large_graph(nodes=1000, relationships=5000)


@pytest.fixture
def test_service(clean_database):
    """Create test service with mocked dependencies"""
    service = SFMService()
    
    # Mock external dependencies
    service.database = clean_database
    service.cache = MagicMock()
    service.external_api = MagicMock()
    
    return service


@pytest.fixture
def test_nodes():
    """Create a set of test nodes"""
    return [
        OrganizationNodeFactory.create(id="org_1", name="Test Organization 1"),
        OrganizationNodeFactory.create(id="org_2", name="Test Organization 2"),
        PersonNodeFactory.create(id="person_1", name="Test Person 1"),
        PersonNodeFactory.create(id="person_2", name="Test Person 2"),
        NodeFactory.create(id="resource_1", name="Test Resource 1", node_type="resource")
    ]


@pytest.fixture
def test_relationships(test_nodes):
    """Create a set of test relationships"""
    return [
        RelationshipFactory.create(
            id="rel_1",
            source_id="org_1",
            target_id="person_1",
            relationship_type="employs"
        ),
        RelationshipFactory.create(
            id="rel_2",
            source_id="org_2",
            target_id="person_2",
            relationship_type="employs"
        ),
        RelationshipFactory.create(
            id="rel_3",
            source_id="org_1",
            target_id="org_2",
            relationship_type="partners_with"
        )
    ]


@pytest.fixture
def populated_graph(test_graph, test_nodes, test_relationships):
    """Create a graph populated with test data"""
    # Add nodes
    for node in test_nodes:
        test_graph.add_node(node)
    
    # Add relationships
    for rel in test_relationships:
        test_graph.add_relationship(rel)
    
    return test_graph


@pytest.fixture
def temp_file():
    """Create a temporary file for testing"""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        yield f.name
    
    # Cleanup
    if os.path.exists(f.name):
        os.unlink(f.name)


@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_external_services():
    """Mock external services and APIs"""
    mocks = {
        'database': MagicMock(),
        'cache': MagicMock(),
        'external_api': MagicMock(),
        'message_queue': MagicMock(),
        'file_storage': MagicMock()
    }
    
    # Configure mock responses
    mocks['database'].query.return_value = []
    mocks['cache'].get.return_value = None
    mocks['external_api'].fetch.return_value = {'status': 'success'}
    
    yield mocks


@pytest.fixture
def performance_monitor():
    """Performance monitoring fixture"""
    import time
    import psutil
    
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.start_memory = None
            self.metrics = {}
        
        def start(self):
            self.start_time = time.time()
            self.start_memory = psutil.Process().memory_info().rss
        
        def stop(self):
            if self.start_time is not None:
                self.metrics['execution_time'] = time.time() - self.start_time
                self.metrics['memory_used'] = psutil.Process().memory_info().rss - self.start_memory
                return self.metrics
            return {}
    
    return PerformanceMonitor()


@pytest.fixture
def integration_environment():
    """Set up integration test environment"""
    env = {
        'api_base_url': 'http://localhost:8000',
        'database_url': 'sqlite:///:memory:',
        'cache_url': 'redis://localhost:6379/1',
        'test_mode': True,
        'debug': True
    }
    
    # Set environment variables
    for key, value in env.items():
        os.environ[f'TEST_{key.upper()}'] = str(value)
    
    yield env
    
    # Cleanup environment variables
    for key in env.keys():
        env_var = f'TEST_{key.upper()}'
        if env_var in os.environ:
            del os.environ[env_var]


# Test markers configuration
pytest_plugins = ['pytest_benchmark']


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "property: marks tests as property-based tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Add markers based on test file location
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        elif "property" in str(item.fspath):
            item.add_marker(pytest.mark.property)
        else:
            item.add_marker(pytest.mark.unit)


@pytest.fixture(autouse=True)
def test_isolation():
    """Ensure test isolation"""
    # Clear any global state before each test
    import gc
    gc.collect()
    
    yield
    
    # Cleanup after each test
    gc.collect()


# Custom test data generators
class TestDataGenerator:
    """Utility class for generating test data"""
    
    @staticmethod
    def create_node_batch(count: int, node_type: str = "test") -> List[Any]:
        """Create a batch of test nodes"""
        if node_type == "organization":
            return [OrganizationNodeFactory.create() for _ in range(count)]
        elif node_type == "person":
            return [PersonNodeFactory.create() for _ in range(count)]
        else:
            return [NodeFactory.create(node_type=node_type) for _ in range(count)]
    
    @staticmethod
    def create_relationship_batch(nodes: List[Any], count: int) -> List[Any]:
        """Create a batch of relationships between nodes"""
        import random
        relationships = []
        
        for _ in range(count):
            if len(nodes) >= 2:
                source = random.choice(nodes)
                target = random.choice(nodes)
                if source.id != target.id:
                    rel = RelationshipFactory.create(
                        source_id=source.id,
                        target_id=target.id
                    )
                    relationships.append(rel)
        
        return relationships


@pytest.fixture
def test_data_generator():
    """Provide test data generator"""
    return TestDataGenerator()


# Test utilities
class TestUtils:
    """Utility functions for testing"""
    
    @staticmethod
    def assert_graph_structure(graph: SFMGraph, expected_nodes: int, expected_relationships: int):
        """Assert graph has expected structure"""
        assert graph.node_count() == expected_nodes, f"Expected {expected_nodes} nodes, got {graph.node_count()}"
        assert graph.relationship_count() == expected_relationships, f"Expected {expected_relationships} relationships, got {graph.relationship_count()}"
    
    @staticmethod
    def assert_performance_threshold(execution_time: float, threshold: float, operation_name: str = "Operation"):
        """Assert performance threshold"""
        assert execution_time < threshold, f"{operation_name} took {execution_time:.3f}s, expected < {threshold}s"
    
    @staticmethod
    def create_mock_response(status_code: int = 200, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create mock HTTP response"""
        return {
            'status_code': status_code,
            'data': data or {},
            'headers': {'Content-Type': 'application/json'}
        }


@pytest.fixture
def test_utils():
    """Provide test utilities"""
    return TestUtils()