"""
Unit tests for the SFM data model classes defined in core/sfm_models.py
"""

import unittest
import uuid
from typing import Optional
from datetime import datetime
from core.sfm_models import (
    ValueCategory, InstitutionLayer, ResourceType, FlowNature, RelationshipKind,
    TimeSlice, SpatialUnit, Scenario,
    Node, Actor, Institution, Resource, Process, Flow, Relationship, SFMGraph,
    # New classes
    BeliefSystem, Policy, TechnologySystem, Indicator, FeedbackLoop,
    AnalyticalContext, SystemProperty
)


class TestEnums(unittest.TestCase):
    """Test suite for the enumeration types in sfm_models.py"""

    def test_value_category_enum(self):
        """Test ValueCategory enum values."""
        self.assertTrue(hasattr(ValueCategory, "ECONOMIC"))
        self.assertTrue(hasattr(ValueCategory, "SOCIAL"))
        self.assertTrue(hasattr(ValueCategory, "ENVIRONMENTAL"))
        self.assertTrue(hasattr(ValueCategory, "CULTURAL"))
        self.assertTrue(hasattr(ValueCategory, "INSTITUTIONAL"))
        self.assertTrue(hasattr(ValueCategory, "TECHNOLOGICAL"))
        
        # Ensure enums have unique values
        values = [e.value for e in ValueCategory]
        self.assertEqual(len(values), len(set(values)))

    def test_institution_layer_enum(self):
        """Test InstitutionLayer enum values."""
        self.assertTrue(hasattr(InstitutionLayer, "FORMAL_RULE"))
        self.assertTrue(hasattr(InstitutionLayer, "ORGANIZATION"))
        self.assertTrue(hasattr(InstitutionLayer, "INFORMAL_NORM"))
        
        # Ensure enums have unique values
        values = [e.value for e in InstitutionLayer]
        self.assertEqual(len(values), len(set(values)))

    def test_resource_type_enum(self):
        """Test ResourceType enum values."""
        self.assertTrue(hasattr(ResourceType, "NATURAL"))
        self.assertTrue(hasattr(ResourceType, "PRODUCED"))
        self.assertTrue(hasattr(ResourceType, "HUMAN"))
        self.assertTrue(hasattr(ResourceType, "INFORMATION"))
        
        # Ensure enums have unique values
        values = [e.value for e in ResourceType]
        self.assertEqual(len(values), len(set(values)))

    def test_flow_nature_enum(self):
        """Test FlowNature enum values."""
        self.assertTrue(hasattr(FlowNature, "INPUT"))
        self.assertTrue(hasattr(FlowNature, "OUTPUT"))
        self.assertTrue(hasattr(FlowNature, "TRANSFER"))
        
        # Ensure enums have unique values
        values = [e.value for e in FlowNature]
        self.assertEqual(len(values), len(set(values)))

    def test_relationship_kind_enum(self):
        """Test RelationshipKind enum values."""
        self.assertTrue(hasattr(RelationshipKind, "GOVERNS"))
        self.assertTrue(hasattr(RelationshipKind, "USES"))
        self.assertTrue(hasattr(RelationshipKind, "PRODUCES"))
        self.assertTrue(hasattr(RelationshipKind, "EXCHANGES_WITH"))
        self.assertTrue(hasattr(RelationshipKind, "LOCATED_IN"))
        self.assertTrue(hasattr(RelationshipKind, "OCCURS_DURING"))
        # New relationship kinds
        self.assertTrue(hasattr(RelationshipKind, "ENABLES"))
        self.assertTrue(hasattr(RelationshipKind, "INHIBITS"))
        self.assertTrue(hasattr(RelationshipKind, "PRECEDES"))
        self.assertTrue(hasattr(RelationshipKind, "REINFORCES"))
        self.assertTrue(hasattr(RelationshipKind, "UNDERMINES"))
        self.assertTrue(hasattr(RelationshipKind, "AFFECTS"))
        
        # Ensure enums have unique values
        values = [e.value for e in RelationshipKind]
        self.assertEqual(len(values), len(set(values)))


