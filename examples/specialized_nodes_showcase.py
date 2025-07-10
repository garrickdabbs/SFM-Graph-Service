#!/usr/bin/env python3
"""
Specialized Nodes Showcase Example

This example demonstrates the specialized SFM node types that extend the core framework
with advanced analytical capabilities. It showcases:

- SystemProperty: Emergent system characteristics and metrics
- AnalyticalContext: Framework for organizing analytical perspectives
- FeedbackLoop: System feedback mechanisms with polarity and type
- TechnologySystem: Innovation tracking with Technology Readiness Levels
- PolicyInstrument: Specific tools for policy implementation

The example models a technology innovation ecosystem to show how these specialized
nodes capture complex system dynamics that emerge from interactions between
core entities.
"""

import sys
import os
from pathlib import Path

# Add the workspace root to Python path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

from core.sfm_models import (
    Actor, Institution, Resource, Policy, Flow, Relationship, SFMGraph,
    TechnologySystem, PolicyInstrument, FeedbackLoop, SystemProperty, AnalyticalContext
)
from core.sfm_enums import (
    RelationshipKind, ResourceType, TechnologyReadinessLevel,
    PolicyInstrumentType, FeedbackType, FeedbackPolarity
)
from core.sfm_query import SFMQueryFactory
from db.sfm_dao import NetworkXSFMRepository


