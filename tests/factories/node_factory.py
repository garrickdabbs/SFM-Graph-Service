"""
Factory classes for generating test Node objects.

This module provides factory classes for creating various types of Node objects
with realistic test data using the factory-boy library.
"""
import factory
import uuid
from factory import Faker, SubFactory, LazyFunction
from typing import Dict, Any

from core.base_nodes import Node
from core.core_nodes import Actor


class NodeFactory(factory.Factory):
    """Base factory for creating Node objects"""
    
    class Meta:
        model = Actor

    label = Faker('company')
    description = Faker('text', max_nb_chars=100)
    id = factory.LazyFunction(lambda: uuid.uuid4())
    meta = LazyFunction(lambda: {
        'node_type': 'actor',
        'created_by': 'test_factory',
        'test_data': True
    })


class OrganizationNodeFactory(NodeFactory):
    """Factory for creating organization nodes"""
    
    label = Faker('company')
    description = "Test organization"
    meta = LazyFunction(lambda: {
        'node_type': 'organization',
        'industry': 'technology',
        'size': 'medium',
        'headquarters': 'San Francisco',
        'founded_year': 2020,
        'test_data': True
    })


class PersonNodeFactory(NodeFactory):
    """Factory for creating person nodes"""
    
    label = Faker('name')
    description = "Test person"
    meta = LazyFunction(lambda: {
        'node_type': 'person',
        'age': 35,
        'occupation': 'engineer',
        'location': 'San Francisco',
        'email': 'test@example.com',
        'test_data': True
    })


class InstitutionNodeFactory(NodeFactory):
    """Factory for creating institution nodes"""
    
    node_type = 'institution'
    name = Faker('company')
    properties = LazyFunction(lambda: {
        'type': 'government',
        'established': 1950,
        'location': 'Washington DC',
        'description': 'Test institution',
        'test_data': True
    })


class ResourceNodeFactory(NodeFactory):
    """Factory for creating resource nodes"""
    
    node_type = 'resource'
    name = Faker('word')
    properties = LazyFunction(lambda: {
        'resource_type': 'natural',
        'availability': 'abundant',
        'unit': 'kg',
        'cost': 100,
        'test_data': True
    })


class ProcessNodeFactory(NodeFactory):
    """Factory for creating process nodes"""
    
    node_type = 'process'
    name = Faker('bs')
    properties = LazyFunction(lambda: {
        'process_type': 'manufacturing',
        'duration': 30,
        'complexity': 'medium',
        'automation_level': 'semi_automated',
        'test_data': True
    })


class PolicyNodeFactory(NodeFactory):
    """Factory for creating policy nodes"""
    
    node_type = 'policy'
    name = Faker('catch_phrase')
    properties = LazyFunction(lambda: {
        'policy_type': 'regulatory',
        'effective_date': '2023-01-01',
        'jurisdiction': 'federal',
        'status': 'active',
        'test_data': True
    })


class GraphFactory:
    """Factory for creating complete graphs with nodes and relationships"""
    
    @staticmethod
    def create_small_graph(nodes: int = 5, relationships: int = 7):
        """Create a small test graph"""
        from core.graph import SFMGraph
        from tests.factories.relationship_factory import RelationshipFactory
        
        graph = SFMGraph()
        
        # Create nodes
        node_factories = [
            OrganizationNodeFactory,
            PersonNodeFactory,
            InstitutionNodeFactory,
            ResourceNodeFactory,
            ProcessNodeFactory
        ]
        
        created_nodes = []
        for i in range(nodes):
            factory_class = node_factories[i % len(node_factories)]
            node = factory_class.create()
            graph.add_node(node)
            created_nodes.append(node)
        
        # Create relationships
        for i in range(relationships):
            source_node = created_nodes[i % len(created_nodes)]
            target_node = created_nodes[(i + 1) % len(created_nodes)]
            rel = RelationshipFactory.create(
                source_id=source_node.id,
                target_id=target_node.id
            )
            graph.add_relationship(rel)
        
        return graph
    
    @staticmethod
    def create_large_graph(nodes: int = 1000, relationships: int = 5000):
        """Create a large test graph for performance testing"""
        from core.graph import SFMGraph
        from tests.factories.relationship_factory import RelationshipFactory
        import random
        
        graph = SFMGraph()
        
        # Create nodes
        node_factories = [
            OrganizationNodeFactory,
            PersonNodeFactory,
            InstitutionNodeFactory,
            ResourceNodeFactory,
            ProcessNodeFactory,
            PolicyNodeFactory
        ]
        
        created_nodes = []
        for i in range(nodes):
            factory_class = random.choice(node_factories)
            node = factory_class.create()
            graph.add_node(node)
            created_nodes.append(node)
        
        # Create relationships
        for i in range(relationships):
            source_node = random.choice(created_nodes)
            target_node = random.choice(created_nodes)
            if source_node.id != target_node.id:  # Avoid self-loops
                rel = RelationshipFactory.create(
                    source_id=source_node.id,
                    target_id=target_node.id
                )
                graph.add_relationship(rel)
        
        return graph