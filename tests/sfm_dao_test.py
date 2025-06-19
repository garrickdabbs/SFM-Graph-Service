import unittest
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

import networkx as nx

from core.sfm_models import (
    Node, Actor, Institution, Resource, Process, Flow, Relationship,
    BeliefSystem, Policy, TechnologySystem, Indicator, FeedbackLoop,
    SFMGraph, RelationshipKind
)
from core.enums import ResourceType
from db.sfm_dao import (
    SFMRepository, NetworkXSFMRepository, TypedSFMRepository,
    ActorRepository, InstitutionRepository, PolicyRepository, 
    ResourceRepository, RelationshipRepository, SFMRepositoryFactory
)


class TestNetworkXSFMRepositoryUnit(unittest.TestCase):
    """Unit tests for NetworkXSFMRepository."""

    def setUp(self):
        self.repo = NetworkXSFMRepository()
        
        # Create some test nodes
        self.actor1 = Actor(label="Test Actor 1", sector="Government")
        self.actor2 = Actor(label="Test Actor 2", sector="Private")
        self.institution = Institution(label="Test Institution")
        
        # Create relationships
        self.relationship = Relationship(
            source_id=self.actor1.id,
            target_id=self.actor2.id,
            kind=RelationshipKind.GOVERNS,
            weight=0.75
        )

    def test_create_node(self):
        # Test creating a node
        created_node = self.repo.create_node(self.actor1)
        self.assertEqual(created_node, self.actor1)
        self.assertTrue(self.actor1.id in self.repo.graph)
        
        # Test creating a duplicate node
        with self.assertRaises(ValueError):
            self.repo.create_node(self.actor1)

    def test_read_node(self):
        self.repo.create_node(self.actor1)
        
        # Test reading existing node
        read_node = self.repo.read_node(self.actor1.id)
        self.assertEqual(read_node, self.actor1)
        
        # Test reading non-existent node
        nonexistent_id = uuid.uuid4()
        self.assertIsNone(self.repo.read_node(nonexistent_id))

    def test_update_node(self):
        self.repo.create_node(self.actor1)
        
        # Modify the node
        self.actor1.label = "Updated Actor"
        
        # Test updating
        updated_node = self.repo.update_node(self.actor1)
        self.assertEqual(updated_node.label, "Updated Actor")
        
        # Verify the update in storage
        stored_node = self.repo.read_node(self.actor1.id)
        self.assertEqual(stored_node.label, "Updated Actor") #type: ignore[exists-in-supertype]
        
        # Test updating non-existent node
        non_existent = Actor(label="Non-existent")
        with self.assertRaises(ValueError):
            self.repo.update_node(non_existent)

    def test_delete_node(self):
        self.repo.create_node(self.actor1)
        
        # Test successful deletion
        self.assertTrue(self.repo.delete_node(self.actor1.id))
        self.assertIsNone(self.repo.read_node(self.actor1.id))
        
        # Test deleting non-existent node
        self.assertFalse(self.repo.delete_node(uuid.uuid4()))

    def test_list_nodes(self):
        self.repo.create_node(self.actor1)
        self.repo.create_node(self.actor2)
        self.repo.create_node(self.institution)
        
        # Test listing all nodes
        all_nodes = self.repo.list_nodes()
        self.assertEqual(len(all_nodes), 3)
        
        # Test filtering by type
        actors = self.repo.list_nodes(Actor)
        self.assertEqual(len(actors), 2)
        institutions = self.repo.list_nodes(Institution)
        self.assertEqual(len(institutions), 1)

    def test_create_relationship(self):
        # Add nodes first
        self.repo.create_node(self.actor1)
        self.repo.create_node(self.actor2)
        
        # Test creating relationship
        created_rel = self.repo.create_relationship(self.relationship)
        self.assertEqual(created_rel, self.relationship)
        
        # Test creating with missing source
        self.repo.delete_node(self.actor1.id)
        with self.assertRaises(ValueError):
            self.repo.create_relationship(self.relationship)
            
        # Restore actor1 and test with missing target
        self.repo.create_node(self.actor1)
        self.repo.delete_node(self.actor2.id)
        with self.assertRaises(ValueError):
            self.repo.create_relationship(self.relationship)
            
        # Test duplicate
        self.repo.create_node(self.actor2)
        self.repo.create_relationship(self.relationship)
        with self.assertRaises(ValueError):
            self.repo.create_relationship(self.relationship)

    def test_read_relationship(self):
        self.repo.create_node(self.actor1)
        self.repo.create_node(self.actor2)
        self.repo.create_relationship(self.relationship)
        
        # Test reading existing relationship
        read_rel = self.repo.read_relationship(self.relationship.id)
        self.assertEqual(read_rel, self.relationship)
        
        # Test reading non-existent relationship
        nonexistent_id = uuid.uuid4()
        self.assertIsNone(self.repo.read_relationship(nonexistent_id))

    def test_update_relationship(self):
        self.repo.create_node(self.actor1)
        self.repo.create_node(self.actor2)
        self.repo.create_relationship(self.relationship)
        
        # Modify the relationship
        self.relationship.weight = 0.9
        
        # Test updating
        updated_rel = self.repo.update_relationship(self.relationship)
        self.assertEqual(updated_rel.weight, 0.9)
        
        # Verify the update in storage
        stored_rel = self.repo.read_relationship(self.relationship.id)
        self.assertEqual(stored_rel.weight, 0.9) #type: ignore[exists-in-supertype]
        
        # Test updating non-existent relationship
        non_existent = Relationship(
            source_id=uuid.uuid4(),
            target_id=uuid.uuid4(),
            kind=RelationshipKind.GOVERNS
        )
        with self.assertRaises(ValueError):
            self.repo.update_relationship(non_existent)

    def test_delete_relationship(self):
        self.repo.create_node(self.actor1)
        self.repo.create_node(self.actor2)
        self.repo.create_relationship(self.relationship)
        
        # Test successful deletion
        self.assertTrue(self.repo.delete_relationship(self.relationship.id))
        self.assertIsNone(self.repo.read_relationship(self.relationship.id))
        
        # Test deleting non-existent relationship
        self.assertFalse(self.repo.delete_relationship(uuid.uuid4()))

    def test_list_relationships(self):
        self.repo.create_node(self.actor1)
        self.repo.create_node(self.actor2)
        self.repo.create_node(self.institution)
        
        # Create two relationships with different kinds
        rel1 = Relationship(
            source_id=self.actor1.id,
            target_id=self.actor2.id,
            kind=RelationshipKind.GOVERNS
        )
        rel2 = Relationship(
            source_id=self.actor2.id,
            target_id=self.institution.id,
            kind=RelationshipKind.SERVES
        )
        self.repo.create_relationship(rel1)
        self.repo.create_relationship(rel2)
        
        # Test listing all relationships
        all_rels = self.repo.list_relationships()
        self.assertEqual(len(all_rels), 2)
        
        # Test filtering by kind
        governs_rels = self.repo.list_relationships(RelationshipKind.GOVERNS)
        self.assertEqual(len(governs_rels), 1)
        self.assertEqual(governs_rels[0].kind, RelationshipKind.GOVERNS)

    def test_find_relationships(self):
        # Create test setup
        self.repo.create_node(self.actor1)
        self.repo.create_node(self.actor2)
        self.repo.create_node(self.institution)
        
        rel1 = Relationship(
            source_id=self.actor1.id,
            target_id=self.actor2.id,
            kind=RelationshipKind.GOVERNS
        )
        rel2 = Relationship(
            source_id=self.actor1.id,
            target_id=self.institution.id,
            kind=RelationshipKind.SERVES
        )
        rel3 = Relationship(
            source_id=self.actor2.id,
            target_id=self.institution.id,
            kind=RelationshipKind.SERVES
        )
        
        self.repo.create_relationship(rel1)
        self.repo.create_relationship(rel2)
        self.repo.create_relationship(rel3)
        
        # Test finding by source
        source_rels = self.repo.find_relationships(source_id=self.actor1.id)
        self.assertEqual(len(source_rels), 2)
        
        # Test finding by target
        target_rels = self.repo.find_relationships(target_id=self.institution.id)
        self.assertEqual(len(target_rels), 2)
        
        # Test finding by kind
        kind_rels = self.repo.find_relationships(kind=RelationshipKind.SERVES)
        self.assertEqual(len(kind_rels), 2)
        
        # Test combined filters
        combined_rels = self.repo.find_relationships(
            source_id=self.actor1.id,
            target_id=self.institution.id,
            kind=RelationshipKind.SERVES
        )
        self.assertEqual(len(combined_rels), 1)
        self.assertEqual(combined_rels[0].source_id, self.actor1.id)
        self.assertEqual(combined_rels[0].target_id, self.institution.id)
        self.assertEqual(combined_rels[0].kind, RelationshipKind.SERVES)

    def test_clear(self):
        # Add some data
        self.repo.create_node(self.actor1)
        self.repo.create_node(self.actor2)
        self.repo.create_relationship(self.relationship)
        
        # Verify data exists
        self.assertEqual(len(self.repo.list_nodes()), 2)
        self.assertEqual(len(self.repo.list_relationships()), 1)
        
        # Clear and verify
        self.repo.clear()
        self.assertEqual(len(self.repo.list_nodes()), 0)
        self.assertEqual(len(self.repo.list_relationships()), 0)