class TestDimensionalEntities(unittest.TestCase):
    """Test suite for dimensional meta entities in sfm_models.py"""

    def test_time_slice(self):
        """Test TimeSlice initialization and properties."""
        time_slice = TimeSlice(label="FY2025")
        self.assertEqual(time_slice.label, "FY2025")
        
        # Test immutability (frozen)
        with self.assertRaises(AttributeError):
            time_slice.label = "Q1-2026"  # type: ignore , this is a frozen dataclass and should raise an error

    def test_spatial_unit(self):
        """Test SpatialUnit initialization and properties."""
        spatial_unit = SpatialUnit(code="US-WA-SEATTLE", name="Seattle, Washington")
        self.assertEqual(spatial_unit.code, "US-WA-SEATTLE")
        self.assertEqual(spatial_unit.name, "Seattle, Washington")
        
        # Test immutability (frozen)
        with self.assertRaises(AttributeError):
            spatial_unit.code = "US-OR-PORTLAND" # type: ignore , this is a frozen dataclass and should raise an error

    def test_scenario(self):
        """Test Scenario initialization and properties."""
        scenario = Scenario(label="Carbon Tax 2026")
        self.assertEqual(scenario.label, "Carbon Tax 2026")
        
        # Test immutability (frozen)
        with self.assertRaises(AttributeError):
            scenario.label = "Baseline" # type: ignore , this is a frozen dataclass and should raise an error


