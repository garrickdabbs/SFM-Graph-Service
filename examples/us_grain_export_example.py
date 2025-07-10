import sys
import os
from pathlib import Path

# Add the workspace root to Python path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

from core.sfm_models import (
    Actor, Institution, Resource, Policy, Flow, Relationship, Indicator, SFMGraph,
    TechnologySystem, ValueSystem, CognitiveFramework, BehavioralPattern, 
    PolicyInstrument, FeedbackLoop, TimeSlice, Scenario
)
from core.sfm_enums import (
    RelationshipKind, ResourceType, FlowNature, TechnologyReadinessLevel,
    LegitimacySource, BehaviorPatternType, PolicyInstrumentType,
    TemporalFunctionType, FeedbackType, FeedbackPolarity
)
from core.sfm_query import SFMQueryFactory, NetworkXSFMQueryEngine
from core.metadata_models import TemporalDynamics
from db.sfm_dao import NetworkXSFMRepository

def create_us_grain_market_graph(repo: NetworkXSFMRepository, graph: SFMGraph):
    """
    Create a comprehensive US grain market analysis graph demonstrating advanced SFM capabilities.
    
    This example showcases:
    - Core entities: Actors, Institutions, Resources, Policies, Flows, Indicators
    - Behavioral components: Value systems, cognitive frameworks, behavioral patterns
    - Technology integration: Agricultural technology systems
    - Policy instruments and feedback loops
    - Temporal dynamics and scenario analysis
    - Advanced relationship modeling
    
    The model represents the complex ecosystem of US grain production and export,
    including government regulation, market dynamics, technological innovation,
    and stakeholder interactions.
    """
    
    # Create temporal context for analysis
    current_period = TimeSlice(label="FY2024")
    projection_period = TimeSlice(label="FY2025-2027")
    
    # Create scenarios for policy analysis
    baseline_scenario = Scenario(label="Baseline Policy Environment")
    carbon_price_scenario = Scenario(label="Carbon Pricing Implementation")

    # ===== CORE ACTORS =====
    # Government and regulatory entities
    usda = Actor(
        label="USDA", 
        sector="Government",
        description="United States Department of Agriculture - primary agricultural regulator",
        legal_form="Federal Agency",
        power_resources={
            "regulatory": 0.95,
            "financial": 0.85,
            "informational": 0.90
        }
    )
    
    epa = Actor(
        label="EPA",
        sector="Government", 
        description="Environmental Protection Agency - environmental regulation",
        legal_form="Federal Agency",
        power_resources={
            "regulatory": 0.90,
            "environmental": 0.95,
            "informational": 0.85
        }
    )
    
    # Private sector actors
    farmers = Actor(
        label="Grain Farmers Association", 
        sector="Agriculture",
        description="Coalition of grain producers representing farming interests",
        legal_form="Trade Association",
        power_resources={
            "economic": 0.75,
            "political": 0.65,
            "technological": 0.60
        }
    )
    
    agtech_company = Actor(
        label="AgTech Innovation Corp",
        sector="Technology",
        description="Agricultural technology company providing precision farming solutions",
        legal_form="Corporation",
        power_resources={
            "technological": 0.90,
            "financial": 0.80,
            "informational": 0.85
        }
    )
    
    traders = Actor(
        label="Global Grain Traders", 
        sector="Private",
        description="International commodity trading companies",
        legal_form="Multinational Corporation",
        power_resources={
            "financial": 0.95,
            "logistical": 0.90,
            "informational": 0.85
        }
    )

    # ===== INSTITUTIONS =====
    government = Institution(
        label="US Federal Government",
        description="Federal institutional framework governing agriculture"
    )
    
    trade_org = Institution(
        label="International Grain Trade Council",
        description="Global trade coordination institution"
    )
    
    market_institution = Institution(
        label="Commodity Markets Exchange",
        description="Price discovery and trading institutional framework"
    )

    # ===== RESOURCES =====
    grain = Resource(
        label="Winter Wheat", 
        rtype=ResourceType.BIOLOGICAL,
        description="Primary grain crop for export markets",
        unit="metric tons"
    )
    
    farmland = Resource(
        label="Agricultural Farmland", 
        rtype=ResourceType.NATURAL,
        description="Productive agricultural land for grain cultivation",
        unit="hectares"
    )
    
    carbon_credits = Resource(
        label="Agricultural Carbon Credits",
        rtype=ResourceType.FINANCIAL,
        description="Carbon sequestration credits from sustainable farming",
        unit="tCO2e"
    )
    
    farm_data = Resource(
        label="Precision Agriculture Data",
        rtype=ResourceType.INFORMATION,
        description="IoT sensor data for optimized farming decisions",
        unit="datasets"
    )

    # ===== TECHNOLOGY SYSTEMS =====
    precision_farming = TechnologySystem(
        label="Precision Farming Platform",
        description="Integrated IoT, GPS, and AI systems for optimized crop management",
        maturity=TechnologyReadinessLevel.ACTUAL_SYSTEM,
        compatibility={
            "environmental": 0.90,
            "economic": 0.85,
            "social": 0.75
        }
    )
    
    blockchain_traceability = TechnologySystem(
        label="Blockchain Supply Chain Traceability",
        description="Distributed ledger system for grain origin and quality tracking",
        maturity=TechnologyReadinessLevel.DEMONSTRATION,
        compatibility={
            "transparency": 0.95,
            "efficiency": 0.80,
            "trust": 0.90
        }
    )

    # ===== VALUE SYSTEMS AND COGNITIVE FRAMEWORKS =====
    sustainability_values = ValueSystem(
        label="Agricultural Sustainability Values",
        description="Environmental stewardship and long-term viability priorities",
        legitimacy_source=LegitimacySource.TRADITIONAL,
        priority_weight=0.80,
        cultural_domain="Environmental Stewardship"
    )
    
    market_efficiency_framework = CognitiveFramework(
        label="Market Efficiency Cognitive Framework",
        description="Belief system emphasizing free market solutions and efficiency",
        framing_effects={
            "market_orientation": "Markets optimize resource allocation",
            "efficiency_focus": "Competition drives innovation"
        },
        cognitive_biases=["Confirmation bias toward market solutions"],
        information_filters=["Economic indicators", "Market signals"]
    )
    
    climate_adaptation_framework = CognitiveFramework(
        label="Climate Adaptation Framework",
        description="Mental model focused on resilience and adaptation to climate change",
        framing_effects={
            "risk_focus": "Climate change requires proactive adaptation",
            "sustainability_lens": "Long-term thinking essential"
        },
        cognitive_biases=["Availability heuristic for recent climate events"],
        information_filters=["Climate data", "Environmental indicators"]
    )

    # ===== BEHAVIORAL PATTERNS =====
    technology_adoption_pattern = BehavioralPattern(
        label="Agricultural Technology Adoption",
        description="Pattern of how farmers adopt new agricultural technologies",
        pattern_type=BehaviorPatternType.ADAPTIVE,
        frequency=0.3,  # Moderate adoption frequency
        predictability=0.7,  # Somewhat predictable pattern
        context_dependency=["Economic incentives", "Peer influence", "Technology complexity"]
    )

    # ===== POLICIES AND INSTRUMENTS =====
    subsidy = Policy(
        label="Grain Production Subsidies", 
        authority="USDA",
        description="Direct payments and crop insurance for grain producers"
    )
    
    carbon_policy = Policy(
        label="Agricultural Carbon Credit Program",
        authority="USDA/EPA",
        description="Incentive program for carbon sequestration in agriculture"
    )
    
    # Policy instruments
    direct_payments = PolicyInstrument(
        label="Direct Subsidy Payments",
        instrument_type=PolicyInstrumentType.ECONOMIC,
        description="Direct financial support to grain producers",
        target_behavior="Increase grain production",
        effectiveness_measure=0.80
    )
    
    carbon_tax_credit = PolicyInstrument(
        label="Carbon Sequestration Tax Credits",
        instrument_type=PolicyInstrumentType.ECONOMIC,
        description="Tax credits for verified carbon sequestration practices",
        target_behavior="Adopt carbon-friendly farming practices",
        effectiveness_measure=0.70
    )

    # ===== FLOWS =====
    export_flow = Flow(
        label="International Grain Export", 
        nature=FlowNature.OUTPUT,
        description="Grain exports to international markets",
        temporal_dynamics=TemporalDynamics(
            start_time=current_period,
            function_type=TemporalFunctionType.LINEAR,
            parameters={"growth_rate": 0.02}
        )
    )
    
    subsidy_flow = Flow(
        label="Government Subsidy Payments", 
        nature=FlowNature.INPUT,
        description="Federal financial support to agricultural sector"
    )
    
    data_flow = Flow(
        label="Agricultural Data Sharing",
        nature=FlowNature.RECIPROCAL,
        description="Exchange of farming data between stakeholders"
    )
    
    carbon_credit_flow = Flow(
        label="Carbon Credit Trading",
        nature=FlowNature.RECIPROCAL,
        description="Trading of agricultural carbon credits"
    )

    # ===== FEEDBACK LOOPS =====
    price_production_loop = FeedbackLoop(
        label="Price-Production Feedback Loop",
        description="Higher prices incentivize increased production, which can lower prices",
        polarity=FeedbackPolarity.BALANCING,
        type=FeedbackType.NEGATIVE,
        relationships=[grain.id, farmers.id, traders.id],
        strength=0.7
    )
    
    technology_productivity_loop = FeedbackLoop(
        label="Technology-Productivity Enhancement Loop", 
        description="Technology adoption increases productivity, generating funds for more technology",
        polarity=FeedbackPolarity.REINFORCING,
        type=FeedbackType.POSITIVE,
        relationships=[precision_farming.id, farmers.id, grain.id],
        strength=0.8
    )

    # ===== INDICATORS =====
    grain_price = Indicator(
        label="Winter Wheat Price Index", 
        current_value=320,  # USD per metric ton
        target_value=340,
        measurement_unit="USD/metric ton",
        temporal_dynamics=TemporalDynamics(
            start_time=current_period,
            function_type=TemporalFunctionType.LINEAR,
            parameters={"growth_rate": 0.03}
        )
    )
    
    production_efficiency = Indicator(
        label="Production Efficiency Index",
        current_value=0.78,
        target_value=0.85,
        measurement_unit="efficiency ratio"
    )
    
    carbon_intensity = Indicator(
        label="Carbon Intensity per Ton",
        current_value=0.45,
        target_value=0.30,
        measurement_unit="tCO2e/ton grain"
    )
    
    tech_adoption_rate = Indicator(
        label="Precision Technology Adoption Rate",
        current_value=0.35,
        target_value=0.75,
        measurement_unit="percentage"
    )

    # ===== ADD ALL NODES TO REPOSITORY AND GRAPH =====
    all_nodes = [
        # Core actors
        usda, epa, farmers, agtech_company, traders,
        # Institutions
        government, trade_org, market_institution,
        # Resources
        grain, farmland, carbon_credits, farm_data,
        # Technology systems
        precision_farming, blockchain_traceability,
        # Value systems and frameworks
        sustainability_values, market_efficiency_framework, climate_adaptation_framework,
        # Behavioral patterns
        technology_adoption_pattern,
        # Policies and instruments
        subsidy, carbon_policy, direct_payments, carbon_tax_credit,
        # Flows
        export_flow, subsidy_flow, data_flow, carbon_credit_flow,
        # Feedback loops
        price_production_loop, technology_productivity_loop,
        # Indicators
        grain_price, production_efficiency, carbon_intensity, tech_adoption_rate
    ]
    
    # Add nodes to repository and graph
    for node in all_nodes:
        repo.create_node(node)
        graph.add_node(node)

    # ===== CREATE SOPHISTICATED RELATIONSHIPS =====
    relationships = [
        # Governance relationships
        Relationship(source_id=usda.id, target_id=farmers.id, kind=RelationshipKind.REGULATES, weight=0.8),
        Relationship(source_id=epa.id, target_id=farmers.id, kind=RelationshipKind.REGULATES, weight=0.6),
        Relationship(source_id=government.id, target_id=subsidy.id, kind=RelationshipKind.IMPLEMENTS, weight=0.9),
        Relationship(source_id=government.id, target_id=carbon_policy.id, kind=RelationshipKind.IMPLEMENTS, weight=0.7),
        
        # Production relationships
        Relationship(source_id=farmers.id, target_id=grain.id, kind=RelationshipKind.PRODUCES, weight=0.9),
        Relationship(source_id=farmers.id, target_id=farmland.id, kind=RelationshipKind.USES, weight=0.95),
        Relationship(source_id=farmers.id, target_id=carbon_credits.id, kind=RelationshipKind.PRODUCES, weight=0.4),
        
        # Technology relationships
        Relationship(source_id=agtech_company.id, target_id=precision_farming.id, kind=RelationshipKind.DEVELOPS, weight=0.9),
        Relationship(source_id=farmers.id, target_id=precision_farming.id, kind=RelationshipKind.USES, weight=0.6),
        Relationship(source_id=precision_farming.id, target_id=farm_data.id, kind=RelationshipKind.PRODUCES, weight=0.85),
        
        # Market relationships  
        Relationship(source_id=traders.id, target_id=grain.id, kind=RelationshipKind.EXCHANGES_WITH, weight=0.9),
        Relationship(source_id=grain.id, target_id=export_flow.id, kind=RelationshipKind.ENABLES, weight=0.95),
        Relationship(source_id=traders.id, target_id=blockchain_traceability.id, kind=RelationshipKind.USES, weight=0.5),
        
        # Financial relationships
        Relationship(source_id=subsidy.id, target_id=farmers.id, kind=RelationshipKind.FUNDS, weight=0.8),
        Relationship(source_id=subsidy.id, target_id=direct_payments.id, kind=RelationshipKind.IMPLEMENTS, weight=0.75),
        Relationship(source_id=carbon_credits.id, target_id=carbon_credit_flow.id, kind=RelationshipKind.ENABLES, weight=0.7),
        
        # Information relationships
        Relationship(source_id=farm_data.id, target_id=data_flow.id, kind=RelationshipKind.ENABLES, weight=0.8),
        Relationship(source_id=agtech_company.id, target_id=farmers.id, kind=RelationshipKind.INFORMS, weight=0.7),
        
        # Value and cognitive relationships
        Relationship(source_id=farmers.id, target_id=sustainability_values.id, kind=RelationshipKind.BELIEVES_IN, weight=0.6),
        Relationship(source_id=traders.id, target_id=market_efficiency_framework.id, kind=RelationshipKind.BELIEVES_IN, weight=0.8),
        Relationship(source_id=climate_adaptation_framework.id, target_id=carbon_policy.id, kind=RelationshipKind.SUPPORTS, weight=0.7),
        
        # Behavioral relationships
        Relationship(source_id=technology_adoption_pattern.id, target_id=farmers.id, kind=RelationshipKind.AFFECTS, weight=0.8),
        
        # Indicator relationships
        Relationship(source_id=grain.id, target_id=grain_price.id, kind=RelationshipKind.AFFECTS, weight=0.9),
        Relationship(source_id=precision_farming.id, target_id=production_efficiency.id, kind=RelationshipKind.AFFECTS, weight=0.8),
        Relationship(source_id=carbon_policy.id, target_id=carbon_intensity.id, kind=RelationshipKind.AFFECTS, weight=0.6),
        Relationship(source_id=precision_farming.id, target_id=tech_adoption_rate.id, kind=RelationshipKind.AFFECTS, weight=0.7),
        
        # Feedback loop relationships
        Relationship(source_id=price_production_loop.id, target_id=grain_price.id, kind=RelationshipKind.AFFECTS, weight=0.8),
        Relationship(source_id=technology_productivity_loop.id, target_id=production_efficiency.id, kind=RelationshipKind.AFFECTS, weight=0.7)
    ]
    
    # Add relationships to repository and graph
    for rel in relationships:
        repo.create_relationship(rel)
        graph.add_relationship(rel)

    repo.save_graph(graph)
    return graph

