"""
Full workflow integration tests.

This module tests complete SFM workflows from end-to-end,
including API interactions, service processing, and data persistence.
"""
import pytest
from tests.integration.integration_base import APIIntegrationTestCase


class TestCompleteWorkflow(APIIntegrationTestCase):
    """Test complete SFM workflows end-to-end"""

    def test_node_lifecycle_workflow(self):
        """Test complete node creation, update, query, and deletion workflow"""
        # Create node through API
        node_data = {
            'name': 'Test Organization',
            'node_type': 'organization',
            'properties': {'industry': 'technology', 'size': 'medium'}
        }

        # Test node creation
        response = self.post_json('/api/nodes', node_data)
        self.assert_api_response(response, 201)
        
        created_node = response['data']
        node_id = created_node['id']
        assert created_node['name'] == 'Test Organization'
        assert created_node['node_type'] == 'organization'

        # Test node retrieval
        response = self.get_json(f'/api/nodes/{node_id}')
        self.assert_api_response(response, 200)
        
        retrieved_node = response['data']
        assert retrieved_node['name'] == 'Test Organization'
        assert retrieved_node['properties']['industry'] == 'technology'

        # Test node update
        update_data = {
            'properties': {
                'industry': 'fintech',
                'size': 'large',
                'headquarters': 'San Francisco'
            }
        }
        
        response = self.api_client.patch(
            f'/api/nodes/{node_id}',
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 200
        
        updated_node = response.get_json()
        assert updated_node['properties']['industry'] == 'fintech'
        assert updated_node['properties']['size'] == 'large'

        # Test relationship creation
        target_node_data = {
            'name': 'Partner Company',
            'node_type': 'organization',
            'properties': {'industry': 'consulting'}
        }
        
        target_response = self.post_json('/api/nodes', target_node_data)
        self.assert_api_response(target_response, 201)
        target_node_id = target_response['data']['id']

        relationship_data = {
            'source_id': node_id,
            'target_id': target_node_id,
            'relationship_type': 'partners_with',
            'properties': {'partnership_type': 'strategic'}
        }

        response = self.post_json('/api/relationships', relationship_data)
        self.assert_api_response(response, 201)
        
        created_relationship = response['data']
        assert created_relationship['source_id'] == node_id
        assert created_relationship['target_id'] == target_node_id
        assert created_relationship['relationship_type'] == 'partners_with'

        # Test graph query
        response = self.get_json(f'/api/nodes/{node_id}/neighbors')
        self.assert_api_response(response, 200)
        
        neighbors = response['data']['neighbors']
        assert len(neighbors) == 1
        assert neighbors[0]['id'] == target_node_id

        # Test node deletion
        response = self.api_client.delete(f'/api/nodes/{node_id}')
        assert response.status_code == 204

        # Verify node is deleted
        response = self.get_json(f'/api/nodes/{node_id}')
        assert response['status_code'] == 404

    def test_batch_operations_workflow(self):
        """Test batch operations for creating multiple nodes and relationships"""
        # Create multiple nodes in batch
        batch_nodes = [
            {
                'name': f'Company {i}',
                'node_type': 'organization',
                'properties': {'industry': 'technology', 'size': 'small'}
            }
            for i in range(5)
        ]

        response = self.post_json('/api/nodes/batch', {'nodes': batch_nodes})
        self.assert_api_response(response, 201)
        
        created_nodes = response['data']['nodes']
        assert len(created_nodes) == 5

        # Create relationships between nodes
        batch_relationships = []
        for i in range(4):
            batch_relationships.append({
                'source_id': created_nodes[i]['id'],
                'target_id': created_nodes[i + 1]['id'],
                'relationship_type': 'partners_with',
                'properties': {'partnership_type': 'operational'}
            })

        response = self.post_json('/api/relationships/batch', {'relationships': batch_relationships})
        self.assert_api_response(response, 201)
        
        created_relationships = response['data']['relationships']
        assert len(created_relationships) == 4

        # Test network query
        response = self.get_json(f'/api/nodes/{created_nodes[0]["id"]}/network?depth=3')
        self.assert_api_response(response, 200)
        
        network = response['data']
        assert len(network['nodes']) == 5
        assert len(network['relationships']) == 4

    def test_search_and_filter_workflow(self):
        """Test search and filtering functionality"""
        # Create diverse test data
        test_nodes = [
            {
                'name': 'TechCorp',
                'node_type': 'organization',
                'properties': {'industry': 'technology', 'size': 'large', 'location': 'Silicon Valley'}
            },
            {
                'name': 'FinanceInc',
                'node_type': 'organization',
                'properties': {'industry': 'finance', 'size': 'medium', 'location': 'Wall Street'}
            },
            {
                'name': 'John Doe',
                'node_type': 'person',
                'properties': {'occupation': 'software engineer', 'location': 'Silicon Valley'}
            }
        ]

        created_nodes = []
        for node_data in test_nodes:
            response = self.post_json('/api/nodes', node_data)
            self.assert_api_response(response, 201)
            created_nodes.append(response['data'])

        # Test search by name
        response = self.get_json('/api/nodes/search?name=TechCorp')
        self.assert_api_response(response, 200)
        
        search_results = response['data']['nodes']
        assert len(search_results) == 1
        assert search_results[0]['name'] == 'TechCorp'

        # Test filter by node type
        response = self.get_json('/api/nodes?node_type=organization')
        self.assert_api_response(response, 200)
        
        filtered_results = response['data']['nodes']
        organization_nodes = [n for n in filtered_results if n['node_type'] == 'organization']
        assert len(organization_nodes) >= 2

        # Test filter by property
        response = self.get_json('/api/nodes?properties.industry=technology')
        self.assert_api_response(response, 200)
        
        tech_nodes = response['data']['nodes']
        assert len(tech_nodes) >= 1
        assert all(n['properties']['industry'] == 'technology' for n in tech_nodes)

    def test_analytics_workflow(self):
        """Test analytics and metrics calculation workflow"""
        # Create test network
        from tests.factories.node_factory import GraphFactory
        test_graph = GraphFactory.create_small_graph(nodes=10, relationships=15)

        # Upload test graph via API
        graph_data = {
            'nodes': [
                {
                    'id': node.id,
                    'name': node.name,
                    'node_type': node.node_type,
                    'properties': node.properties
                }
                for node in test_graph.nodes.values()
            ],
            'relationships': [
                {
                    'id': rel.id,
                    'source_id': rel.source_id,
                    'target_id': rel.target_id,
                    'relationship_type': rel.relationship_type,
                    'properties': rel.properties
                }
                for rel in test_graph.relationships.values()
            ]
        }

        response = self.post_json('/api/graphs', graph_data)
        self.assert_api_response(response, 201)
        
        graph_id = response['data']['id']

        # Test network metrics calculation
        response = self.get_json(f'/api/graphs/{graph_id}/metrics')
        self.assert_api_response(response, 200)
        
        metrics = response['data']
        assert 'node_count' in metrics
        assert 'relationship_count' in metrics
        assert 'density' in metrics
        assert 'clustering_coefficient' in metrics

        # Test centrality analysis
        response = self.get_json(f'/api/graphs/{graph_id}/centrality')
        self.assert_api_response(response, 200)
        
        centrality = response['data']
        assert 'degree_centrality' in centrality
        assert 'betweenness_centrality' in centrality
        assert 'closeness_centrality' in centrality

        # Test community detection
        response = self.get_json(f'/api/graphs/{graph_id}/communities')
        self.assert_api_response(response, 200)
        
        communities = response['data']['communities']
        assert len(communities) > 0
        assert all('nodes' in community for community in communities)