class TestNodeClasses(unittest.TestCase):
    """Test suite for node classes in sfm_models.py"""

    def test_node_init(self):
        """Test base Node class initialization."""
        # Default initialization with just label
        node = Node(label="Test Node")
        self.assertEqual(node.label, "Test Node")
        self.assertIsNone(node.description)
        self.assertIsInstance(node.id, uuid.UUID)
        self.assertEqual(node.meta, {})
        
        # Full initialization
        test_id = uuid.uuid4()
        node = Node(
            label="Test Node", 
            description="A test node",
            id=test_id,
            meta={"key1": "value1", "key2": "value2"}
        )
        self.assertEqual(node.label, "Test Node")
        self.assertEqual(node.description, "A test node")
        self.assertEqual(node.id, test_id)
        self.assertEqual(node.meta, {"key1": "value1", "key2": "value2"})

    def test_actor_init(self):
        """Test Actor class initialization and inheritance."""
        # Test inheritance
        actor = Actor(label="Test Actor")
        self.assertIsInstance(actor, Node)
        
        # Test Actor-specific properties
        actor = Actor(
            label="EPA", 
            description="Environmental Protection Agency",
            legal_form="Government Agency",
            sector="Public Administration"
        )
        self.assertEqual(actor.label, "EPA")
        self.assertEqual(actor.description, "Environmental Protection Agency")
        self.assertEqual(actor.legal_form, "Government Agency")
        self.assertEqual(actor.sector, "Public Administration")

    def test_institution_init(self):
        """Test Institution class initialization and inheritance."""
        # Test inheritance
        institution = Institution(label="Test Institution",layer=InstitutionLayer.FORMAL_RULE)
        self.assertIsInstance(institution, Node)
        
        # Test default layer
        self.assertEqual(institution.layer, InstitutionLayer.FORMAL_RULE)
        
        # Test Institution-specific properties
        institution = Institution(
            label="Carbon Tax", 
            description="Tax on carbon emissions",
            layer=InstitutionLayer.FORMAL_RULE
        )
        self.assertEqual(institution.label, "Carbon Tax")
        self.assertEqual(institution.description, "Tax on carbon emissions")
        self.assertEqual(institution.layer, InstitutionLayer.FORMAL_RULE)

    def test_resource_init(self):
        """Test Resource class initialization and inheritance."""
        # Test inheritance
        resource = Resource(label="Test Resource")
        self.assertIsInstance(resource, Node)
        
        # Test default type
        self.assertEqual(resource.rtype, ResourceType.NATURAL)
        
        # Test Resource-specific properties
        resource = Resource(
            label="Coal", 
            description="Fossil fuel resource",
            rtype=ResourceType.NATURAL,
            unit="tonnes"
        )
        self.assertEqual(resource.label, "Coal")
        self.assertEqual(resource.description, "Fossil fuel resource")
        self.assertEqual(resource.rtype, ResourceType.NATURAL)
        self.assertEqual(resource.unit, "tonnes")

    def test_process_init(self):
        """Test Process class initialization and inheritance."""
        # Test inheritance
        process = Process(label="Test Process")
        self.assertIsInstance(process, Node)
        
        # Test Process-specific properties
        process = Process(
            label="Steel Production", 
            description="Production of steel from iron ore",
            technology="Blast Furnace",
            responsible_actor_id="steel_mill_1"
        )
        self.assertEqual(process.label, "Steel Production")
        self.assertEqual(process.description, "Production of steel from iron ore")
        self.assertEqual(process.technology, "Blast Furnace")
        self.assertEqual(process.responsible_actor_id, "steel_mill_1")

    def test_flow_init(self):
        """Test Flow class initialization and inheritance."""
        # Test inheritance
        flow = Flow(label="Test Flow")
        self.assertIsInstance(flow, Node)
        
        # Test default nature
        self.assertEqual(flow.nature, FlowNature.TRANSFER)
        
        # Test Flow-specific properties
        time_slice = TimeSlice(label="2025")
        spatial_unit = SpatialUnit(code="US", name="United States")
        scenario = Scenario(label="Baseline")
        
        flow = Flow(
            label="CO2 Emissions", 
            description="Carbon dioxide emissions from coal power plant",
            nature=FlowNature.OUTPUT,
            quantity=1000000.0,
            unit="tonnes",
            time=time_slice,
            space=spatial_unit,
            scenario=scenario
        )
        self.assertEqual(flow.label, "CO2 Emissions")
        self.assertEqual(flow.description, "Carbon dioxide emissions from coal power plant")
        self.assertEqual(flow.nature, FlowNature.OUTPUT)
        self.assertEqual(flow.quantity, 1000000.0)
        self.assertEqual(flow.unit, "tonnes")
        self.assertEqual(flow.time, time_slice)
        self.assertEqual(flow.space, spatial_unit)
        self.assertEqual(flow.scenario, scenario)

    # New class tests
    def test_belief_system_init(self):
        """Test BeliefSystem class initialization and inheritance."""
        # Test inheritance
        belief = BeliefSystem(label="Test Belief System")
        self.assertIsInstance(belief, Node)
        
        # Test BeliefSystem-specific properties
        belief = BeliefSystem(
            label="Economic Growth Paradigm", 
            description="Belief system centered on continuous economic growth",
            strength=0.8,
            domain="Economics"
        )
        self.assertEqual(belief.label, "Economic Growth Paradigm")
        self.assertEqual(belief.description, "Belief system centered on continuous economic growth")
        self.assertEqual(belief.strength, 0.8)
        self.assertEqual(belief.domain, "Economics")

    def test_policy_init(self):
        """Test Policy class initialization and inheritance."""
        # Test inheritance
        policy = Policy(label="Test Policy")
        self.assertIsInstance(policy, Institution)  # Policy extends Institution
        
        # Test Policy-specific properties
        policy = Policy(
            label="Carbon Tax Policy", 
            description="Tax on carbon emissions",
            authority="Environmental Protection Agency",
            enforcement=0.75,
            target_sectors=["Energy", "Transportation"],
            layer=InstitutionLayer.FORMAL_RULE  # Redundant if Policy inherits from Institution
        )
        self.assertEqual(policy.label, "Carbon Tax Policy")
        self.assertEqual(policy.description, "Tax on carbon emissions")
        self.assertEqual(policy.authority, "Environmental Protection Agency")
        self.assertEqual(policy.enforcement, 0.75)
        self.assertEqual(policy.target_sectors, ["Energy", "Transportation"])
        self.assertEqual(policy.layer, InstitutionLayer.FORMAL_RULE)  # Inherited from Institution

    def test_technology_system_init(self):
        """Test TechnologySystem class initialization and inheritance."""
        # Test inheritance
        tech = TechnologySystem(label="Test Technology System")
        self.assertIsInstance(tech, Node)
        
        # Test TechnologySystem-specific properties
        tech = TechnologySystem(
            label="Renewable Energy Grid", 
            description="System of interconnected renewable energy sources",
            maturity=0.6,
            compatibility={"fossil_fuel_grid": 0.3, "battery_storage": 0.9}
        )
        self.assertEqual(tech.label, "Renewable Energy Grid")
        self.assertEqual(tech.description, "System of interconnected renewable energy sources")
        self.assertEqual(tech.maturity, 0.6)
        self.assertEqual(tech.compatibility, {"fossil_fuel_grid": 0.3, "battery_storage": 0.9})

    def test_indicator_init(self):
        """Test Indicator class initialization and inheritance."""
        # Test inheritance
        indicator = Indicator(
            label="Test Indicator",
            value_category=ValueCategory.ECONOMIC,
            measurement_unit="$"
        )
        self.assertIsInstance(indicator, Node)
        
        # Test Indicator-specific properties
        indicator = Indicator(
            label="GDP Growth", 
            description="Annual gross domestic product growth",
            value_category=ValueCategory.ECONOMIC,
            measurement_unit="%",
            current_value=2.5,
            target_value=3.0,
            threshold_values={"recession": 0.0, "boom": 4.0}
        )
        self.assertEqual(indicator.label, "GDP Growth")
        self.assertEqual(indicator.description, "Annual gross domestic product growth")
        self.assertEqual(indicator.value_category, ValueCategory.ECONOMIC)
        self.assertEqual(indicator.measurement_unit, "%")
        self.assertEqual(indicator.current_value, 2.5)
        self.assertEqual(indicator.target_value, 3.0)
        self.assertEqual(indicator.threshold_values, {"recession": 0.0, "boom": 4.0})