class TestTypedSFMRepositoryUnit(unittest.TestCase):
    """Unit tests for TypedSFMRepository."""

    def setUp(self):
        self.base_repo = NetworkXSFMRepository()
        self.actor_repo = TypedSFMRepository(self.base_repo, Actor)
        
        # Create test data
        self.actor = Actor(label="Test Actor", sector="Government")
        self.institution = Institution(label="Test Institution")

    def test_create(self):
        # Test correct type
        created = self.actor_repo.create(self.actor)
        self.assertEqual(created, self.actor)
        
        # Test wrong type
        with self.assertRaises(TypeError):
            self.actor_repo.create(self.institution) #type: ignore[expected-type] this is testing a type error

    def test_read(self):
        # Add nodes
        self.base_repo.create_node(self.actor)
        self.base_repo.create_node(self.institution)
        
        # Should find actors
        actor = self.actor_repo.read(self.actor.id)
        self.assertEqual(actor, self.actor)
        
        # Should not find institutions
        self.assertIsNone(self.actor_repo.read(self.institution.id))
        
        # Should not find non-existent nodes
        self.assertIsNone(self.actor_repo.read(uuid.uuid4()))

    def test_update(self):
        # Add node
        self.actor_repo.create(self.actor)
        
        # Update
        self.actor.label = "Updated Actor"
        updated = self.actor_repo.update(self.actor)
        self.assertEqual(updated.label, "Updated Actor")
        
        # Test wrong type
        with self.assertRaises(TypeError):
            self.actor_repo.update(self.institution) #type: ignore[expected-type] this is testing a type error

    def test_delete(self):
        self.actor_repo.create(self.actor)
        self.assertTrue(self.actor_repo.delete(self.actor.id))
        self.assertIsNone(self.actor_repo.read(self.actor.id))

    def test_list_all(self):
        # Add mixed types to base repo
        self.base_repo.create_node(self.actor)
        self.base_repo.create_node(self.institution)
        
        # Should only list actors
        actors = self.actor_repo.list_all()
        self.assertEqual(len(actors), 1)
        self.assertEqual(actors[0], self.actor)

    def test_query(self):
        # Add test actors with different attributes
        actor1 = Actor(label="Actor 1", sector="Government", legal_form="Federal")
        actor2 = Actor(label="Actor 2", sector="Government", legal_form="State")
        actor3 = Actor(label="Actor 3", sector="Private", legal_form="Corporation")
        
        self.actor_repo.create(actor1)
        self.actor_repo.create(actor2)
        self.actor_repo.create(actor3)
        
        # Query by a single attribute
        govt_actors = self.actor_repo.query({"sector": "Government"})
        self.assertEqual(len(govt_actors), 2)
        
        # Query by multiple attributes
        fed_govt_actors = self.actor_repo.query({
            "sector": "Government",
            "legal_form": "Federal"
        })
        self.assertEqual(len(fed_govt_actors), 1)
        self.assertEqual(fed_govt_actors[0].label, "Actor 1")
        
        # Query with no matches
        no_matches = self.actor_repo.query({"sector": "Nonprofit"})
        self.assertEqual(len(no_matches), 0)
        
        # Query with non-existent attribute
        empty_result = self.actor_repo.query({"non_existent": "value"})
        self.assertEqual(len(empty_result), 0)


