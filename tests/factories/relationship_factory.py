"""
Factory classes for generating test Relationship objects.

This module provides factory classes for creating various types of Relationship objects
with realistic test data using the factory-boy library.
"""
import factory
import uuid
from factory import Faker, LazyFunction
from typing import Dict, Any

from core.relationships import Relationship
from core.sfm_enums import RelationshipKind


class RelationshipFactory(factory.Factory):
    """Base factory for creating Relationship objects"""
    
    class Meta:
        model = Relationship

    source_id = factory.LazyFunction(lambda: uuid.uuid4())
    target_id = factory.LazyFunction(lambda: uuid.uuid4())
    kind = factory.Iterator([
        RelationshipKind.GOVERNS,
        RelationshipKind.REGULATES,
        RelationshipKind.AFFECTS,
        RelationshipKind.SUPPLIES,
        RelationshipKind.COMPETES_WITH,
        RelationshipKind.EMPLOYS,
        RelationshipKind.CONTRACTS_WITH
    ])
    weight = 1.0
    meta = LazyFunction(lambda: {
        'created_by': 'test_factory',
        'test_data': True,
        'strength': 'moderate',
        'confidence': 7
    })


class InfluenceRelationshipFactory(RelationshipFactory):
    """Factory for creating influence relationships"""
    
    kind = RelationshipKind.AFFECTS
    weight = 0.8
    meta = LazyFunction(lambda: {
        'influence_type': 'direct',
        'influence_strength': 8,
        'mechanism': 'regulation',
        'test_data': True
    })


class DependencyRelationshipFactory(RelationshipFactory):
    """Factory for creating dependency relationships"""
    
    relationship_type = RelationshipKind.SUPPLIES.value
    properties = LazyFunction(lambda: {
        'dependency_type': factory.Faker('random_element', elements=['resource', 'service', 'information', 'approval']).generate(),
        'criticality': factory.Faker('random_element', elements=['low', 'medium', 'high', 'critical']).generate(),
        'frequency': factory.Faker('random_element', elements=['daily', 'weekly', 'monthly', 'yearly']).generate(),
        'test_data': True
    })


class PartnershipRelationshipFactory(RelationshipFactory):
    """Factory for creating partnership relationships"""
    
    relationship_type = RelationshipKind.CONTRACTS_WITH.value
    properties = LazyFunction(lambda: {
        'partnership_type': factory.Faker('random_element', elements=['strategic', 'operational', 'financial', 'research']).generate(),
        'duration': factory.Faker('random_int', min=1, max=120).generate(),  # months
        'formality': factory.Faker('random_element', elements=['formal', 'informal', 'contractual']).generate(),
        'mutual_benefit': factory.Faker('boolean').generate(),
        'test_data': True
    })


class CompetitionRelationshipFactory(RelationshipFactory):
    """Factory for creating competition relationships"""
    
    relationship_type = RelationshipKind.COMPETES_WITH.value
    properties = LazyFunction(lambda: {
        'competition_type': factory.Faker('random_element', elements=['direct', 'indirect', 'substitute']).generate(),
        'market_overlap': factory.Faker('random_int', min=0, max=100).generate(),  # percentage
        'intensity': factory.Faker('random_element', elements=['low', 'moderate', 'high', 'intense']).generate(),
        'test_data': True
    })


class ContainsRelationshipFactory(RelationshipFactory):
    """Factory for creating containment relationships"""
    
    relationship_type = RelationshipKind.OWNS.value
    properties = LazyFunction(lambda: {
        'containment_type': factory.Faker('random_element', elements=['physical', 'organizational', 'conceptual']).generate(),
        'capacity': factory.Faker('random_int', min=1, max=1000).generate(),
        'current_usage': factory.Faker('random_int', min=0, max=100).generate(),  # percentage
        'test_data': True
    })


class FlowRelationshipFactory(RelationshipFactory):
    """Factory for creating flow relationships"""
    
    relationship_type = RelationshipKind.TRANSFERS.value
    properties = LazyFunction(lambda: {
        'flow_type': factory.Faker('random_element', elements=['material', 'information', 'energy', 'financial']).generate(),
        'volume': factory.Faker('random_int', min=1, max=10000).generate(),
        'frequency': factory.Faker('random_element', elements=['continuous', 'batch', 'periodic']).generate(),
        'direction': factory.Faker('random_element', elements=['unidirectional', 'bidirectional']).generate(),
        'test_data': True
    })


class TemporalRelationshipFactory(RelationshipFactory):
    """Factory for creating temporal relationships"""
    
    relationship_type = RelationshipKind.AFFECTS.value
    properties = LazyFunction(lambda: {
        'temporal_type': factory.Faker('random_element', elements=['immediate', 'delayed', 'conditional']).generate(),
        'delay_time': factory.Faker('random_int', min=0, max=365).generate(),  # days
        'causality': factory.Faker('random_element', elements=['causal', 'correlational', 'coincidental']).generate(),
        'test_data': True
    })


class RelationshipBatchFactory:
    """Factory for creating batches of relationships"""
    
    @staticmethod
    def create_relationship_network(nodes: list, density: float = 0.3):
        """Create a network of relationships between nodes"""
        import random
        from itertools import combinations
        
        relationships = []
        total_possible = len(list(combinations(nodes, 2)))
        target_count = int(total_possible * density)
        
        # Factories for different relationship types
        factories = [
            InfluenceRelationshipFactory,
            DependencyRelationshipFactory,
            PartnershipRelationshipFactory,
            CompetitionRelationshipFactory,
            ContainsRelationshipFactory,
            FlowRelationshipFactory,
            TemporalRelationshipFactory
        ]
        
        # Create random relationships
        node_pairs = list(combinations(nodes, 2))
        selected_pairs = random.sample(node_pairs, min(target_count, len(node_pairs)))
        
        for source_node, target_node in selected_pairs:
            factory_class = random.choice(factories)
            rel = factory_class.create(
                source_id=source_node.id,
                target_id=target_node.id
            )
            relationships.append(rel)
        
        return relationships
    
    @staticmethod
    def create_hierarchical_relationships(nodes: list):
        """Create hierarchical relationships between nodes"""
        relationships = []
        
        # Create tree-like structure
        for i in range(1, len(nodes)):
            parent_idx = (i - 1) // 2
            rel = ContainsRelationshipFactory.create(
                source_id=nodes[parent_idx].id,
                target_id=nodes[i].id
            )
            relationships.append(rel)
        
        return relationships
    
    @staticmethod
    def create_workflow_relationships(nodes: list):
        """Create workflow-like relationships between nodes"""
        relationships = []
        
        # Create sequential relationships
        for i in range(len(nodes) - 1):
            rel = TemporalRelationshipFactory.create(
                source_id=nodes[i].id,
                target_id=nodes[i + 1].id
            )
            relationships.append(rel)
        
        # Add some parallel dependencies
        for i in range(0, len(nodes) - 2, 2):
            rel = DependencyRelationshipFactory.create(
                source_id=nodes[i].id,
                target_id=nodes[i + 2].id
            )
            relationships.append(rel)
        
        return relationships