class TestFeedbackLoop(unittest.TestCase):
    """Test suite for FeedbackLoop class"""
    
    def test_feedback_loop_init(self):
        """Test FeedbackLoop class initialization."""
        # Create some UUIDs for relationships
        rel_ids = [uuid.uuid4() for _ in range(3)]
        
        # Test inheritance
        loop = FeedbackLoop(label="Test Loop")
        self.assertIsInstance(loop, Node)
        
        # Test FeedbackLoop-specific properties  
        loop = FeedbackLoop(
            label="Economic Growth Loop",
            description="Reinforcing feedback between investment and growth",
            relationships=rel_ids,
            type="reinforcing",
            strength=1.5
        )
        self.assertEqual(loop.label, "Economic Growth Loop")
        self.assertEqual(loop.description, "Reinforcing feedback between investment and growth")
        self.assertEqual(loop.relationships, rel_ids)
        self.assertEqual(loop.type, "reinforcing")
        self.assertEqual(loop.strength, 1.5)


class TestMetadataClasses(unittest.TestCase):
    """Test suite for metadata classes in sfm_models.py"""
    
    def test_analytical_context_init(self):
        """Test AnalyticalContext class initialization."""
        context = AnalyticalContext(label="Climate Analysis")
        self.assertIsInstance(context.id, uuid.UUID)
        
        # Test with parameters
        methods = ["network_analysis", "system_dynamics"]
        assumptions = {"growth_rate": "constant", "technology": "improving"}
        sources = {"economic_data": "World Bank", "emissions_data": "EPA"}
        
        context = AnalyticalContext(
            label="Climate Policy Analysis",
            description="Analysis of climate policy impacts on economy",
            methods_used=methods,
            assumptions=assumptions,
            data_sources=sources,
            validation_approach="historical_data_comparison"
        )
        self.assertEqual(context.label, "Climate Policy Analysis")
        self.assertEqual(context.description, "Analysis of climate policy impacts on economy")
        self.assertEqual(context.methods_used, methods)
        self.assertEqual(context.assumptions, assumptions)
        self.assertEqual(context.data_sources, sources)
        self.assertEqual(context.validation_approach, "historical_data_comparison")
        self.assertIsInstance(context.created_at, datetime)
    
    def test_system_property_init(self):
        """Test SystemProperty class initialization."""
        # Create some UUIDs for nodes and relationships
        node_ids = [uuid.uuid4() for _ in range(3)]
        rel_ids = [uuid.uuid4() for _ in range(2)]
        
        # Test inheritance
        prop = SystemProperty(label="Test Property")
        self.assertIsInstance(prop, Node)
        
        # Test SystemProperty-specific properties
        prop = SystemProperty(
            label="System Resilience",
            description="Overall system resilience to shocks",
            property_type="resilience_measure",
            affected_nodes=node_ids,
            contributing_relationships=rel_ids,
            value=0.72,
            unit="index"
        )
        self.assertEqual(prop.label, "System Resilience")
        self.assertEqual(prop.description, "Overall system resilience to shocks")
        self.assertEqual(prop.property_type, "resilience_measure")
        self.assertEqual(prop.affected_nodes, node_ids)
        self.assertEqual(prop.contributing_relationships, rel_ids)
        self.assertEqual(prop.value, 0.72)
        self.assertEqual(prop.unit, "index")