def create_innovation_ecosystem_graph(repo: NetworkXSFMRepository, graph: SFMGraph):
    """
    Create an innovation ecosystem demonstrating specialized SFM nodes.
    
    This model shows how specialized nodes capture system-level properties,
    analytical contexts, feedback mechanisms, and technology dynamics that
    emerge from basic actor-institution-resource interactions.
    """
    
    # ===== CORE ENTITIES =====
    # Actors in the innovation ecosystem
    startup = Actor(
        label="CleanTech Startup",
        sector="Technology",
        description="Early-stage clean technology company"
    )
    
    research_univ = Actor(
        label="Research University",
        sector="Education",
        description="Leading research institution in clean technology"
    )
    
    venture_capital = Actor(
        label="Green Venture Capital",
        sector="Finance",
        description="Investment fund focused on clean technology ventures"
    )
    
    government_agency = Actor(
        label="Innovation Development Agency",
        sector="Government",
        description="Government agency promoting technology innovation"
    )
    
    # Supporting institutions
    innovation_lab = Institution(
        label="Clean Technology Innovation Lab",
        description="Collaborative research and development facility"
    )
    
    # Resources
    research_data = Resource(
        label="Clean Technology Research Data",
        rtype=ResourceType.INFORMATION,
        description="Scientific research data on clean technologies"
    )
    
    venture_funding = Resource(
        label="Venture Capital Funding",
        rtype=ResourceType.FINANCIAL,
        description="Investment capital for technology development"
    )
    
    intellectual_property = Resource(
        label="Technology Patents",
        rtype=ResourceType.INFORMATION,
        description="Intellectual property assets and patents"
    )
    
    # ===== SPECIALIZED NODES =====
    
    # Technology Systems with readiness tracking
    ai_energy_system = TechnologySystem(
        label="AI-Optimized Energy Management System",
        description="Artificial intelligence system for optimizing energy consumption in buildings",
        maturity=TechnologyReadinessLevel.DEMONSTRATION,
        compatibility={
            "market_readiness": 0.75,
            "regulatory_compliance": 0.60,
            "scalability": 0.80
        }
    )
    
    blockchain_carbon = TechnologySystem(
        label="Blockchain Carbon Credit Platform",
        description="Distributed ledger platform for transparent carbon credit trading",
        maturity=TechnologyReadinessLevel.PROTOTYPE_DEMONSTRATION,
        compatibility={
            "market_readiness": 0.50,
            "regulatory_compliance": 0.40,
            "scalability": 0.90
        }
    )
    
    # Policy Instruments for innovation support
    tax_incentive = PolicyInstrument(
        label="Clean Technology Tax Credits",
        instrument_type=PolicyInstrumentType.ECONOMIC,
        description="Tax incentives for clean technology development and deployment",
        target_behavior="Increase clean technology investment and adoption",
        effectiveness_measure=0.75
    )
    
    regulatory_sandbox = PolicyInstrument(
        label="Innovation Regulatory Sandbox",
        instrument_type=PolicyInstrumentType.REGULATORY,
        description="Regulatory framework allowing testing of innovative technologies",
        target_behavior="Enable safe testing of disruptive technologies",
        effectiveness_measure=0.65
    )
    
    # System Properties - emergent characteristics
    innovation_velocity = SystemProperty(
        label="Innovation Ecosystem Velocity",
        description="Rate at which new technologies move from research to market deployment",
        value=2.5,
        unit="technologies/year"
    )
    
    knowledge_spillover = SystemProperty(
        label="Knowledge Spillover Effects",
        description="Extent to which research knowledge transfers between organizations",
        value=0.67,
        unit="knowledge_transfer_coefficient"
    )
    
    market_concentration = SystemProperty(
        label="Market Concentration Index",
        description="Degree of concentration in the clean technology market",
        value=0.35,
        unit="herfindahl_index"
    )
    
    # Feedback Loops - system dynamics
    investment_success_loop = FeedbackLoop(
        label="Investment Success Feedback Loop",
        description="Successful investments attract more capital, increasing future success probability",
        polarity=FeedbackPolarity.REINFORCING,
        type=FeedbackType.POSITIVE,
        relationships=[venture_capital.id, startup.id, ai_energy_system.id],
        strength=0.8
    )
    
    knowledge_sharing_loop = FeedbackLoop(
        label="University-Industry Knowledge Loop",
        description="Industry problems inform research, research solutions benefit industry",
        polarity=FeedbackPolarity.REINFORCING,
        type=FeedbackType.POSITIVE,
        relationships=[research_univ.id, startup.id, research_data.id],
        strength=0.7
    )
    
    # Analytical Contexts for different perspectives
    economic_context = AnalyticalContext(
        label="Economic Impact Analysis Context",
        description="Analytical framework focusing on economic outcomes and market dynamics",
        methods_used=["cost-benefit analysis", "market analysis"],
        assumptions={"market_efficiency": "Markets are reasonably efficient", "rational_actors": "Actors make rational decisions"},
        data_sources={"financial_data": "Venture capital databases", "market_data": "Industry reports"}
    )
    
    innovation_context = AnalyticalContext(
        label="Innovation Dynamics Analysis Context",
        description="Analytical framework focusing on technology development and adoption patterns",
        methods_used=["technology lifecycle analysis", "adoption curve modeling"],
        assumptions={"technology_diffusion": "Technology follows diffusion patterns", "learning_effects": "Learning by doing effects exist"},
        data_sources={"patent_data": "Patent databases", "research_data": "Academic publications"}
    )
    
    # ===== ADD ALL NODES =====
    all_nodes = [
        # Core entities
        startup, research_univ, venture_capital, government_agency, innovation_lab,
        research_data, venture_funding, intellectual_property,
        # Specialized nodes
        ai_energy_system, blockchain_carbon,
        tax_incentive, regulatory_sandbox,
        innovation_velocity, knowledge_spillover, market_concentration,
        investment_success_loop, knowledge_sharing_loop,
        economic_context, innovation_context
    ]
    
    for node in all_nodes:
        repo.create_node(node)
        graph.add_node(node)
    
    # ===== CREATE RELATIONSHIPS =====
    relationships = [
        # Core innovation relationships
        Relationship(source_id=research_univ.id, target_id=research_data.id, kind=RelationshipKind.PRODUCES, weight=0.9),
        Relationship(source_id=startup.id, target_id=research_data.id, kind=RelationshipKind.USES, weight=0.8),
        Relationship(source_id=venture_capital.id, target_id=startup.id, kind=RelationshipKind.FUNDS, weight=0.85),
        Relationship(source_id=startup.id, target_id=intellectual_property.id, kind=RelationshipKind.PRODUCES, weight=0.7),
        
        # Technology development relationships
        Relationship(source_id=startup.id, target_id=ai_energy_system.id, kind=RelationshipKind.DEVELOPS, weight=0.9),
        Relationship(source_id=research_univ.id, target_id=blockchain_carbon.id, kind=RelationshipKind.DEVELOPS, weight=0.8),
        Relationship(source_id=innovation_lab.id, target_id=ai_energy_system.id, kind=RelationshipKind.SUPPORTS, weight=0.6),
        
        # Government support relationships
        Relationship(source_id=government_agency.id, target_id=innovation_lab.id, kind=RelationshipKind.FUNDS, weight=0.8),
        Relationship(source_id=government_agency.id, target_id=startup.id, kind=RelationshipKind.SUPPORTS, weight=0.7),
        
        # System property relationships - what drives emergent properties
        Relationship(source_id=startup.id, target_id=innovation_velocity.id, kind=RelationshipKind.AFFECTS, weight=0.8),
        Relationship(source_id=research_univ.id, target_id=knowledge_spillover.id, kind=RelationshipKind.AFFECTS, weight=0.9),
        Relationship(source_id=venture_capital.id, target_id=market_concentration.id, kind=RelationshipKind.AFFECTS, weight=0.6),
        
        # Feedback loop connections
        Relationship(source_id=investment_success_loop.id, target_id=innovation_velocity.id, kind=RelationshipKind.AFFECTS, weight=0.7),
        Relationship(source_id=knowledge_sharing_loop.id, target_id=knowledge_spillover.id, kind=RelationshipKind.AFFECTS, weight=0.8),
        
        # Analytical context relationships - what each context focuses on
        Relationship(source_id=economic_context.id, target_id=market_concentration.id, kind=RelationshipKind.ANALYZES, weight=0.9),
        Relationship(source_id=innovation_context.id, target_id=innovation_velocity.id, kind=RelationshipKind.ANALYZES, weight=0.9),
        Relationship(source_id=innovation_context.id, target_id=ai_energy_system.id, kind=RelationshipKind.ANALYZES, weight=0.8)
    ]
    
    for rel in relationships:
        repo.create_relationship(rel)
        graph.add_relationship(rel)
    
    repo.save_graph(graph)
    return graph