class TestSpecializedRepositoriesUnit(unittest.TestCase):
    """Unit tests for specialized repository classes."""

    def setUp(self):
        self.base_repo = NetworkXSFMRepository()
        self.actor_repo = ActorRepository(self.base_repo)
        self.institution_repo = InstitutionRepository(self.base_repo)
        self.policy_repo = PolicyRepository(self.base_repo)
        self.resource_repo = ResourceRepository(self.base_repo)
        self.relationship_repo = RelationshipRepository(self.base_repo)
        
        # Create test data
        self.actor1 = Actor(label="Test Actor 1", sector="Government")
        self.actor2 = Actor(label="Test Actor 2", sector="Private", legal_form="Corporation")
        self.institution = Institution(label="Test Institution")
        self.policy = Policy(
            label="Test Policy", 
            authority="EPA",
            target_sectors=["Energy", "Transportation"]
        )
        self.resource = Resource(
            label="Test Resource",
            rtype=ResourceType.NATURAL
        )
        
        # Create a relationship
        self.relationship = Relationship(
            source_id=self.actor1.id,
            target_id=self.actor2.id,
            kind=RelationshipKind.GOVERNS
        )
        
        # Add data to repositories
        self.actor_repo.create(self.actor1)
        self.actor_repo.create(self.actor2)
        self.institution_repo.create(self.institution)
        self.policy_repo.create(self.policy)
        self.resource_repo.create(self.resource)
        self.relationship_repo.create(self.relationship)

    def test_actor_repository_specialized_methods(self):
        # Test find_by_sector
        govt_actors = self.actor_repo.find_by_sector("Government")
        self.assertEqual(len(govt_actors), 1)
        self.assertEqual(govt_actors[0].label, "Test Actor 1")
        
        # Test find_by_legal_form
        corp_actors = self.actor_repo.find_by_legal_form("Corporation")
        self.assertEqual(len(corp_actors), 1)
        self.assertEqual(corp_actors[0].label, "Test Actor 2")

    def test_policy_repository_specialized_methods(self):
        # Test find_by_authority
        epa_policies = self.policy_repo.find_by_authority("EPA")
        self.assertEqual(len(epa_policies), 1)
        self.assertEqual(epa_policies[0].label, "Test Policy")
        
        # Test find_by_target_sector
        energy_policies = self.policy_repo.find_by_target_sector("Energy")
        self.assertEqual(len(energy_policies), 1)
        self.assertEqual(energy_policies[0].label, "Test Policy")
        
        transportation_policies = self.policy_repo.find_by_target_sector("Transportation")
        self.assertEqual(len(transportation_policies), 1)
        
        agriculture_policies = self.policy_repo.find_by_target_sector("Agriculture")
        self.assertEqual(len(agriculture_policies), 0)

    def test_resource_repository_specialized_methods(self):
        # Test find_by_type
        natural_resources = self.resource_repo.find_by_type(ResourceType.NATURAL)
        self.assertEqual(len(natural_resources), 1)
        self.assertEqual(natural_resources[0].label, "Test Resource")
        
        produced_resources = self.resource_repo.find_by_type(ResourceType.PRODUCED)
        self.assertEqual(len(produced_resources), 0)

    def test_relationship_repository_methods(self):
        # Test find_by_kind
        governs_rels = self.relationship_repo.find_by_kind(RelationshipKind.GOVERNS)
        self.assertEqual(len(governs_rels), 1)
        
        # Test find_by_source
        source_rels = self.relationship_repo.find_by_source(self.actor1.id)
        self.assertEqual(len(source_rels), 1)
        self.assertEqual(source_rels[0].source_id, self.actor1.id)
        
        # Test find_by_target
        target_rels = self.relationship_repo.find_by_target(self.actor2.id)
        self.assertEqual(len(target_rels), 1)
        self.assertEqual(target_rels[0].target_id, self.actor2.id)
        
        # Test find_by_nodes
        node_rels = self.relationship_repo.find_by_nodes(
            self.actor1.id,
            self.actor2.id
        )
        self.assertEqual(len(node_rels), 1)
        self.assertEqual(node_rels[0].source_id, self.actor1.id)
        self.assertEqual(node_rels[0].target_id, self.actor2.id)