class TestRelationship(unittest.TestCase):
    """Test suite for Relationship class in sfm_models.py"""

    def test_relationship_init(self):
        """Test Relationship class initialization."""
        source_id = uuid.uuid4()
        target_id = uuid.uuid4()
        
        # Basic initialization
        rel = Relationship(
            source_id=source_id,
            target_id=target_id,
            kind=RelationshipKind.GOVERNS
        )
        self.assertEqual(rel.source_id, source_id)
        self.assertEqual(rel.target_id, target_id)
        self.assertEqual(rel.kind, RelationshipKind.GOVERNS)
        self.assertEqual(rel.weight, 0.0)  # Default value
        self.assertIsNone(rel.time)
        self.assertIsNone(rel.space)
        self.assertIsNone(rel.scenario)
        self.assertEqual(rel.meta, {})
        self.assertIsInstance(rel.id, uuid.UUID)
        
        # Full initialization with new attributes
        time_slice = TimeSlice(label="2025")
        spatial_unit = SpatialUnit(code="US", name="United States")
        scenario = Scenario(label="Carbon Tax")
        rel_id = uuid.uuid4()
        
        rel = Relationship(
            source_id=source_id,
            target_id=target_id,
            kind=RelationshipKind.USES,
            weight=0.75,
            time=time_slice,
            space=spatial_unit,
            scenario=scenario,
            meta={"reliability": "high"},
            id=rel_id,
            certainty=0.85,
            variability=0.2
        )
        self.assertEqual(rel.source_id, source_id)
        self.assertEqual(rel.target_id, target_id)
        self.assertEqual(rel.kind, RelationshipKind.USES)
        self.assertEqual(rel.weight, 0.75)
        self.assertEqual(rel.time, time_slice)
        self.assertEqual(rel.space, spatial_unit)
        self.assertEqual(rel.scenario, scenario)
        self.assertEqual(rel.meta, {"reliability": "high"})
        self.assertEqual(rel.id, rel_id)
        self.assertEqual(rel.certainty, 0.85)
        self.assertEqual(rel.variability, 0.2)