if __name__ == "__main__":
    """
    Specialized Nodes Showcase - Innovation Ecosystem Analysis
    
    This example demonstrates how specialized SFM nodes capture complex
    system dynamics that emerge from basic entity interactions.
    """
    
    # Initialize
    repo = NetworkXSFMRepository()
    graph = SFMGraph(
        name="Innovation Ecosystem - Specialized Nodes Showcase",
        description="Demonstration of specialized SFM node types in technology innovation context"
    )
    repo.save_graph(graph)
    
    print("=" * 80)
    print("SPECIALIZED NODES SHOWCASE - INNOVATION ECOSYSTEM")
    print("=" * 80)
    print()
    print("This example demonstrates specialized SFM node types:")
    print("• TechnologySystem - Innovation tracking with maturity levels")
    print("• PolicyInstrument - Specific policy implementation tools")
    print("• SystemProperty - Emergent system characteristics")
    print("• FeedbackLoop - System feedback mechanisms")
    print("• AnalyticalContext - Different analytical perspectives")
    print()
    
    # Create the graph
    ecosystem_graph = create_innovation_ecosystem_graph(repo, graph)
    
    # ===== ANALYSIS =====
    print("Graph Structure:")
    print(f"  • Total entities: {len(ecosystem_graph)} nodes")
    print(f"  • Technology Systems: {len(ecosystem_graph.technology_systems)}")
    print(f"  • Policy Instruments: {len(ecosystem_graph.policy_instruments)}")
    print(f"  • System Properties: {len(ecosystem_graph.system_properties)}")
    print(f"  • Feedback Loops: {len(ecosystem_graph.feedback_loops)}")
    print(f"  • Analytical Contexts: {len(ecosystem_graph.analytical_contexts)}")
    print(f"  • Relationships: {len(ecosystem_graph.relationships)}")
    print()
    
    try:
        query_engine = SFMQueryFactory.create_query_engine(ecosystem_graph, "networkx")
        
        # Technology Systems Analysis
        print("-" * 60)
        print("TECHNOLOGY SYSTEMS ANALYSIS")
        print("-" * 60)
        print()
        
        print("🔬 Technology Maturity and Compatibility:")
        for tech_id, tech in ecosystem_graph.technology_systems.items():
            maturity = getattr(tech, 'maturity', 'Unknown')
            compatibility = getattr(tech, 'compatibility', {})
            print(f"  • {tech.label}")
            print(f"    └─ Maturity: {maturity}")
            if compatibility:
                avg_compat = sum(compatibility.values()) / len(compatibility)
                print(f"    └─ Average Compatibility: {avg_compat:.2f}")
                for metric, score in compatibility.items():
                    print(f"      • {metric}: {score}")
        print()
        
        # Policy Instruments Analysis
        print("-" * 60)
        print("POLICY INSTRUMENTS ANALYSIS")
        print("-" * 60)
        print()
        
        print("🛠️ Policy Implementation Tools:")
        for instrument_id, instrument in ecosystem_graph.policy_instruments.items():
            instrument_type = getattr(instrument, 'instrument_type', 'Unknown')
            target_behavior = getattr(instrument, 'target_behavior', 'Not specified')
            effectiveness = getattr(instrument, 'effectiveness_measure', 0)
            connections = sum(1 for rel in ecosystem_graph.relationships.values()
                            if rel.source_id == instrument_id or rel.target_id == instrument_id)
            print(f"  • {instrument.label} ({instrument_type})")
            print(f"    └─ Target Behavior: {target_behavior}")
            print(f"    └─ Effectiveness: {effectiveness}")
            print(f"    └─ Network Connections: {connections}")
        print()
        
        # System Properties Analysis
        print("-" * 60)
        print("SYSTEM PROPERTIES ANALYSIS")
        print("-" * 60)
        print()
        
        print("📊 Emergent System Characteristics:")
        for prop_id, prop in ecosystem_graph.system_properties.items():
            value = getattr(prop, 'value', 'N/A')
            unit = getattr(prop, 'unit', '')
            print(f"  • {prop.label}")
            print(f"    └─ Current Value: {value} {unit}")
        print()
        
        # Feedback Loops Analysis
        print("-" * 60)
        print("FEEDBACK LOOPS ANALYSIS")
        print("-" * 60)
        print()
        
        print("🔄 System Feedback Mechanisms:")
        for loop_id, loop in ecosystem_graph.feedback_loops.items():
            loop_type = getattr(loop, 'type', 'Unknown')
            polarity = getattr(loop, 'polarity', 'Unknown')
            strength = getattr(loop, 'strength', 0)
            relationships = getattr(loop, 'relationships', [])
            print(f"  • {loop.label}")
            print(f"    └─ Type: {loop_type}, Polarity: {polarity}")
            print(f"    └─ Strength: {strength}")
            print(f"    └─ Components: {len(relationships)} entities")
        print()
        
        # Analytical Contexts Analysis
        print("-" * 60)
        print("ANALYTICAL CONTEXTS ANALYSIS")
        print("-" * 60)
        print()
        
        print("🔍 Different Analytical Perspectives:")
        for context_id, context in ecosystem_graph.analytical_contexts.items():
            methods = getattr(context, 'methods_used', [])
            assumptions = getattr(context, 'assumptions', {})
            data_sources = getattr(context, 'data_sources', {})
            connections = sum(1 for rel in ecosystem_graph.relationships.values()
                            if rel.source_id == context_id)
            print(f"  • {context.label}")
            print(f"    └─ Methods: {', '.join(methods[:2])}")
            print(f"    └─ Key Assumptions: {len(assumptions)} assumptions")
            print(f"    └─ Data Sources: {len(data_sources)} sources")
            print(f"    └─ Analyzes: {connections} entities")
        print()
        
        # Network Analysis
        print("-" * 60)
        print("NETWORK STRUCTURE ANALYSIS")
        print("-" * 60)
        print()
        
        density = query_engine.get_network_density()
        print(f"📈 Network Density: {density:.3f}")
        
        central_actors = query_engine.get_most_central_nodes(Actor, "betweenness", 3)
        print("\n🎯 Most Central Actors:")
        for node_id, score in central_actors:
            actor = ecosystem_graph.actors.get(node_id)
            if actor:
                print(f"  • {actor.label}: {score:.3f}")
        print()
        
    except Exception as e:
        print(f"Analysis error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 80)
    print("SPECIALIZED NODES SHOWCASE COMPLETE")
    print("=" * 80)
    print()
    print("Key Insights Demonstrated:")
    print("✓ TechnologySystem nodes track innovation maturity and compatibility")
    print("✓ PolicyInstrument nodes model specific implementation mechanisms")
    print("✓ SystemProperty nodes capture emergent system characteristics")
    print("✓ FeedbackLoop nodes identify self-reinforcing/balancing dynamics")
    print("✓ AnalyticalContext nodes organize different analytical perspectives")
    print("✓ Specialized nodes reveal system dynamics invisible at entity level")
    print()
    print("This showcase demonstrates how specialized nodes extend basic SFM")
    print("modeling to capture complex system dynamics and analytical frameworks.")
    
    # Cleanup
    ecosystem_graph.clear()
    repo.clear()
    print("\nGraph and repository cleared.")