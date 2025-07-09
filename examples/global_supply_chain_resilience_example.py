"""
Global Supply Chain Resilience Social Fabric Matrix Example

This example demonstrates advanced SFM analysis for global supply chain resilience,
showcasing complex features including:
- Multi-regional supply chain networks
- Risk assessment and vulnerability analysis
- Dynamic flow analysis with bottleneck identification
- Stakeholder coordination and governance structures
- Technology adoption and digital transformation
- Crisis response and adaptation mechanisms
- Temporal dynamics for disruption and recovery patterns

The model represents the social fabric of a global supply chain system involving
manufacturers, logistics providers, regulatory bodies, and technology platforms
working together to maintain resilient operations.
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
    TimeSlice, ValueSystem, PolicyInstrument, Process, FeedbackLoop
)
from core.sfm_enums import (
    RelationshipKind, ResourceType, FlowNature, FlowType, ValueCategory,
    TechnologyReadinessLevel, LegitimacySource, BehaviorPatternType,
    TemporalFunctionType, PolicyInstrumentType, ChangeType, InstitutionLayer,
    FeedbackPolarity
)
from core.sfm_query import SFMQueryFactory
from db.sfm_dao import NetworkXSFMRepository


def create_supply_chain_resilience_graph(repo: NetworkXSFMRepository, graph: SFMGraph):
    """
    Create a comprehensive global supply chain resilience SFM graph.
    
    Models a complex supply chain ecosystem with multiple tiers, regions,
    and stakeholders working together to maintain operational resilience
    in the face of global disruptions.
    """
    
    print("Creating Global Supply Chain Resilience SFM Graph...")
    
    # ═══════════════════════════════════════════════════════════════════
    # TEMPORAL FRAMEWORK FOR DISRUPTION CYCLES
    # ═══════════════════════════════════════════════════════════════════
    
    pre_disruption = TimeSlice(label="2023_Q4_Pre_Disruption")
    crisis_phase = TimeSlice(label="2024_Q1_Crisis_Phase")
    recovery_phase = TimeSlice(label="2024_Q3_Recovery_Phase")
    resilience_phase = TimeSlice(label="2025_Q1_Enhanced_Resilience")
    
    # Crisis response dynamics
    disruption_dynamics = TemporalDynamics(
        start_time=pre_disruption,
        end_time=crisis_phase,
        function_type=TemporalFunctionType.EXPONENTIAL,
        parameters={"decay_rate": -0.8, "baseline": 100.0}
    )
    
    recovery_dynamics = TemporalDynamics(
        start_time=crisis_phase,
        end_time=recovery_phase,
        function_type=TemporalFunctionType.LOGISTIC,
        parameters={"growth_rate": 0.4, "capacity": 120.0, "midpoint": 0.6}
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # MULTI-TIER SUPPLY CHAIN ACTORS
    # ═══════════════════════════════════════════════════════════════════
    
    # Original Equipment Manufacturers (OEMs)
    automotive_oem = Actor(
        label="Global Automotive OEM",
        sector="Manufacturing",
        legal_form="Multinational Corporation",
        power_resources={
            "economic": 0.9,
            "technological": 0.85,
            "market_influence": 0.95,
            "supply_control": 0.8
        }
    )
    
    electronics_oem = Actor(
        label="Consumer Electronics Manufacturer",
        sector="Technology",
        legal_form="Corporation",
        power_resources={
            "technological": 0.95,
            "economic": 0.85,
            "innovation": 0.9,
            "market_influence": 0.8
        }
    )
    
    # Tier 1 Suppliers
    tier1_supplier_asia = Actor(
        label="Tier 1 Component Supplier (Asia)",
        sector="Manufacturing",
        legal_form="Corporation",
        power_resources={
            "production_capacity": 0.9,
            "cost_efficiency": 0.85,
            "regional_dominance": 0.8
        }
    )
    
    tier1_supplier_europe = Actor(
        label="Tier 1 Component Supplier (Europe)",
        sector="Manufacturing",
        legal_form="Corporation",
        power_resources={
            "quality_standards": 0.9,
            "technological": 0.8,
            "regulatory_compliance": 0.95
        }
    )
    
    # Tier 2 and Raw Material Suppliers
    raw_material_supplier = Actor(
        label="Critical Raw Materials Supplier",
        sector="Mining",
        legal_form="Mining Corporation",
        power_resources={
            "resource_control": 0.95,
            "geographic_monopoly": 0.8,
            "extraction_capacity": 0.85
        }
    )
    
    semiconductor_foundry = Actor(
        label="Semiconductor Foundry",
        sector="Technology",
        legal_form="Corporation",
        power_resources={
            "technological": 0.95,
            "production_capacity": 0.7,
            "market_influence": 0.9
        }
    )
    
    # Logistics and Transportation
    global_logistics = Actor(
        label="Global Logistics Provider",
        sector="Transportation",
        legal_form="Multinational Corporation",
        power_resources={
            "network_reach": 0.9,
            "operational": 0.85,
            "cost_efficiency": 0.8
        }
    )
    
    port_authority = Actor(
        label="Major Port Authority",
        sector="Transportation",
        legal_form="Public Authority",
        power_resources={
            "infrastructure_control": 0.95,
            "regulatory": 0.8,
            "bottleneck_power": 0.9
        }
    )
    
    # Financial and Insurance Sector
    trade_finance_bank = Actor(
        label="Trade Finance Bank",
        sector="Financial Services",
        legal_form="Bank",
        power_resources={
            "financial": 0.9,
            "risk_management": 0.85,
            "global_reach": 0.8
        }
    )
    
    supply_chain_insurer = Actor(
        label="Supply Chain Risk Insurer",
        sector="Insurance",
        legal_form="Insurance Company",
        power_resources={
            "risk_assessment": 0.9,
            "financial": 0.8,
            "market_intelligence": 0.85
        }
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # GOVERNANCE AND REGULATORY INSTITUTIONS
    # ═══════════════════════════════════════════════════════════════════
    
    international_trade_org = Institution(
        label="International Trade Organization",
        layer=InstitutionLayer.FORMAL_RULE,
        legitimacy_basis="Multilateral agreements"
    )
    
    supply_chain_alliance = Institution(
        label="Global Supply Chain Resilience Alliance",
        layer=InstitutionLayer.ORGANIZATION,
        legitimacy_basis="Industry collaboration"
    )
    
    regional_trade_bloc = Institution(
        label="Regional Trade Agreement",
        layer=InstitutionLayer.FORMAL_RULE,
        legitimacy_basis="Regional economic integration"
    )
    
    industry_standards_body = Institution(
        label="Supply Chain Standards Organization",
        layer=InstitutionLayer.ORGANIZATION,
        legitimacy_basis="Technical expertise"
    )
    
    crisis_response_network = Institution(
        label="Crisis Response Coordination Network",
        layer=InstitutionLayer.INFORMAL_NORM,
        legitimacy_basis="Emergency cooperation protocols"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # ADVANCED TECHNOLOGY SYSTEMS
    # ═══════════════════════════════════════════════════════════════════
    
    blockchain_platform = TechnologySystem(
        label="Blockchain Supply Chain Platform",
        maturity=TechnologyReadinessLevel.PROTOTYPE_DEMONSTRATION,
        compatibility={
            "legacy_erp_systems": 0.6,
            "iot_sensors": 0.9,
            "financial_systems": 0.8,
            "regulatory_reporting": 0.7
        }
    )
    
    ai_demand_forecasting = TechnologySystem(
        label="AI Demand Forecasting System",
        maturity=TechnologyReadinessLevel.SYSTEM_COMPLETE,
        compatibility={
            "market_data_feeds": 0.95,
            "inventory_systems": 0.9,
            "production_planning": 0.85,
            "supplier_systems": 0.7
        }
    )
    
    iot_tracking_system = TechnologySystem(
        label="IoT Asset Tracking Network",
        maturity=TechnologyReadinessLevel.ACTUAL_SYSTEM,
        compatibility={
            "transportation_systems": 0.9,
            "warehouse_management": 0.95,
            "customs_systems": 0.7,
            "insurance_platforms": 0.8
        }
    )
    
    digital_twin_platform = TechnologySystem(
        label="Supply Chain Digital Twin Platform",
        maturity=TechnologyReadinessLevel.PROTOTYPE_DEMONSTRATION,
        compatibility={
            "simulation_engines": 0.9,
            "real_time_data": 0.8,
            "decision_support": 0.85,
            "risk_modeling": 0.9
        }
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # COGNITIVE FRAMEWORKS AND BEHAVIORAL PATTERNS
    # ═══════════════════════════════════════════════════════════════════
    
    # Risk management cognitive frameworks
    enterprise_risk_framework = CognitiveFramework(
        label="Enterprise Risk Management Framework",
        framing_effects={
            "uncertainty": "manageable_through_planning",
            "disruption": "opportunity_for_improvement",
            "costs": "investment_in_resilience"
        },
        cognitive_biases=["overconfidence_bias", "planning_fallacy"],
        information_filters=["risk_reports", "supplier_assessments", "market_intelligence"],
        learning_capacity=0.8
    )
    
    operational_efficiency_framework = CognitiveFramework(
        label="Operational Efficiency Framework",
        framing_effects={
            "costs": "optimization_target",
            "quality": "competitive_advantage",
            "speed": "market_responsiveness"
        },
        cognitive_biases=["cost_optimization_bias", "efficiency_tunnel_vision"],
        information_filters=["performance_metrics", "cost_reports", "competitor_analysis"],
        learning_capacity=0.7
    )
    
    sustainability_framework = CognitiveFramework(
        label="Sustainable Supply Chain Framework",
        framing_effects={
            "environment": "stakeholder_responsibility",
            "social_impact": "license_to_operate",
            "long_term": "value_creation"
        },
        cognitive_biases=["green_washing_temptation", "stakeholder_pressure_bias"],
        information_filters=["sustainability_reports", "stakeholder_feedback", "regulatory_updates"],
        learning_capacity=0.75
    )
    
    # Behavioral patterns in crisis and normal operations
    collaborative_response = BehavioralPattern(
        label="Crisis Collaborative Response",
        pattern_type=BehaviorPatternType.ADAPTIVE,
        frequency=0.8,
        predictability=0.6,
        context_dependency=["crisis_severity", "stakeholder_trust", "regulatory_pressure"]
    )
    
    competitive_hoarding = BehavioralPattern(
        label="Competitive Resource Hoarding",
        pattern_type=BehaviorPatternType.STRATEGIC,
        frequency=0.4,
        predictability=0.7,
        context_dependency=["supply_scarcity", "market_competition", "inventory_costs"]
    )
    
    digital_transformation_adoption = BehavioralPattern(
        label="Digital Technology Adoption",
        pattern_type=BehaviorPatternType.ADAPTIVE,
        frequency=0.6,
        predictability=0.5,
        context_dependency=["technology_maturity", "competitive_pressure", "implementation_costs"]
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # CRITICAL RESOURCES AND MATERIALS
    # ═══════════════════════════════════════════════════════════════════
    
    # Physical resources
    rare_earth_materials = Resource(
        label="Rare Earth Materials",
        rtype=ResourceType.MINERAL,
        unit="metric-tons"
    )
    
    semiconductor_chips = Resource(
        label="Advanced Semiconductor Chips",
        rtype=ResourceType.PRODUCED,
        unit="units"
    )
    
    manufacturing_capacity = Resource(
        label="Global Manufacturing Capacity",
        rtype=ResourceType.BUILT,
        unit="production-units"
    )
    
    # Financial resources
    working_capital = Resource(
        label="Supply Chain Working Capital",
        rtype=ResourceType.FINANCIAL,
        unit="USD"
    )
    
    trade_credit = Resource(
        label="Trade Credit Facilities",
        rtype=ResourceType.CREDIT,
        unit="USD"
    )
    
    # Knowledge and information
    supply_chain_data = Resource(
        label="Supply Chain Visibility Data",
        rtype=ResourceType.DATA,
        unit="data-records"
    )
    
    market_intelligence = Resource(
        label="Market Intelligence and Forecasts",
        rtype=ResourceType.INFORMATION,
        unit="intelligence-reports"
    )
    
    risk_assessments = Resource(
        label="Risk Assessment Reports",
        rtype=ResourceType.KNOWLEDGE,
        unit="risk-reports"
    )
    
    # Infrastructure resources
    logistics_networks = Resource(
        label="Global Logistics Networks",
        rtype=ResourceType.NETWORK_INFRASTRUCTURE,
        unit="network-capacity"
    )
    
    port_capacity = Resource(
        label="Port and Terminal Capacity",
        rtype=ResourceType.TRANSPORTATION,
        unit="container-throughput"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # POLICIES AND REGULATORY FRAMEWORKS
    # ═══════════════════════════════════════════════════════════════════
    
    supply_chain_transparency = Policy(
        label="Supply Chain Transparency Mandate",
        authority="International Trade Organization"
    )
    
    critical_materials_stockpile = Policy(
        label="Strategic Critical Materials Reserve",
        authority="Regional Trade Bloc"
    )
    
    digital_trade_facilitation = Policy(
        label="Digital Trade Facilitation Framework",
        authority="International Trade Organization"
    )
    
    resilience_standards = Policy(
        label="Supply Chain Resilience Standards",
        authority="Industry Standards Body"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # POLICY INSTRUMENTS FOR RESILIENCE
    # ═══════════════════════════════════════════════════════════════════
    
    diversification_incentives = PolicyInstrument(
        label="Supplier Diversification Incentives",
        instrument_type=PolicyInstrumentType.ECONOMIC,
        target_behavior="geographic_diversification",
        effectiveness_measure=0.7
    )
    
    transparency_requirements = PolicyInstrument(
        label="Supply Chain Reporting Requirements",
        instrument_type=PolicyInstrumentType.REGULATORY,
        target_behavior="transparency_compliance",
        effectiveness_measure=0.8
    )
    
    resilience_certification = PolicyInstrument(
        label="Resilience Certification Program",
        instrument_type=PolicyInstrumentType.VOLUNTARY,
        target_behavior="best_practice_adoption",
        effectiveness_measure=0.6
    )
    
    information_sharing_platform = PolicyInstrument(
        label="Industry Information Sharing Platform",
        instrument_type=PolicyInstrumentType.INFORMATION,
        target_behavior="collaborative_intelligence",
        effectiveness_measure=0.75
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # VALUE SYSTEMS AND CULTURAL FOUNDATIONS
    # ═══════════════════════════════════════════════════════════════════
    
    resilience_value_system = ValueSystem(
        label="Supply Chain Resilience Values",
        legitimacy_source=LegitimacySource.EXPERT,
        cultural_domain="operational_resilience"
    )
    
    efficiency_value_system = ValueSystem(
        label="Operational Efficiency Values",
        legitimacy_source=LegitimacySource.LEGAL_RATIONAL,
        cultural_domain="cost_optimization"
    )
    
    collaboration_values = ValueSystem(
        label="Industry Collaboration Values",
        legitimacy_source=LegitimacySource.DEMOCRATIC,
        cultural_domain="collective_action"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # PROCESS MODELS FOR TRANSFORMATION
    # ═══════════════════════════════════════════════════════════════════
    
    demand_planning_process = Process(
        label="Collaborative Demand Planning Process",
        technology="demand_planning_software"
    )
    
    risk_assessment_process = Process(
        label="Integrated Risk Assessment Process",
        technology="risk_modeling_platform"
    )
    
    supplier_qualification_process = Process(
        label="Supplier Resilience Qualification Process",
        technology="supplier_evaluation_system"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # COMPLEX FLOWS WITH TEMPORAL DYNAMICS
    # ═══════════════════════════════════════════════════════════════════
    
    # Material flows
    component_flow = Flow(
        label="Critical Component Flow",
        nature=FlowNature.TRANSFER,
        flow_type=FlowType.MATERIAL,
        temporal_dynamics=disruption_dynamics
    )
    
    raw_material_flow = Flow(
        label="Raw Material Supply Flow",
        nature=FlowNature.INPUT,
        flow_type=FlowType.MATERIAL,
        temporal_dynamics=recovery_dynamics
    )
    
    # Information flows
    demand_signals = Flow(
        label="Demand Signal Propagation",
        nature=FlowNature.INFORMATION,
        flow_type=FlowType.INFORMATION,
        temporal_dynamics=TemporalDynamics(
            start_time=pre_disruption,
            function_type=TemporalFunctionType.LINEAR,
            parameters={"rate": 0.1}
        )
    )
    
    risk_intelligence = Flow(
        label="Risk Intelligence Sharing",
        nature=FlowNature.INFORMATION,
        flow_type=FlowType.INFORMATION
    )
    
    # Financial flows
    payment_flows = Flow(
        label="Cross-Border Payment Flows",
        nature=FlowNature.FINANCIAL,
        flow_type=FlowType.FINANCIAL,
        temporal_dynamics=disruption_dynamics
    )
    
    insurance_coverage = Flow(
        label="Supply Chain Insurance Coverage",
        nature=FlowNature.FINANCIAL,
        flow_type=FlowType.FINANCIAL
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # FEEDBACK LOOPS FOR SYSTEM ADAPTATION
    # ═══════════════════════════════════════════════════════════════════
    
    resilience_feedback = FeedbackLoop(
        label="Resilience Learning Feedback Loop",
        relationships=[],
        polarity=FeedbackPolarity.REINFORCING,
        strength=0.8
    )
    
    market_response_loop = FeedbackLoop(
        label="Market Response Feedback Loop",
        relationships=[],
        polarity=FeedbackPolarity.BALANCING,
        strength=0.6
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # COMPREHENSIVE INDICATORS ACROSS DIMENSIONS
    # ═══════════════════════════════════════════════════════════════════
    
    # Operational indicators
    supply_chain_velocity = Indicator(
        label="End-to-End Supply Chain Velocity",
        value_category=ValueCategory.PERFORMANCE,
        measurement_unit="days",
        current_value=45.0,
        target_value=35.0,
        temporal_dynamics=recovery_dynamics
    )
    
    inventory_turnover = Indicator(
        label="Inventory Turnover Rate",
        value_category=ValueCategory.ECONOMIC,
        measurement_unit="turns_per_year",
        current_value=8.2,
        target_value=10.0
    )
    
    # Resilience indicators
    supplier_diversity_index = Indicator(
        label="Supplier Geographic Diversity Index",
        value_category=ValueCategory.DIVERSITY,
        measurement_unit="diversity_score",
        current_value=0.65,
        target_value=0.8
    )
    
    disruption_recovery_time = Indicator(
        label="Average Disruption Recovery Time",
        value_category=ValueCategory.RESILIENCE,
        measurement_unit="days",
        current_value=28.0,
        target_value=14.0,
        temporal_dynamics=TemporalDynamics(
            start_time=crisis_phase,
            function_type=TemporalFunctionType.EXPONENTIAL,
            parameters={"decay_rate": 0.3}
        )
    )
    
    # Financial indicators
    supply_chain_costs = Indicator(
        label="Total Supply Chain Costs",
        value_category=ValueCategory.ECONOMIC,
        measurement_unit="percentage_of_revenue",
        current_value=18.5,
        target_value=16.0
    )
    
    working_capital_efficiency = Indicator(
        label="Working Capital Efficiency",
        value_category=ValueCategory.ECONOMIC,
        measurement_unit="cash_conversion_days",
        current_value=42.0,
        target_value=32.0
    )
    
    # Technology and innovation indicators
    digital_integration_level = Indicator(
        label="Digital Technology Integration Level",
        value_category=ValueCategory.TECHNOLOGICAL,
        measurement_unit="integration_percentage",
        current_value=45.0,
        target_value=75.0
    )
    
    automation_coverage = Indicator(
        label="Process Automation Coverage",
        value_category=ValueCategory.TECHNOLOGICAL,
        measurement_unit="percentage",
        current_value=35.0,
        target_value=60.0
    )
    
    # Social and governance indicators
    stakeholder_satisfaction = Indicator(
        label="Supply Chain Stakeholder Satisfaction",
        value_category=ValueCategory.SOCIAL,
        measurement_unit="satisfaction_score",
        current_value=7.2,
        target_value=8.5
    )
    
    transparency_compliance = Indicator(
        label="Supply Chain Transparency Compliance",
        value_category=ValueCategory.INSTITUTIONAL,
        measurement_unit="compliance_percentage",
        current_value=68.0,
        target_value=90.0
    )
    
    # Environmental indicators  
    carbon_footprint = Indicator(
        label="Supply Chain Carbon Footprint",
        value_category=ValueCategory.ENVIRONMENTAL,
        measurement_unit="tonnes_co2_equivalent",
        current_value=125000.0,
        target_value=95000.0
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # ADD ALL NODES TO REPOSITORY AND GRAPH
    # ═══════════════════════════════════════════════════════════════════
    
    nodes = [
        # Actors
        automotive_oem, electronics_oem, tier1_supplier_asia, tier1_supplier_europe,
        raw_material_supplier, semiconductor_foundry, global_logistics, port_authority,
        trade_finance_bank, supply_chain_insurer,
        
        # Institutions
        international_trade_org, supply_chain_alliance, regional_trade_bloc,
        industry_standards_body, crisis_response_network,
        
        # Technology Systems
        blockchain_platform, ai_demand_forecasting, iot_tracking_system, digital_twin_platform,
        
        # Cognitive Frameworks
        enterprise_risk_framework, operational_efficiency_framework, sustainability_framework,
        
        # Behavioral Patterns
        collaborative_response, competitive_hoarding, digital_transformation_adoption,
        
        # Resources
        rare_earth_materials, semiconductor_chips, manufacturing_capacity, working_capital,
        trade_credit, supply_chain_data, market_intelligence, risk_assessments,
        logistics_networks, port_capacity,
        
        # Policies
        supply_chain_transparency, critical_materials_stockpile, digital_trade_facilitation,
        resilience_standards,
        
        # Policy Instruments
        diversification_incentives, transparency_requirements, resilience_certification,
        information_sharing_platform,
        
        # Value Systems
        resilience_value_system, efficiency_value_system, collaboration_values,
        
        # Processes
        demand_planning_process, risk_assessment_process, supplier_qualification_process,
        
        # Flows
        component_flow, raw_material_flow, demand_signals, risk_intelligence,
        payment_flows, insurance_coverage,
        
        # Feedback Loops
        resilience_feedback, market_response_loop,
        
        # Indicators
        supply_chain_velocity, inventory_turnover, supplier_diversity_index,
        disruption_recovery_time, supply_chain_costs, working_capital_efficiency,
        digital_integration_level, automation_coverage, stakeholder_satisfaction,
        transparency_compliance, carbon_footprint
    ]
    
    print(f"Adding {len(nodes)} nodes to repository...")
    for node in nodes:
        repo.create_node(node)
        graph.add_node(node)
    
    # ═══════════════════════════════════════════════════════════════════
    # COMPLEX MULTI-DIMENSIONAL RELATIONSHIPS
    # ═══════════════════════════════════════════════════════════════════
    
    relationships = [
        # Supply chain tier relationships
        Relationship(
            source_id=automotive_oem.id,
            target_id=tier1_supplier_asia.id,
            kind=RelationshipKind.BUYS_FROM,
            weight=0.9,
            meta={"description": "Primary component sourcing relationship"}
        ),
        
        Relationship(
            source_id=electronics_oem.id,
            target_id=tier1_supplier_europe.id,
            kind=RelationshipKind.BUYS_FROM,
            weight=0.85,
            meta={"description": "High-quality component sourcing"}
        ),
        
        Relationship(
            source_id=tier1_supplier_asia.id,
            target_id=semiconductor_foundry.id,
            kind=RelationshipKind.BUYS_FROM,
            weight=0.8,
            meta={"description": "Critical semiconductor supply"}
        ),
        
        Relationship(
            source_id=semiconductor_foundry.id,
            target_id=raw_material_supplier.id,
            kind=RelationshipKind.BUYS_FROM,
            weight=0.9,
            meta={"description": "Rare earth materials for chip production"}
        ),
        
        # Logistics and transportation relationships
        Relationship(
            source_id=global_logistics.id,
            target_id=port_authority.id,
            kind=RelationshipKind.CONTRACTS_WITH,
            weight=0.8,
            meta={"description": "Port services and capacity agreements"}
        ),
        
        Relationship(
            source_id=automotive_oem.id,
            target_id=global_logistics.id,
            kind=RelationshipKind.CONTRACTS_WITH,
            weight=0.85,
            meta={"description": "Global transportation services"}
        ),
        
        # Financial service relationships
        Relationship(
            source_id=trade_finance_bank.id,
            target_id=automotive_oem.id,
            kind=RelationshipKind.FUNDS,
            weight=0.8,
            meta={"description": "Trade financing and working capital"}
        ),
        
        Relationship(
            source_id=supply_chain_insurer.id,
            target_id=tier1_supplier_asia.id,
            kind=RelationshipKind.INSURES,
            weight=0.7,
            meta={"description": "Supply chain risk insurance coverage"}
        ),
        
        # Governance and coordination relationships
        Relationship(
            source_id=supply_chain_alliance.id,
            target_id=automotive_oem.id,
            kind=RelationshipKind.COLLABORATES_WITH,
            weight=0.7,
            meta={"description": "Industry collaboration coordination"}
        ),
        
        Relationship(
            source_id=international_trade_org.id,
            target_id=supply_chain_transparency.id,
            kind=RelationshipKind.ENFORCES,
            weight=0.9,
            meta={"description": "International transparency mandate enforcement"}
        ),
        
        # Technology integration relationships
        Relationship(
            source_id=blockchain_platform.id,
            target_id=supply_chain_data.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.85,
            meta={"description": "Immutable supply chain data generation"}
        ),
        
        Relationship(
            source_id=ai_demand_forecasting.id,
            target_id=demand_signals.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.9,
            meta={"description": "AI-enhanced demand signal generation"}
        ),
        
        Relationship(
            source_id=iot_tracking_system.id,
            target_id=supply_chain_data.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.9,
            meta={"description": "Real-time asset tracking data"}
        ),
        
        # Resource allocation and flow relationships - automotive OEM manages working capital and payment flows
        Relationship(
            source_id=automotive_oem.id,
            target_id=working_capital.id,
            kind=RelationshipKind.USES,
            weight=0.9,
            meta={"description": "Automotive OEM manages working capital"}
        ),
        
        Relationship(
            source_id=automotive_oem.id,
            target_id=payment_flows.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.9,
            meta={"description": "OEM produces payment flows from working capital"}
        ),
        
        Relationship(
            source_id=rare_earth_materials.id,
            target_id=raw_material_flow.id,
            kind=RelationshipKind.TRANSFERS,
            weight=0.85,
            meta={"description": "Critical materials supply flow"}
        ),
        
        # Process transformation relationships
        Relationship(
            source_id=demand_planning_process.id,
            target_id=demand_signals.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.8,
            meta={"description": "Collaborative demand planning output"}
        ),
        
        Relationship(
            source_id=risk_assessment_process.id,
            target_id=risk_assessments.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.9,
            meta={"description": "Integrated risk assessment output"}
        ),
        
        # NOTE: Cognitive framework influences commented out due to validation restrictions
        # CognitiveFramework -> Actor INFLUENCES relationships are not currently supported
        # Relationship(
        #     source_id=enterprise_risk_framework.id,
        #     target_id=automotive_oem.id,
        #     kind=RelationshipKind.INFLUENCES,
        #     weight=0.8,
        #     meta={"description": "Risk management decision framework"}
        # ),
        
        # Relationship(
        #     source_id=operational_efficiency_framework.id,
        #     target_id=tier1_supplier_asia.id,
        #     kind=RelationshipKind.INFLUENCES,
        #     weight=0.85,
        #     meta={"description": "Efficiency optimization mindset"}
        # ),
        
        # Behavioral pattern relationships
        Relationship(
            source_id=collaborative_response.id,
            target_id=supply_chain_alliance.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.8,
            meta={"description": "Crisis collaboration behavior"}
        ),
        
        Relationship(
            source_id=competitive_hoarding.id,
            target_id=semiconductor_chips.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.6,
            meta={"description": "Strategic inventory accumulation"}
        ),
        
        # Value system alignments
        Relationship(
            source_id=resilience_value_system.id,
            target_id=supply_chain_alliance.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.9,
            meta={"description": "Resilience values driving collaboration"}
        ),
        
        Relationship(
            source_id=efficiency_value_system.id,
            target_id=global_logistics.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.8,
            meta={"description": "Efficiency values in logistics optimization"}
        ),
        
        # Policy implementation relationships
        Relationship(
            source_id=diversification_incentives.id,
            target_id=automotive_oem.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.7,
            meta={"description": "Incentivizing supplier diversification"}
        ),
        
        Relationship(
            source_id=transparency_requirements.id,
            target_id=blockchain_platform.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.8,
            meta={"description": "Regulatory transparency driving technology adoption"}
        ),
        
        # Information and intelligence flows
        Relationship(
            source_id=market_intelligence.id,
            target_id=risk_intelligence.id,
            kind=RelationshipKind.INFORMS,
            weight=0.8,
            meta={"description": "Market intelligence informing risk assessment"}
        ),
        
        Relationship(
            source_id=risk_intelligence.id,
            target_id=supply_chain_insurer.id,
            kind=RelationshipKind.INFORMS,
            weight=0.85,
            meta={"description": "Risk intelligence for insurance pricing"}
        ),
        
        # Performance measurement relationships
        Relationship(
            source_id=component_flow.id,
            target_id=supply_chain_velocity.id,
            kind=RelationshipKind.MEASURES,
            weight=0.9,
            meta={"description": "Component flow velocity measurement"}
        ),
        
        Relationship(
            source_id=digital_twin_platform.id,
            target_id=disruption_recovery_time.id,
            kind=RelationshipKind.MEASURES,
            weight=0.8,
            meta={"description": "Digital twin monitoring recovery performance"}
        ),
        
        # Feedback loop relationships
        Relationship(
            source_id=resilience_feedback.id,
            target_id=supplier_diversity_index.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.75,
            meta={"description": "Resilience learning improving diversity"}
        ),
        
        Relationship(
            source_id=market_response_loop.id,
            target_id=inventory_turnover.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.7,
            meta={"description": "Market feedback optimizing inventory"}
        )
    ]
    
    print(f"Creating {len(relationships)} relationships...")
    for relationship in relationships:
        repo.create_relationship(relationship)
        graph.add_relationship(relationship)
    
    print(f"Supply Chain Resilience SFM Graph completed with {len(nodes)} nodes and {len(relationships)} relationships.")
    return graph


if __name__ == "__main__":
    # Initialize repository and graph
    repo = NetworkXSFMRepository()
    sfm_graph = SFMGraph()
    repo.save_graph(sfm_graph)
    
    # Create the comprehensive supply chain resilience graph
    supply_chain_graph = create_supply_chain_resilience_graph(repo, sfm_graph)
    
    # ═══════════════════════════════════════════════════════════════════
    # ADVANCED SUPPLY CHAIN ANALYSIS
    # ═══════════════════════════════════════════════════════════════════
    
    print(f"\n{'='*70}")
    print("GLOBAL SUPPLY CHAIN RESILIENCE SFM ANALYSIS")
    print(f"{'='*70}")
    
    print(f"\nGraph Structure Summary:")
    print(f"  Total entities: {len(supply_chain_graph)} nodes")
    print(f"  Actors: {len(supply_chain_graph.actors)}")
    print(f"  Institutions: {len(supply_chain_graph.institutions)}")
    print(f"  Resources: {len(supply_chain_graph.resources)}")
    print(f"  Policies: {len(supply_chain_graph.policies)}")
    print(f"  Flows: {len(supply_chain_graph.flows)}")
    print(f"  Indicators: {len(supply_chain_graph.indicators)}")
    print(f"  Technology Systems: {len(supply_chain_graph.technology_systems)}")
    print(f"  Policy Instruments: {len(supply_chain_graph.policy_instruments)}")
    print(f"  Processes: {len(supply_chain_graph.processes)}")
    print(f"  Feedback Loops: {len(supply_chain_graph.feedback_loops)}")
    print(f"  Relationships: {len(supply_chain_graph.relationships)}")
    
    try:
        # Create advanced query engine
        query_engine = SFMQueryFactory.create_query_engine(supply_chain_graph, "networkx")
        
        print(f"\n{'-'*50}")
        print("SUPPLY CHAIN NETWORK ANALYSIS")
        print(f"{'-'*50}")
        
        # Analyze most central actors in supply chain
        print("\n🎯 Most Central Supply Chain Actors (Betweenness Centrality):")
        from core.sfm_models import Actor
        central_actors = query_engine.get_most_central_nodes(Actor, "betweenness", 8)
        for node_id, score in central_actors:
            actor = supply_chain_graph.actors.get(node_id)
            if actor:
                print(f"  • {actor.label}: {score:.3f}")
        
        # Network topology analysis
        print(f"\n📊 Supply Chain Network Topology:")
        density = query_engine.get_network_density()
        print(f"  • Network density: {density:.3f}")
        
        # Identify critical bottlenecks and vulnerabilities
        print(f"\n🌉 Critical Supply Chain Bridges:")
        bridges = query_engine.get_structural_holes()
        for bridge_id in bridges[:8]:
            # Find the node in any collection
            bridge_node = None
            for collection in [supply_chain_graph.actors, supply_chain_graph.institutions,
                             supply_chain_graph.resources, supply_chain_graph.policies,
                             supply_chain_graph.technology_systems]:
                if bridge_id in collection:
                    bridge_node = collection[bridge_id]
                    break
            if bridge_node:
                print(f"  • {bridge_node.label}")
        
        print(f"\n{'-'*50}")
        print("FLOW AND BOTTLENECK ANALYSIS")
        print(f"{'-'*50}")
        
        # Analyze resource and material flows
        print(f"\n💰 Critical Flow Analysis:")
        for flow_id, flow in supply_chain_graph.flows.items():
            flow_connections = 0
            for rel in supply_chain_graph.relationships.values():
                if rel.source_id == flow_id or rel.target_id == flow_id:
                    flow_connections += 1
            flow_nature = flow.nature.value if hasattr(flow.nature, 'value') else str(flow.nature)
            print(f"  • {flow.label} ({flow_nature}): {flow_connections} connections")
        
        # Identify bottlenecks by flow type
        print(f"\n🚧 Supply Chain Bottleneck Identification:")
        try:
            material_bottlenecks = query_engine.identify_bottlenecks(FlowNature.TRANSFER)
            print(f"  • Material flow bottlenecks: {len(material_bottlenecks)} identified")
            
            info_bottlenecks = query_engine.identify_bottlenecks(FlowNature.INFORMATION)
            print(f"  • Information flow bottlenecks: {len(info_bottlenecks)} identified")
            
            financial_bottlenecks = query_engine.identify_bottlenecks(FlowNature.FINANCIAL)
            print(f"  • Financial flow bottlenecks: {len(financial_bottlenecks)} identified")
        except Exception as e:
            print(f"  • Bottleneck analysis: {str(e)}")
        
        print(f"\n{'-'*50}")
        print("RESILIENCE AND RISK ANALYSIS")
        print(f"{'-'*50}")
        
        # Analyze system vulnerabilities
        print(f"\n🔍 Supply Chain Vulnerability Assessment:")
        try:
            vulnerabilities = query_engine.system_vulnerability_analysis()
            print(f"  • Comprehensive vulnerability analysis completed")
        except Exception as e:
            print(f"  • Vulnerability assessment: {str(e)}")
        
        # Multi-tier supplier analysis
        print(f"\n🏭 Multi-Tier Supplier Analysis:")
        supplier_tiers = {
            "OEMs": ["Global Automotive OEM", "Consumer Electronics Manufacturer"],
            "Tier 1": ["Tier 1 Component Supplier (Asia)", "Tier 1 Component Supplier (Europe)"],
            "Tier 2+": ["Critical Raw Materials Supplier", "Semiconductor Foundry"]
        }
        
        for tier, suppliers in supplier_tiers.items():
            tier_connections = 0
            for actor_id, actor in supply_chain_graph.actors.items():
                if actor.label in suppliers:
                    connections = 0
                    for rel in supply_chain_graph.relationships.values():
                        if rel.source_id == actor_id or rel.target_id == actor_id:
                            connections += 1
                    tier_connections += connections
            print(f"  • {tier} suppliers: {tier_connections} total connections")
        
        print(f"\n{'-'*50}")
        print("TECHNOLOGY INTEGRATION ANALYSIS")
        print(f"{'-'*50}")
        
        # Analyze technology systems and digital transformation
        print(f"\n🔬 Digital Technology Integration Assessment:")
        for tech_id, tech_system in supply_chain_graph.technology_systems.items():
            if hasattr(tech_system, 'maturity') and tech_system.maturity:
                print(f"  • {tech_system.label}: TRL {tech_system.maturity.value}")
                if hasattr(tech_system, 'compatibility') and tech_system.compatibility:
                    avg_compatibility = sum(tech_system.compatibility.values()) / len(tech_system.compatibility)
                    print(f"    └─ Average compatibility: {avg_compatibility:.2f}")
        
        print(f"\n{'-'*50}")
        print("GOVERNANCE AND COORDINATION ANALYSIS")
        print(f"{'-'*50}")
        
        # Analyze governance structures and policy instruments
        print(f"\n🛠️ Policy Instrument Effectiveness:")
        for instr_id, instr in supply_chain_graph.policy_instruments.items():
            connections = 0
            for rel in supply_chain_graph.relationships.values():
                if rel.source_id == instr_id or rel.target_id == instr_id:
                    connections += 1
            effectiveness = getattr(instr, 'effectiveness_measure', 'N/A')
            print(f"  • {instr.label}: {connections} connections, {effectiveness} effectiveness")
        
        # Institution analysis
        print(f"\n🏛️ Institutional Coordination Analysis:")
        for inst_id, institution in supply_chain_graph.institutions.items():
            connections = 0
            for rel in supply_chain_graph.relationships.values():
                if rel.source_id == inst_id or rel.target_id == inst_id:
                    connections += 1
            layer = getattr(institution, 'layer', 'Unknown')
            layer_name = layer.name if hasattr(layer, 'name') else str(layer)
            print(f"  • {institution.label} ({layer_name}): {connections} connections")
        
        print(f"\n{'-'*50}")
        print("STAKEHOLDER POWER ANALYSIS")
        print(f"{'-'*50}")
        
        # Analyze stakeholder power distribution
        print(f"\n⚡ Supply Chain Stakeholder Power Distribution:")
        power_rankings = []
        for actor_id, actor in supply_chain_graph.actors.items():
            if hasattr(actor, 'power_resources') and actor.power_resources:
                total_power = sum(actor.power_resources.values())
                avg_power = total_power / len(actor.power_resources)
                power_rankings.append((actor.label, avg_power))
        
        power_rankings.sort(key=lambda x: x[1], reverse=True)
        for actor_name, avg_power in power_rankings:
            print(f"  • {actor_name}: {avg_power:.2f} average power")
        
        print(f"\n{'-'*50}")
        print("TEMPORAL DYNAMICS ANALYSIS")
        print(f"{'-'*50}")
        
        # Analyze temporal patterns and crisis response
        print(f"\n⏰ Crisis and Recovery Dynamics:")
        temporal_entities = 0
        disruption_affected = 0
        recovery_patterns = 0
        
        all_collections = [
            supply_chain_graph.flows, supply_chain_graph.indicators,
            supply_chain_graph.policies
        ]
        
        for collection in all_collections:
            for entity in collection.values():
                if hasattr(entity, 'temporal_dynamics') and entity.temporal_dynamics:
                    temporal_entities += 1
                    function_type = entity.temporal_dynamics.function_type
                    function_name = function_type.name if hasattr(function_type, 'name') else str(function_type)
                    print(f"  • {entity.label}: {function_name} dynamics")
                    
                    if "exponential" in function_name.lower():
                        disruption_affected += 1
                    elif "logistic" in function_name.lower():
                        recovery_patterns += 1
        
        print(f"\nTemporal dynamics summary:")
        print(f"  • Total entities with temporal patterns: {temporal_entities}")
        print(f"  • Disruption-affected entities: {disruption_affected}")
        print(f"  • Recovery pattern entities: {recovery_patterns}")
        
        print(f"\n{'-'*50}")
        print("PERFORMANCE INDICATORS SUMMARY")
        print(f"{'-'*50}")
        
        # Categorize and summarize indicators
        print(f"\n📊 Key Performance Indicators by Category:")
        indicator_categories = {
            ValueCategory.PERFORMANCE: [],
            ValueCategory.ECONOMIC: [],
            ValueCategory.TECHNOLOGICAL: [],
            ValueCategory.SOCIAL: [],
            ValueCategory.ENVIRONMENTAL: [],
            ValueCategory.INSTITUTIONAL: [],
            ValueCategory.RESILIENCE: [],
            ValueCategory.DIVERSITY: []
        }
        
        for indicator in supply_chain_graph.indicators.values():
            if hasattr(indicator, 'value_category') and indicator.value_category in indicator_categories:
                current = getattr(indicator, 'current_value', 'N/A')
                target = getattr(indicator, 'target_value', 'N/A')
                indicator_categories[indicator.value_category].append((indicator.label, current, target))
        
        for category, indicators in indicator_categories.items():
            if indicators:
                category_name = category.name if hasattr(category, 'name') else str(category)
                print(f"\n  {category_name.title()} Indicators:")
                for label, current, target in indicators:
                    print(f"    • {label}: {current} → {target}")
        
    except Exception as e:
        print(f"\nAnalysis error: {e}")
        import traceback
        traceback.print_exc()
    
    # Clean up
    supply_chain_graph.clear()
    repo.clear()
    
    print(f"\n{'='*70}")
    print("SUPPLY CHAIN ANALYSIS COMPLETE - Graph cleared")
    print(f"{'='*70}")