class TestSFMRepositoryFactoryUnit(unittest.TestCase):
    """Unit tests for SFMRepositoryFactory."""

    def test_create_repository(self):
        # Test creating with default
        default_repo = SFMRepositoryFactory.create_repository()
        self.assertIsInstance(default_repo, NetworkXSFMRepository)
        
        # Test creating with networkx explicitly
        nx_repo = SFMRepositoryFactory.create_repository("networkx")
        self.assertIsInstance(nx_repo, NetworkXSFMRepository)
        
        # Test unsupported storage type
        with self.assertRaises(ValueError):
            SFMRepositoryFactory.create_repository("unsupported_storage")

    def test_create_specialized_repositories(self):
        # Test creating actor repository
        actor_repo = SFMRepositoryFactory.create_actor_repository()
        self.assertIsInstance(actor_repo, ActorRepository)
        
        # Test creating institution repository
        inst_repo = SFMRepositoryFactory.create_institution_repository()
        self.assertIsInstance(inst_repo, InstitutionRepository)
        
        # Test creating policy repository
        policy_repo = SFMRepositoryFactory.create_policy_repository()
        self.assertIsInstance(policy_repo, PolicyRepository)
        
        # Test creating resource repository
        resource_repo = SFMRepositoryFactory.create_resource_repository()
        self.assertIsInstance(resource_repo, ResourceRepository)
        
        # Test creating relationship repository
        rel_repo = SFMRepositoryFactory.create_relationship_repository()
        self.assertIsInstance(rel_repo, RelationshipRepository)