class TestSFMGraph(unittest.TestCase):
    """Test suite for SFMGraph class in sfm_models.py"""

    def setUp(self):
        """Set up test data for SFMGraph tests."""
        self.graph = SFMGraph()
                
        # Create sample nodes
        self.actor = Actor(label="EPA", description="Environmental Protection Agency")
        self.institution = Institution(label="Carbon Tax", layer=InstitutionLayer.FORMAL_RULE)
        self.resource = Resource(label="Atmosphere", rtype=ResourceType.NATURAL)
        self.process = Process(label="Emissions Monitoring")
        self.flow = Flow(label="Carbon Dioxide", nature=FlowNature.OUTPUT)
        self.belief = BeliefSystem(label="Environmental Conservation", strength=0.7)
        self.policy = Policy(
            label="Emissions Reduction Policy", 
            authority="Federal Government",
            target_sectors=["Energy", "Transportation"],
            layer=InstitutionLayer.FORMAL_RULE
        )
        self.tech = TechnologySystem(label="Smart Grid", maturity=0.8)
        self.indicator = Indicator(
            label="CO2 Levels", 
            value_category=ValueCategory.ENVIRONMENTAL,
            measurement_unit="ppm"
        )
        
        # Create relationships
        self.relationship = Relationship(
            source_id=self.actor.id,
            target_id=self.institution.id,
            kind=RelationshipKind.GOVERNS
        )
            
    def test_graph_init(self):
        """Test SFMGraph initialization."""
        graph = SFMGraph()
        self.assertEqual(graph.actors, {})
        self.assertEqual(graph.institutions, {})
        self.assertEqual(graph.resources, {})
        self.assertEqual(graph.processes, {})
        self.assertEqual(graph.flows, {})
        self.assertEqual(graph.relationships, {})
        self.assertEqual(graph.belief_systems, {})
        self.assertEqual(graph.technology_systems, {})
        self.assertEqual(graph.indicators, {})
        self.assertEqual(graph.policies, {})
        self.assertEqual(graph.feedback_loops, {})
        self.assertEqual(graph.system_properties, {})
        self.assertEqual(graph.analytical_contexts, {})

    def test_add_node(self):
        """Test SFMGraph.add_node method."""
        # Add each type of node
        self.graph.add_node(self.actor)
        self.graph.add_node(self.institution)
        self.graph.add_node(self.resource)
        self.graph.add_node(self.process)
        self.graph.add_node(self.flow)
        self.graph.add_node(self.belief)
        self.graph.add_node(self.policy)
        self.graph.add_node(self.tech)
        self.graph.add_node(self.indicator)
                          
        # Verify nodes were added to the correct collections
        self.assertEqual(self.graph.actors.get(self.actor.id), self.actor)
        self.assertEqual(self.graph.institutions.get(self.institution.id), self.institution)
        self.assertEqual(self.graph.resources.get(self.resource.id), self.resource)
        self.assertEqual(self.graph.processes.get(self.process.id), self.process)
        self.assertEqual(self.graph.flows.get(self.flow.id), self.flow)
        self.assertEqual(self.graph.belief_systems.get(self.belief.id), self.belief)
        self.assertEqual(self.graph.policies.get(self.policy.id), self.policy)
        self.assertEqual(self.graph.technology_systems.get(self.tech.id), self.tech)
        self.assertEqual(self.graph.indicators.get(self.indicator.id), self.indicator)
        
        # Test adding an unsupported node type
        class UnsupportedNode(Node):
            pass
        
        unsupported_node = UnsupportedNode(label="Unsupported")
        with self.assertRaises(TypeError):
            self.graph.add_node(unsupported_node)

    def test_add_relationship(self):
        """Test SFMGraph.add_relationship method."""
        # Add a relationship
        self.graph.add_relationship(self.relationship)
        
        storedRel = self.graph.relationships.get(self.relationship.id)
        # Verify the relationship exists before checking its properties
        self.assertIsNotNone(storedRel)
        self.assertEqual(storedRel.id, self.relationship.id) # type: ignore     not sure how to fix this
        
        self.assertEqual(len(self.graph.relationships), 1)
    
        # Add another relationship
        relationship2 = Relationship(
            source_id=self.institution.id,
            target_id=self.resource.id,
            kind=RelationshipKind.USES
        )
        
        self.graph.add_relationship(relationship2)
        
        # Verify both relationships are in the graph
        self.assertEqual(len(self.graph.relationships), 2)
        self.assertEqual(self.graph.relationships.get(relationship2.id), relationship2)
    
    def test_add_feedback_loop(self):
        """Test adding a feedback loop to the SFMGraph."""
        # Create feedback loop
        rel_ids = [uuid.uuid4() for _ in range(3)]
        loop = FeedbackLoop(
            label="Economic Growth Loop",
            type="reinforcing",
            relationships=rel_ids
        )
        
        # Add to graph
        self.graph.add_node(loop)
        
        # Verify it was added
        self.assertEqual(self.graph.feedback_loops.get(loop.id), loop)
    
    def test_add_system_property(self):
        """Test adding a system property to the SFMGraph."""
        # Create system property
        node_ids = [uuid.uuid4() for _ in range(2)]
        prop = SystemProperty(
            label="System Resilience",
            property_type="resilience_measure",
            affected_nodes=node_ids
        )
        
        # Add to graph
        self.graph.add_node(prop)
        
        # Verify it was added
        self.assertEqual(self.graph.system_properties.get(prop.id), prop)
    
    def test_add_analytical_context(self):
        """Test adding an analytical context to the SFMGraph."""
        # Create analytical context
        context = AnalyticalContext(
            label="Climate Policy Analysis",
            methods_used=["network_analysis"]
        )
        
        # Add to graph
        self.graph.add_node(context)
        
        # Verify it was added
        self.assertEqual(self.graph.analytical_contexts.get(context.id), context)

    def test_node_iterator(self):
        """Test that Node objects can be iterated over."""
        node = Node(label="Test Node", description="A test node", meta={"key": "value"})
        
        # Convert iterator results to dict for easy checking
        node_dict = dict(node)
        
        self.assertIn("label", node_dict)
        self.assertEqual(node_dict["label"], "Test Node")
        self.assertIn("description", node_dict)
        self.assertEqual(node_dict["description"], "A test node")
        self.assertIn("meta", node_dict)
        self.assertEqual(node_dict["meta"], {"key": "value"})


if __name__ == "__main__":
    unittest.main()
