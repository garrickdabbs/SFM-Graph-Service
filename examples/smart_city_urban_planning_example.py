"""
Smart City Urban Planning Social Fabric Matrix Example

This example demonstrates a comprehensive SFM analysis of smart city urban planning initiatives,
showcasing advanced features including:
- Temporal dynamics modeling for policy implementation
- Complex multi-stakeholder relationships
- Technology systems with maturity assessment
- Cognitive frameworks and behavioral patterns
- Advanced network analysis and vulnerability assessment
- Multi-dimensional value system integration

The model represents the social fabric of a smart city initiative involving various actors,
institutions, technology systems, and policy instruments working together to achieve
sustainable urban development goals.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add the workspace root to Python path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

from core.sfm_models import (
    Actor, Institution, Resource, Policy, Flow, Relationship, Indicator, SFMGraph,
    TechnologySystem, CognitiveFramework, BehavioralPattern, TemporalDynamics,
    TimeSlice, ValueSystem, PolicyInstrument, NetworkMetrics, ChangeProcess
)
from core.sfm_enums import (
    RelationshipKind, ResourceType, FlowNature, FlowType, ValueCategory,
    TechnologyReadinessLevel, LegitimacySource, BehaviorPatternType,
    TemporalFunctionType, PolicyInstrumentType, ChangeType, InstitutionLayer
)
from core.sfm_query import SFMQueryFactory
from db.sfm_dao import NetworkXSFMRepository


def create_smart_city_planning_graph(repo: NetworkXSFMRepository, graph: SFMGraph):
    """
    Create a comprehensive smart city urban planning SFM graph.
    
    This example models a complex urban planning scenario involving multiple stakeholders,
    technology systems, policy instruments, and temporal dynamics for sustainable city development.
    """
    
    print("Creating Smart City Urban Planning SFM Graph...")
    
    # ═══════════════════════════════════════════════════════════════════
    # TEMPORAL FRAMEWORK
    # ═══════════════════════════════════════════════════════════════════
    
    # Create time slices for planning phases
    current_phase = TimeSlice(label="2024_Q1_Planning")
    implementation_phase = TimeSlice(label="2025_Q1_Implementation")
    evaluation_phase = TimeSlice(label="2026_Q1_Evaluation")
    
    # Create temporal dynamics for policy rollout
    policy_rollout_dynamics = TemporalDynamics(
        start_time=current_phase,
        end_time=implementation_phase,
        function_type=TemporalFunctionType.LOGISTIC,
        parameters={"growth_rate": 0.3, "capacity": 100.0, "midpoint": 0.5}
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # CORE ACTORS WITH COMPLEX ATTRIBUTES
    # ═══════════════════════════════════════════════════════════════════
    
    # Government actors with power resources
    city_government = Actor(
        label="City Government",
        sector="Government",
        legal_form="Municipal Authority",
        power_resources={
            "political": 0.9,
            "regulatory": 0.95,
            "financial": 0.7,
            "informational": 0.6
        }
    )
    
    planning_department = Actor(
        label="Urban Planning Department",
        sector="Government",
        legal_form="Municipal Department",
        power_resources={
            "regulatory": 0.8,
            "technical": 0.9,
            "informational": 0.85
        }
    )
    
    # Private sector actors
    tech_company = Actor(
        label="Smart Infrastructure Corp",
        sector="Technology",
        legal_form="Corporation",
        power_resources={
            "technological": 0.95,
            "financial": 0.8,
            "informational": 0.9
        }
    )
    
    construction_consortium = Actor(
        label="Green Building Consortium",
        sector="Construction",
        legal_form="Partnership",
        power_resources={
            "economic": 0.7,
            "technical": 0.85
        }
    )
    
    # Civil society actors
    community_groups = Actor(
        label="Neighborhood Associations",
        sector="Civil Society",
        legal_form="Non-profit Coalition",
        power_resources={
            "social": 0.8,
            "political": 0.4
        }
    )
    
    environmental_ngos = Actor(
        label="Environmental NGOs",
        sector="Civil Society",
        legal_form="Non-profit Organizations",
        power_resources={
            "social": 0.7,
            "informational": 0.8,
            "political": 0.5
        }
    )
    
    research_university = Actor(
        label="Metropolitan University",
        sector="Education",
        legal_form="Public University",
        power_resources={
            "informational": 0.95,
            "technical": 0.9,
            "social": 0.6
        }
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # INSTITUTIONS WITH LAYERED STRUCTURE
    # ═══════════════════════════════════════════════════════════════════
    
    zoning_authority = Institution(
        label="Zoning and Land Use Authority",
        layer=InstitutionLayer.FORMAL_RULE,
        legitimacy_basis="Legal authority"
    )
    
    smart_city_initiative = Institution(
        label="Smart City Public-Private Partnership",
        layer=InstitutionLayer.ORGANIZATION,
        legitimacy_basis="Public-private cooperation"
    )
    
    sustainability_culture = Institution(
        label="Community Sustainability Values",
        layer=InstitutionLayer.INFORMAL_NORM,
        legitimacy_basis="Community values"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # TECHNOLOGY SYSTEMS WITH MATURITY LEVELS
    # ═══════════════════════════════════════════════════════════════════
    
    iot_sensor_network = TechnologySystem(
        label="IoT Environmental Sensor Network",
        maturity=TechnologyReadinessLevel.SYSTEM_COMPLETE,
        compatibility={
            "data_platforms": 0.9,
            "legacy_systems": 0.6,
            "smart_grid": 0.8
        }
    )
    
    ai_traffic_system = TechnologySystem(
        label="AI Traffic Management System",
        maturity=TechnologyReadinessLevel.PROTOTYPE_DEMONSTRATION,
        compatibility={
            "existing_infrastructure": 0.7,
            "emergency_services": 0.85,
            "public_transport": 0.9
        }
    )
    
    green_building_tech = TechnologySystem(
        label="Smart Green Building Technology",
        maturity=TechnologyReadinessLevel.ACTUAL_SYSTEM,
        compatibility={
            "energy_grid": 0.95,
            "building_codes": 0.8,
            "resident_systems": 0.7
        }
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # COGNITIVE FRAMEWORKS AND BEHAVIORAL PATTERNS
    # ═══════════════════════════════════════════════════════════════════
    
    # Stakeholder cognitive frameworks
    government_framework = CognitiveFramework(
        label="Public Administration Efficiency Framework",
        framing_effects={
            "cost_benefit": "efficiency_focused",
            "risk_assessment": "conservative",
            "innovation": "evidence_based"
        },
        cognitive_biases=["status_quo_bias", "confirmation_bias"],
        information_filters=["bureaucratic_channels", "formal_reports"],
        learning_capacity=0.7
    )
    
    community_framework = CognitiveFramework(
        label="Community Quality of Life Framework",
        framing_effects={
            "development": "livability_focused",
            "technology": "privacy_concerned",
            "change": "participation_oriented"
        },
        cognitive_biases=["loss_aversion", "availability_heuristic"],
        information_filters=["local_media", "social_networks"],
        learning_capacity=0.6
    )
    
    tech_framework = CognitiveFramework(
        label="Innovation and Scalability Framework",
        framing_effects={
            "problems": "technology_solvable",
            "adoption": "efficiency_driven",
            "success": "metrics_based"
        },
        cognitive_biases=["optimism_bias", "technological_solutionism"],
        information_filters=["industry_reports", "performance_data"],
        learning_capacity=0.9
    )
    
    # Behavioral patterns
    collaborative_behavior = BehavioralPattern(
        label="Multi-stakeholder Collaboration Pattern",
        pattern_type=BehaviorPatternType.STRATEGIC,
        frequency=0.7,
        predictability=0.6,
        context_dependency=["funding_availability", "political_climate", "community_support"]
    )
    
    innovation_resistance = BehavioralPattern(
        label="Technology Adoption Resistance",
        pattern_type=BehaviorPatternType.RESISTANT,
        frequency=0.4,
        predictability=0.8,
        context_dependency=["privacy_concerns", "cost_impacts", "usability_issues"]
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # RESOURCES WITH COMPLEX CLASSIFICATIONS
    # ═══════════════════════════════════════════════════════════════════
    
    # Financial resources
    municipal_budget = Resource(
        label="Municipal Smart City Budget",
        rtype=ResourceType.FINANCIAL,
        unit="USD"
    )
    
    federal_grants = Resource(
        label="Federal Urban Innovation Grants",
        rtype=ResourceType.FINANCIAL,
        unit="USD"
    )
    
    # Knowledge resources
    urban_planning_expertise = Resource(
        label="Urban Planning and Design Expertise",
        rtype=ResourceType.KNOWLEDGE,
        unit="expert-hours"
    )
    
    community_knowledge = Resource(
        label="Local Community Knowledge",
        rtype=ResourceType.SOCIAL_CAPITAL,
        unit="community-insights"
    )
    
    # Infrastructure resources
    existing_infrastructure = Resource(
        label="Legacy Urban Infrastructure",
        rtype=ResourceType.BUILT,
        unit="infrastructure-units"
    )
    
    public_spaces = Resource(
        label="Public Spaces and Land",
        rtype=ResourceType.LAND,
        unit="square-meters"
    )
    
    # Data resources
    citizen_data = Resource(
        label="Citizen Mobility and Usage Data",
        rtype=ResourceType.DATA,
        unit="data-points"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # POLICIES WITH TEMPORAL DYNAMICS
    # ═══════════════════════════════════════════════════════════════════
    
    smart_city_master_plan = Policy(
        label="Comprehensive Smart City Master Plan",
        authority="City Government"
    )
    
    green_building_standards = Policy(
        label="Mandatory Green Building Standards",
        authority="Planning Department"
    )
    
    data_privacy_regulations = Policy(
        label="Smart City Data Privacy Regulations",
        authority="City Government"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # POLICY INSTRUMENTS
    # ═══════════════════════════════════════════════════════════════════
    
    tax_incentives = PolicyInstrument(
        label="Green Technology Tax Incentives",
        instrument_type=PolicyInstrumentType.ECONOMIC,
        target_behavior="technology_adoption",
        effectiveness_measure=0.7
    )
    
    zoning_requirements = PolicyInstrument(
        label="Smart Infrastructure Zoning Requirements",
        instrument_type=PolicyInstrumentType.REGULATORY,
        target_behavior="compliance_behavior",
        effectiveness_measure=0.8
    )
    
    public_participation = PolicyInstrument(
        label="Citizen Engagement Platforms",
        instrument_type=PolicyInstrumentType.INFORMATION,
        target_behavior="civic_participation",
        effectiveness_measure=0.6
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # VALUE SYSTEMS
    # ═══════════════════════════════════════════════════════════════════
    
    sustainability_values = ValueSystem(
        label="Urban Sustainability Value System",
        legitimacy_source=LegitimacySource.LEGAL_RATIONAL,
        cultural_domain="environmental_stewardship"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # FLOWS WITH MULTIPLE NATURES
    # ═══════════════════════════════════════════════════════════════════
    
    funding_flow = Flow(
        label="Smart City Investment Flow",
        nature=FlowNature.FINANCIAL,
        flow_type=FlowType.FINANCIAL,
        temporal_dynamics=TemporalDynamics(
            start_time=current_phase,
            function_type=TemporalFunctionType.EXPONENTIAL,
            parameters={"growth_rate": 0.15}
        )
    )
    
    data_flow = Flow(
        label="Sensor Data Collection Flow",
        nature=FlowNature.INFORMATION,
        flow_type=FlowType.INFORMATION
    )
    
    knowledge_transfer = Flow(
        label="Research to Practice Knowledge Transfer",
        nature=FlowNature.TRANSFER,
        flow_type=FlowType.INFORMATION,
        temporal_dynamics=TemporalDynamics(
            start_time=current_phase,
            function_type=TemporalFunctionType.LOGISTIC,
            parameters={"growth_rate": 0.2, "capacity": 85.0}
        )
    )
    
    service_delivery = Flow(
        label="Enhanced Urban Services Delivery",
        nature=FlowNature.OUTPUT,
        flow_type=FlowType.MATERIAL
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # INDICATORS WITH MULTIPLE VALUE CATEGORIES
    # ═══════════════════════════════════════════════════════════════════
    
    # Environmental indicators
    air_quality_index = Indicator(
        label="Real-time Air Quality Index",
        value_category=ValueCategory.ENVIRONMENTAL,
        measurement_unit="AQI_score",
        current_value=65.0,
        target_value=45.0,
        temporal_dynamics=TemporalDynamics(
            start_time=current_phase,
            function_type=TemporalFunctionType.LINEAR,
            parameters={"rate": -0.5}  # Improving air quality
        )
    )
    
    energy_efficiency = Indicator(
        label="District Energy Efficiency Rating",
        value_category=ValueCategory.ENVIRONMENTAL,
        measurement_unit="efficiency_percentage",
        current_value=72.0,
        target_value=85.0
    )
    
    # Economic indicators
    development_roi = Indicator(
        label="Smart City Investment ROI",
        value_category=ValueCategory.ECONOMIC,
        measurement_unit="percentage",
        current_value=8.5,
        target_value=12.0
    )
    
    # Social indicators
    citizen_satisfaction = Indicator(
        label="Citizen Satisfaction with Smart Services",
        value_category=ValueCategory.SOCIAL,
        measurement_unit="satisfaction_score",
        current_value=6.8,
        target_value=8.0
    )
    
    digital_inclusion = Indicator(
        label="Digital Inclusion Index",
        value_category=ValueCategory.SOCIAL,
        measurement_unit="inclusion_score",
        current_value=67.0,
        target_value=85.0
    )
    
    # Governance indicators
    policy_effectiveness = Indicator(
        label="Policy Implementation Effectiveness",
        value_category=ValueCategory.INSTITUTIONAL,
        measurement_unit="effectiveness_score",
        current_value=72.0,
        target_value=88.0
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # ADD ALL NODES TO REPOSITORY
    # ═══════════════════════════════════════════════════════════════════
    
    nodes = [
        # Actors
        city_government, planning_department, tech_company, construction_consortium,
        community_groups, environmental_ngos, research_university,
        
        # Institutions
        zoning_authority, smart_city_initiative, sustainability_culture,
        
        # Technology Systems
        iot_sensor_network, ai_traffic_system, green_building_tech,
        
        # Cognitive Frameworks
        government_framework, community_framework, tech_framework,
        
        # Behavioral Patterns
        collaborative_behavior, innovation_resistance,
        
        # Resources
        municipal_budget, federal_grants, urban_planning_expertise, community_knowledge,
        existing_infrastructure, public_spaces, citizen_data,
        
        # Policies
        smart_city_master_plan, green_building_standards, data_privacy_regulations,
        
        # Policy Instruments
        tax_incentives, zoning_requirements, public_participation,
        
        # Value Systems
        sustainability_values,
        
        # Flows
        funding_flow, data_flow, knowledge_transfer, service_delivery,
        
        # Indicators
        air_quality_index, energy_efficiency, development_roi, citizen_satisfaction,
        digital_inclusion, policy_effectiveness
    ]
    
    print(f"Adding {len(nodes)} nodes to repository...")
    for node in nodes:
        repo.create_node(node)
        graph.add_node(node)
    
    # ═══════════════════════════════════════════════════════════════════
    # COMPLEX RELATIONSHIPS WITH MULTIPLE DIMENSIONS
    # ═══════════════════════════════════════════════════════════════════
    
    relationships = [
        # Governance relationships
        Relationship(
            source_id=city_government.id,
            target_id=planning_department.id,
            kind=RelationshipKind.GOVERNS,
            weight=0.9,
            meta={"description": "Administrative oversight and resource allocation"}
        ),
        
        Relationship(
            source_id=zoning_authority.id,
            target_id=green_building_standards.id,
            kind=RelationshipKind.ENFORCES,
            weight=0.85,
            meta={"description": "Regulatory enforcement of building standards"}
        ),
        
        # Public-Private Partnership relationships
        Relationship(
            source_id=smart_city_initiative.id,
            target_id=tech_company.id,
            kind=RelationshipKind.COLLABORATES_WITH,
            weight=0.8,
            meta={"description": "Technology implementation partnership"}
        ),
        
        Relationship(
            source_id=smart_city_initiative.id,
            target_id=construction_consortium.id,
            kind=RelationshipKind.COLLABORATES_WITH,
            weight=0.75,
            meta={"description": "Infrastructure development partnership"}
        ),
        
        # Technology integration relationships
        Relationship(
            source_id=tech_company.id,
            target_id=iot_sensor_network.id,
            kind=RelationshipKind.OWNS,
            weight=0.9,
            meta={"description": "Primary technology development and deployment"}
        ),
        
        Relationship(
            source_id=tech_company.id,
            target_id=ai_traffic_system.id,
            kind=RelationshipKind.OWNS,
            weight=0.85,
            meta={"description": "AI system development and integration"}
        ),
        
        # Knowledge and expertise relationships
        Relationship(
            source_id=research_university.id,
            target_id=urban_planning_expertise.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.9,
            meta={"description": "Research-based planning expertise"}
        ),
        
        Relationship(
            source_id=research_university.id,
            target_id=knowledge_transfer.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.8,
            meta={"description": "Research to practice knowledge transfer"}
        ),
        
        # Community engagement relationships
        Relationship(
            source_id=community_groups.id,
            target_id=community_knowledge.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.85,
            meta={"description": "Local knowledge and community insights"}
        ),
        
        Relationship(
            source_id=public_participation.id,
            target_id=community_groups.id,
            kind=RelationshipKind.INFORMS,
            weight=0.7,
            meta={"description": "Citizen engagement mechanisms"}
        ),
        
        # Resource allocation relationships
        Relationship(
            source_id=municipal_budget.id,
            target_id=funding_flow.id,
            kind=RelationshipKind.FUNDS,
            weight=0.8,
            meta={"description": "Primary funding source"}
        ),
        
        Relationship(
            source_id=federal_grants.id,
            target_id=funding_flow.id,
            kind=RelationshipKind.FUNDS,
            weight=0.6,
            meta={"description": "Additional funding support"}
        ),
        
        # Cognitive framework influences
        Relationship(
            source_id=government_framework.id,
            target_id=planning_department.id,
            kind=RelationshipKind.INFLUENCES,
            weight=0.75,
            meta={"description": "Administrative decision-making framework"}
        ),
        
        Relationship(
            source_id=community_framework.id,
            target_id=community_groups.id,
            kind=RelationshipKind.INFLUENCES,
            weight=0.8,
            meta={"description": "Community perspective and priorities"}
        ),
        
        Relationship(
            source_id=tech_framework.id,
            target_id=tech_company.id,
            kind=RelationshipKind.INFLUENCES,
            weight=0.85,
            meta={"description": "Technology development approach"}
        ),
        
        # Behavioral pattern relationships
        Relationship(
            source_id=collaborative_behavior.id,
            target_id=smart_city_initiative.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.7,
            meta={"description": "Collaborative governance mechanisms"}
        ),
        
        Relationship(
            source_id=innovation_resistance.id,
            target_id=ai_traffic_system.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.5,
            meta={"description": "Technology adoption barriers"}
        ),
        
        # Value system relationships
        Relationship(
            source_id=sustainability_values.id,
            target_id=environmental_ngos.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.9,
            meta={"description": "Environmental advocacy alignment"}
        ),
        
        Relationship(
            source_id=sustainability_values.id,
            target_id=green_building_standards.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.8,
            meta={"description": "Policy motivation and justification"}
        ),
        
        # Data and monitoring relationships
        Relationship(
            source_id=iot_sensor_network.id,
            target_id=data_flow.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.9,
            meta={"description": "Sensor data collection and transmission"}
        ),
        
        Relationship(
            source_id=data_flow.id,
            target_id=air_quality_index.id,
            kind=RelationshipKind.INFORMS,
            weight=0.85,
            meta={"description": "Real-time environmental monitoring"}
        ),
        
        # Service delivery relationships
        Relationship(
            source_id=ai_traffic_system.id,
            target_id=service_delivery.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.8,
            meta={"description": "Enhanced traffic management services"}
        ),
        
        Relationship(
            source_id=green_building_tech.id,
            target_id=energy_efficiency.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.85,
            meta={"description": "Building energy performance enhancement"}
        ),
        
        # Policy implementation relationships
        Relationship(
            source_id=smart_city_master_plan.id,
            target_id=policy_effectiveness.id,
            kind=RelationshipKind.MEASURES,
            weight=0.8,
            meta={"description": "Policy implementation assessment"}
        ),
        
        # Impact relationships on citizen outcomes
        Relationship(
            source_id=service_delivery.id,
            target_id=citizen_satisfaction.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.75,
            meta={"description": "Service quality impact on satisfaction"}
        ),
        
        Relationship(
            source_id=public_participation.id,
            target_id=digital_inclusion.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.7,
            meta={"description": "Digital engagement platform inclusion"}
        )
    ]
    
    print(f"Creating {len(relationships)} relationships...")
    for relationship in relationships:
        repo.create_relationship(relationship)
        graph.add_relationship(relationship)
    
    print(f"Smart City SFM Graph completed with {len(nodes)} nodes and {len(relationships)} relationships.")
    return graph


if __name__ == "__main__":
    # Initialize repository and graph
    repo = NetworkXSFMRepository()
    sfm_graph = SFMGraph()
    repo.save_graph(sfm_graph)
    
    # Create the comprehensive smart city graph
    smart_city_graph = create_smart_city_planning_graph(repo, sfm_graph)
    
    # ═══════════════════════════════════════════════════════════════════
    # COMPREHENSIVE ANALYSIS EXAMPLES
    # ═══════════════════════════════════════════════════════════════════
    
    print(f"\n{'='*60}")
    print("SMART CITY URBAN PLANNING SFM ANALYSIS")
    print(f"{'='*60}")
    
    print(f"\nGraph Structure Summary:")
    print(f"  Total entities: {len(smart_city_graph)} nodes")
    print(f"  Actors: {len(smart_city_graph.actors)}")
    print(f"  Institutions: {len(smart_city_graph.institutions)}")
    print(f"  Resources: {len(smart_city_graph.resources)}")
    print(f"  Policies: {len(smart_city_graph.policies)}")
    print(f"  Flows: {len(smart_city_graph.flows)}")
    print(f"  Indicators: {len(smart_city_graph.indicators)}")
    print(f"  Relationships: {len(smart_city_graph.relationships)}")
    
    try:
        # Create advanced query engine
        query_engine = SFMQueryFactory.create_query_engine(smart_city_graph, "networkx")
        
        print(f"\n{'-'*40}")
        print("NETWORK ANALYSIS")
        print(f"{'-'*40}")
        
        # Analyze most central actors (key stakeholders)
        print("\n🎯 Most Central Actors (Betweenness Centrality):")
        from core.sfm_models import Actor
        central_actors = query_engine.get_most_central_nodes(Actor, "betweenness", 5)
        for node_id, score in central_actors:
            actor = smart_city_graph.actors.get(node_id)
            if actor:
                print(f"  • {actor.label}: {score:.3f}")
        
        # Network topology analysis
        print(f"\n📊 Network Topology:")
        density = query_engine.get_network_density()
        print(f"  • Network density: {density:.3f}")
        
        # Find structural bridges (critical connectors)
        print(f"\n🌉 Structural Bridges (Critical Connectors):")
        bridges = query_engine.get_structural_holes()
        for bridge_id in bridges[:5]:
            # Find the node in any collection
            bridge_node = None
            for collection in [smart_city_graph.actors, smart_city_graph.institutions, 
                             smart_city_graph.resources, smart_city_graph.policies]:
                if bridge_id in collection:
                    bridge_node = collection[bridge_id]
                    break
            if bridge_node:
                print(f"  • {bridge_node.label}")
        
        print(f"\n{'-'*40}")
        print("POLICY IMPACT ANALYSIS")
        print(f"{'-'*40}")
        
        # Analyze policy impact networks
        print(f"\n📋 Policy Impact Analysis:")
        for policy_id, policy in smart_city_graph.policies.items():
            affected_nodes = query_engine.analyze_policy_impact(policy_id)
            print(f"  • {policy.label}: affects {len(affected_nodes)} nodes")
        
        # Find most influential policy instruments
        print(f"\n🛠️ Policy Instrument Influence:")
        try:
            # Access policy instruments from their dedicated collection
            for instr_id, instr in smart_city_graph.policy_instruments.items():
                # Analyze connections from this policy instrument
                connections = 0
                for rel in smart_city_graph.relationships.values():
                    if rel.source_id == instr_id or rel.target_id == instr_id:
                        connections += 1
                print(f"  • {instr.label}: {connections} direct connections")
                
            if not smart_city_graph.policy_instruments:
                print("  • No policy instruments found")
        except Exception as e:
            print(f"  • Policy instrument analysis: {str(e)}")
        
        print(f"\n{'-'*40}")
        print("FLOW ANALYSIS")
        print(f"{'-'*40}")
        
        # Analyze resource and information flows
        print(f"\n💰 Resource Flow Analysis:")
        for flow_id, flow in smart_city_graph.flows.items():
            flow_connections = 0
            for rel in smart_city_graph.relationships.values():
                if rel.source_id == flow_id or rel.target_id == flow_id:
                    flow_connections += 1
            print(f"  • {flow.label} ({flow.nature.value}): {flow_connections} connections")
        
        print(f"\n{'-'*40}")
        print("STAKEHOLDER ANALYSIS")
        print(f"{'-'*40}")
        
        # Analyze stakeholder power and influence
        print(f"\n⚡ Stakeholder Power Analysis:")
        for actor_id, actor in smart_city_graph.actors.items():
            if hasattr(actor, 'power_resources') and actor.power_resources:
                total_power = sum(actor.power_resources.values())
                avg_power = total_power / len(actor.power_resources)
                print(f"  • {actor.label}: {avg_power:.2f} average power")
        
        print(f"\n{'-'*40}")
        print("VULNERABILITY ASSESSMENT")
        print(f"{'-'*40}")
        
        # Identify critical vulnerabilities
        print(f"\n🔍 System Vulnerability Assessment:")
        try:
            vulnerabilities = query_engine.system_vulnerability_analysis()
            print(f"  • Vulnerability analysis completed")
        except Exception as e:
            print(f"  • Vulnerability assessment: {str(e)}")
        
        print(f"\n{'-'*40}")
        print("TEMPORAL DYNAMICS INSIGHTS")
        print(f"{'-'*40}")
        
        # Analyze nodes with temporal dynamics
        print(f"\n⏰ Temporal Change Analysis:")
        temporal_nodes = 0
        for node_collection in [smart_city_graph.policies, smart_city_graph.flows, smart_city_graph.indicators]:
            for node in node_collection.values():
                if hasattr(node, 'temporal_dynamics') and node.temporal_dynamics:
                    temporal_nodes += 1
                    print(f"  • {node.label}: {node.temporal_dynamics.function_type.value} dynamics")
        
        print(f"\nTotal nodes with temporal dynamics: {temporal_nodes}")
        
        print(f"\n{'-'*40}")
        print("TECHNOLOGY READINESS ASSESSMENT")
        print(f"{'-'*40}")
        
        # Analyze technology systems maturity
        print(f"\n🔬 Technology Maturity Analysis:")
        
        # Access technology systems from their dedicated collection
        for tech_id, tech_system in smart_city_graph.technology_systems.items():
            if hasattr(tech_system, 'maturity') and tech_system.maturity:
                print(f"  • {tech_system.label}: TRL {tech_system.maturity.value}")
                if hasattr(tech_system, 'compatibility') and tech_system.compatibility:
                    avg_compatibility = sum(tech_system.compatibility.values()) / len(tech_system.compatibility)
                    print(f"    └─ Average compatibility: {avg_compatibility:.2f}")
        
        if not smart_city_graph.technology_systems:
            print("  • No technology systems found")
        
    except Exception as e:
        print(f"\nAnalysis error: {e}")
        import traceback
        traceback.print_exc()
    
    # Clean up
    smart_city_graph.clear()
    repo.clear()
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE - Graph cleared")
    print(f"{'='*60}")