class TestSFMRepositoryIntegration(unittest.TestCase):
    """Integration tests for SFM repositories."""

    def setUp(self):
        # Create repositories
        self.repo = NetworkXSFMRepository()
        self.actor_repo = ActorRepository(self.repo)
        self.institution_repo = InstitutionRepository(self.repo)
        self.relationship_repo = RelationshipRepository(self.repo)
        
        # Create test data
        self.actor = Actor(label="Government Actor", sector="Government")
        self.institution = Institution(label="Research Institution")

    def test_cross_repo_operations(self):
        # Create nodes in different repositories
        self.actor_repo.create(self.actor)
        self.institution_repo.create(self.institution)
        
        # Create a relationship between them
        relationship = Relationship(
            source_id=self.actor.id,
            target_id=self.institution.id,
            kind=RelationshipKind.FUNDS
        )
        self.relationship_repo.create(relationship)
        
        # Query from relationship repo
        actor_relations = self.relationship_repo.find_by_source(self.actor.id)
        self.assertEqual(len(actor_relations), 1)
        
        # Query from actor repo - should see the relationship through the base repo
        node = self.actor_repo.read(self.actor.id)
        self.assertIsNotNone(node)

    def test_graph_save_load(self):
        # Create complex data structure
        actor1 = Actor(label="Actor 1")
        actor2 = Actor(label="Actor 2")
        institution = Institution(label="Institution")
        
        rel1 = Relationship(
            source_id=actor1.id,
            target_id=actor2.id,
            kind=RelationshipKind.GOVERNS
        )
        rel2 = Relationship(
            source_id=actor1.id,
            target_id=institution.id,
            kind=RelationshipKind.FUNDS
        )
        
        # Create entities
        self.actor_repo.create(actor1)
        self.actor_repo.create(actor2)
        self.institution_repo.create(institution)
        self.relationship_repo.create(rel1)
        self.relationship_repo.create(rel2)
        
        # Load into SFMGraph
        graph = self.repo.load_graph()
        
        # Verify graph contents
        self.assertEqual(len(graph), 3)  # 3 nodes
        self.assertEqual(len(graph.relationships), 2)  # 2 relationships
        
        # Clear repository
        self.repo.clear()
        self.assertEqual(len(self.actor_repo.list_all()), 0)
        
        # Save graph back
        self.repo.save_graph(graph)
        
        # Verify restored contents
        self.assertEqual(len(self.actor_repo.list_all()), 2)
        self.assertEqual(len(self.institution_repo.list_all()), 1)
        self.assertEqual(len(self.relationship_repo.list_all()), 2)

    def test_type_safety_across_system(self):
        # Create node in actor repo
        actor = Actor(label="Test Actor")
        self.actor_repo.create(actor)
        
        # Try to read as institution - should return None
        found_institution = self.institution_repo.read(actor.id)
        self.assertIsNone(found_institution)
        
        # Trying to update an institution as an actor should fail
        inst = Institution(label="Test Institution")
        with self.assertRaises(TypeError):
            self.actor_repo.update(inst) #type: ignore[expected-type] this is testing a type error


class TestMultipleStorageTypes(unittest.TestCase):
    """
    Tests to validate that different repositories can work together 
    even with different storage backends.
    
    Note: Currently this just tests the same NetworkX backend,
    but the test structure is in place for future storage types.
    """
    
    def setUp(self):
        self.base_repo1 = SFMRepositoryFactory.create_repository("networkx")
        self.base_repo2 = SFMRepositoryFactory.create_repository("networkx")
        
        # Create specialized repositories
        self.actor_repo = ActorRepository(self.base_repo1)
        self.institution_repo = InstitutionRepository(self.base_repo2)

    def test_data_isolation(self):
        # Each repo should have separate storage
        actor = Actor(label="Test Actor")
        institution = Institution(label="Test Institution")
        
        # Add to respective repositories
        self.actor_repo.create(actor)
        self.institution_repo.create(institution)
        
        # Base repo 1 should only have actor
        self.assertEqual(len(self.base_repo1.list_nodes()), 1)
        self.assertEqual(len(self.base_repo1.list_nodes(Actor)), 1)
        self.assertEqual(len(self.base_repo1.list_nodes(Institution)), 0)
        
        # Base repo 2 should only have institution
        self.assertEqual(len(self.base_repo2.list_nodes()), 1)
        self.assertEqual(len(self.base_repo2.list_nodes(Actor)), 0)
        self.assertEqual(len(self.base_repo2.list_nodes(Institution)), 1)


if __name__ == '__main__':
    unittest.main()