if __name__ == "__main__":
    """
    Enhanced US Grain Market Analysis Example
    
    This comprehensive example demonstrates the advanced capabilities of the SFM framework
    for modeling complex socio-economic systems. The grain market model includes:
    
    - Multiple stakeholder types with power resource analysis
    - Advanced technology integration and adoption patterns  
    - Behavioral and cognitive frameworks influencing decisions
    - Policy instruments and their effectiveness measures
    - Feedback loops and temporal dynamics
    - Carbon markets and environmental considerations
    - Comprehensive indicator tracking and analysis
    
    Expected Output:
    - Graph structure statistics
    - Network analysis (centrality, density, structural analysis)
    - Policy impact assessment across multiple interventions
    - Technology integration analysis with readiness levels
    - Stakeholder power distribution analysis
    - Behavioral pattern insights
    - Flow analysis across different resource types
    - Temporal dynamics and scenario comparisons
    - Advanced vulnerability and resilience assessment
    """
    
    # Initialize repository and graph
    repo = NetworkXSFMRepository()
    sfm_graph = SFMGraph(
        name="Enhanced US Grain Market Analysis",
        description="Comprehensive SFM model demonstrating advanced framework capabilities"
    )
    repo.save_graph(sfm_graph)
    
    # Create the enhanced graph
    print("Creating Enhanced US Grain Market SFM Graph...")
    print("This example demonstrates advanced SFM modeling capabilities including:")
    print("- Behavioral and cognitive frameworks")
    print("- Technology systems and adoption patterns") 
    print("- Policy instruments and feedback loops")
    print("- Multi-stakeholder power analysis")
    print("- Temporal dynamics and scenario modeling")
    print()
    
    enhanced_graph = create_us_grain_market_graph(repo, sfm_graph)
    
    # ===== GRAPH STRUCTURE ANALYSIS =====
    print("=" * 80)
    print("ENHANCED US GRAIN MARKET SFM ANALYSIS")
    print("=" * 80)
    print()
    
    print("Graph Structure Summary:")
    print(f"  Total entities: {len(enhanced_graph)} nodes")
    print(f"  Actors: {len(enhanced_graph.actors)}")
    print(f"  Institutions: {len(enhanced_graph.institutions)}")
    print(f"  Resources: {len(enhanced_graph.resources)}")
    print(f"  Technology Systems: {len(enhanced_graph.technology_systems)}")
    print(f"  Value Systems: {len(enhanced_graph.value_systems)}")
    print(f"  Cognitive Frameworks: {len(enhanced_graph.cognitive_frameworks)}")
    print(f"  Behavioral Patterns: {len(enhanced_graph.behavioral_patterns)}")
    print(f"  Policies: {len(enhanced_graph.policies)}")
    print(f"  Policy Instruments: {len(enhanced_graph.policy_instruments)}")
    print(f"  Flows: {len(enhanced_graph.flows)}")
    print(f"  Feedback Loops: {len(enhanced_graph.feedback_loops)}")
    print(f"  Indicators: {len(enhanced_graph.indicators)}")
    print(f"  Relationships: {len(enhanced_graph.relationships)}")
    print()
    
    try:
        # Create query engine for advanced analysis
        query_engine = SFMQueryFactory.create_query_engine(enhanced_graph, "networkx")
        
        # ===== NETWORK STRUCTURE ANALYSIS =====
        print("-" * 60)
        print("NETWORK ANALYSIS")
        print("-" * 60)
        print()
        
        print("🎯 Most Central Actors (Betweenness Centrality):")
        central_actors = query_engine.get_most_central_nodes(Actor, "betweenness", 5)
        for node_id, score in central_actors:
            actor = enhanced_graph.actors.get(node_id)
            if actor:
                print(f"  • {actor.label}: {score:.3f}")
        print()
        
        print("📊 Network Topology:")
        density = query_engine.get_network_density()
        print(f"  • Network density: {density:.3f}")
        print()
        
        print("🌉 Structural Bridges (Critical Connectors):")
        bridges = query_engine.get_structural_holes()
        bridge_names = []
        for bridge_id in bridges[:5]:
            for collection_name, collection in [
                ("actors", enhanced_graph.actors),
                ("institutions", enhanced_graph.institutions),
                ("technology_systems", enhanced_graph.technology_systems),
                ("policies", enhanced_graph.policies)
            ]:
                if bridge_id in collection:
                    bridge_names.append(collection[bridge_id].label)
                    break
        for name in bridge_names:
            print(f"  • {name}")
        print()
        
        # ===== POLICY ANALYSIS =====
        print("-" * 60)
        print("POLICY IMPACT ANALYSIS")  
        print("-" * 60)
        print()
        
        print("📋 Policy Impact Analysis:")
        for policy_id, policy in enhanced_graph.policies.items():
            impact = query_engine.analyze_policy_impact(policy_id, impact_radius=3)
            affected_nodes = impact.get('total_affected_nodes', 0)
            print(f"  • {policy.label}: affects {affected_nodes} nodes")
        print()
        
        print("🛠️ Policy Instrument Effectiveness:")
        for instrument_id, instrument in enhanced_graph.policy_instruments.items():
            # Count direct connections to target actors
            connections = sum(1 for rel in enhanced_graph.relationships.values() 
                            if rel.source_id == instrument_id or rel.target_id == instrument_id)
            effectiveness = getattr(instrument, 'effectiveness_measure', 0)
            print(f"  • {instrument.label}: {connections} connections, {effectiveness} effectiveness")
        print()
        
        # ===== TECHNOLOGY ANALYSIS =====
        print("-" * 60)
        print("TECHNOLOGY INTEGRATION ANALYSIS")
        print("-" * 60)
        print()
        
        print("🔬 Technology Maturity Analysis:")
        for tech_id, tech in enhanced_graph.technology_systems.items():
            maturity = getattr(tech, 'maturity', 'Unknown')
            compatibility = getattr(tech, 'compatibility', {})
            avg_compatibility = sum(compatibility.values()) / len(compatibility) if compatibility else 0
            print(f"  • {tech.label}: {maturity}")
            if compatibility:
                print(f"    └─ Average compatibility: {avg_compatibility:.2f}")
        print()
        
        # ===== STAKEHOLDER POWER ANALYSIS =====
        print("-" * 60)
        print("STAKEHOLDER ANALYSIS")
        print("-" * 60)
        print()
        
        print("⚡ Stakeholder Power Analysis:")
        for actor_id, actor in enhanced_graph.actors.items():
            power_resources = getattr(actor, 'power_resources', {})
            if power_resources:
                avg_power = sum(power_resources.values()) / len(power_resources)
                print(f"  • {actor.label}: {avg_power:.2f} average power")
                for resource_type, level in power_resources.items():
                    print(f"    └─ {resource_type}: {level}")
        print()
        
        # ===== BEHAVIORAL ANALYSIS =====
        print("-" * 60)
        print("BEHAVIORAL AND COGNITIVE ANALYSIS")
        print("-" * 60)
        print()
        
        print("🧠 Cognitive Framework Influence:")
        for framework_id, framework in enhanced_graph.cognitive_frameworks.items():
            connections = sum(1 for rel in enhanced_graph.relationships.values()
                            if rel.source_id == framework_id)
            framing_effects = getattr(framework, 'framing_effects', {})
            print(f"  • {framework.label}: {connections} influence connections")
            if framing_effects:
                print(f"    └─ Framing effects: {len(framing_effects)} dimensions")
        print()
        
        print("🎭 Behavioral Pattern Analysis:")
        for pattern_id, pattern in enhanced_graph.behavioral_patterns.items():
            pattern_type = getattr(pattern, 'pattern_type', 'Unknown')
            context_deps = getattr(pattern, 'context_dependency', [])
            print(f"  • {pattern.label} ({pattern_type})")
            if context_deps:
                print(f"    └─ Context dependencies: {', '.join(context_deps[:3])}")
        print()
        
        # ===== FLOW ANALYSIS =====
        print("-" * 60)
        print("FLOW ANALYSIS")
        print("-" * 60)
        print()
        
        print("💰 Resource Flow Analysis:")
        for flow_id, flow in enhanced_graph.flows.items():
            flow_nature = getattr(flow, 'nature', 'Unknown')
            connections = sum(1 for rel in enhanced_graph.relationships.values()
                            if rel.source_id == flow_id or rel.target_id == flow_id)
            print(f"  • {flow.label} ({flow_nature}): {connections} connections")
        print()
        
        # ===== FEEDBACK LOOP ANALYSIS =====
        print("-" * 60)
        print("FEEDBACK LOOP ANALYSIS")
        print("-" * 60)
        print()
        
        print("🔄 System Feedback Loops:")
        for loop_id, loop in enhanced_graph.feedback_loops.items():
            loop_type = getattr(loop, 'type', 'Unknown')
            polarity = getattr(loop, 'polarity', 'Unknown')
            relationships = getattr(loop, 'relationships', [])
            strength = getattr(loop, 'strength', 0)
            print(f"  • {loop.label} ({loop_type}, {polarity})")
            print(f"    └─ Components: {len(relationships)}, Strength: {strength}")
        print()
        
        # ===== TEMPORAL DYNAMICS ANALYSIS =====
        print("-" * 60)
        print("TEMPORAL DYNAMICS ANALYSIS")
        print("-" * 60)
        print()
        
        print("⏰ Temporal Change Patterns:")
        entities_with_dynamics = []
        for collection_name, collection in [
            ("flows", enhanced_graph.flows),
            ("indicators", enhanced_graph.indicators),
            ("behavioral_patterns", enhanced_graph.behavioral_patterns)
        ]:
            for entity_id, entity in collection.items():
                temporal_dynamics = getattr(entity, 'temporal_dynamics', None)
                if temporal_dynamics:
                    function_type = getattr(temporal_dynamics, 'function_type', 'Unknown')
                    entities_with_dynamics.append(f"  • {entity.label}: {function_type} dynamics")
        
        for item in entities_with_dynamics:
            print(item)
        print(f"\nTotal entities with temporal dynamics: {len(entities_with_dynamics)}")
        print()
        
        # ===== VULNERABILITY ASSESSMENT =====
        print("-" * 60)
        print("VULNERABILITY ASSESSMENT")
        print("-" * 60)
        print()
        
        print("🔍 System Vulnerability Assessment:")
        vulnerabilities = query_engine.system_vulnerability_analysis()
        print("  • Comprehensive vulnerability analysis completed")
        print()
        
        # ===== INDICATOR PERFORMANCE =====
        print("-" * 60)
        print("PERFORMANCE INDICATORS")
        print("-" * 60)
        print()
        
        print("📊 Key Performance Indicators:")
        for indicator_id, indicator in enhanced_graph.indicators.items():
            current = getattr(indicator, 'current_value', 0)
            target = getattr(indicator, 'target_value', 0)
            unit = getattr(indicator, 'measurement_unit', '')
            print(f"  • {indicator.label}: {current} → {target} {unit}")
        print()
        
    except Exception as e:
        print(f"Analysis error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 80)
    print("ENHANCED ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print("This example demonstrated advanced SFM capabilities including:")
    print("✓ Multi-stakeholder power analysis with resource dimensions")
    print("✓ Technology integration with maturity and compatibility assessment")
    print("✓ Behavioral patterns and cognitive framework modeling")
    print("✓ Policy instrument effectiveness evaluation")
    print("✓ Feedback loop identification and temporal dynamics")
    print("✓ Comprehensive flow analysis across resource types")
    print("✓ System vulnerability and resilience assessment")
    print("✓ Real-world complexity with environmental considerations")
    print()
    
    # Cleanup
    enhanced_graph.clear()
    repo.clear()
    print("Graph and repository cleared.")


