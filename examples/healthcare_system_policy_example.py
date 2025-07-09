"""
Healthcare System Policy Analysis Social Fabric Matrix Example

This example demonstrates advanced SFM analysis for healthcare system policy evaluation,
showcasing complex features including:
- Multi-stakeholder healthcare ecosystem modeling
- Cognitive frameworks in healthcare decision-making
- Value systems and ethical considerations in medical practice
- Policy instrument effectiveness in health outcomes
- Information flows and evidence-based decision making
- Quality indicators across clinical, economic, and social dimensions
- Temporal dynamics of healthcare reforms and outcomes
- Behavioral patterns in healthcare adoption and compliance

The model represents the social fabric of a healthcare system involving patients,
providers, payers, regulators, and technology systems working together to improve
health outcomes through coordinated policy interventions.
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
    TimeSlice, ValueSystem, PolicyInstrument, Process
)
from core.sfm_enums import (
    RelationshipKind, ResourceType, FlowNature, FlowType, ValueCategory,
    TechnologyReadinessLevel, LegitimacySource, BehaviorPatternType,
    TemporalFunctionType, PolicyInstrumentType, ChangeType, InstitutionLayer
)
from core.sfm_query import SFMQueryFactory
from db.sfm_dao import NetworkXSFMRepository


def create_healthcare_policy_graph(repo: NetworkXSFMRepository, graph: SFMGraph):
    """
    Create a comprehensive healthcare system policy analysis SFM graph.
    
    Models a complex healthcare ecosystem with multiple stakeholders, policy
    interventions, and outcome measures focusing on improving population health
    through coordinated systemic reforms.
    """
    
    print("Creating Healthcare System Policy Analysis SFM Graph...")
    
    # ═══════════════════════════════════════════════════════════════════
    # TEMPORAL FRAMEWORK FOR POLICY IMPLEMENTATION
    # ═══════════════════════════════════════════════════════════════════
    
    baseline_period = TimeSlice(label="2023_Q4_Baseline")
    implementation_period = TimeSlice(label="2024_Q2_Policy_Implementation")
    adjustment_period = TimeSlice(label="2024_Q4_System_Adjustment")
    outcome_period = TimeSlice(label="2025_Q2_Outcome_Assessment")
    
    # Policy implementation dynamics
    implementation_dynamics = TemporalDynamics(
        start_time=baseline_period,
        end_time=implementation_period,
        function_type=TemporalFunctionType.LOGISTIC,
        parameters={"growth_rate": 0.5, "capacity": 90.0, "midpoint": 0.4}
    )
    
    # Health outcome improvement dynamics
    outcome_dynamics = TemporalDynamics(
        start_time=implementation_period,
        end_time=outcome_period,
        function_type=TemporalFunctionType.LINEAR,
        parameters={"rate": 0.2}
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # HEALTHCARE STAKEHOLDER ECOSYSTEM
    # ═══════════════════════════════════════════════════════════════════
    
    # Primary Care Providers
    primary_care_physicians = Actor(
        label="Primary Care Physicians",
        sector="Healthcare",
        legal_form="Professional Association",
        power_resources={
            "clinical_expertise": 0.9,
            "patient_relationships": 0.85,
            "professional_autonomy": 0.8,
            "evidence_interpretation": 0.85
        }
    )
    
    community_health_centers = Actor(
        label="Community Health Centers",
        sector="Healthcare",
        legal_form="Non-profit Organizations",
        power_resources={
            "community_access": 0.9,
            "population_health": 0.8,
            "cultural_competency": 0.85,
            "cost_effectiveness": 0.75
        }
    )
    
    # Specialized Healthcare Providers
    hospital_systems = Actor(
        label="Regional Hospital Systems",
        sector="Healthcare",
        legal_form="Health Systems",
        power_resources={
            "acute_care_capacity": 0.95,
            "advanced_technology": 0.9,
            "emergency_response": 0.95,
            "economic_influence": 0.85
        }
    )
    
    public_health_agencies = Actor(
        label="Public Health Agencies",
        sector="Government",
        legal_form="Government Agencies",
        power_resources={
            "population_surveillance": 0.9,
            "regulatory_authority": 0.85,
            "policy_coordination": 0.8,
            "prevention_programs": 0.8
        }
    )
    
    # Healthcare Payers and Financers
    insurance_companies = Actor(
        label="Health Insurance Companies",
        sector="Insurance",
        legal_form="Corporations",
        power_resources={
            "financial_resources": 0.95,
            "coverage_decisions": 0.9,
            "provider_negotiations": 0.85,
            "data_analytics": 0.8
        }
    )
    
    government_payers = Actor(
        label="Government Health Programs",
        sector="Government",
        legal_form="Government Programs",
        power_resources={
            "policy_setting": 0.95,
            "coverage_mandates": 0.9,
            "population_coverage": 0.85,
            "quality_standards": 0.8
        }
    )
    
    # Patient and Community Representatives
    patient_advocacy_groups = Actor(
        label="Patient Advocacy Organizations",
        sector="Civil Society",
        legal_form="Non-profit Organizations",
        power_resources={
            "patient_voice": 0.8,
            "advocacy_expertise": 0.75,
            "community_mobilization": 0.7,
            "policy_influence": 0.6
        }
    )
    
    community_organizations = Actor(
        label="Community Health Organizations",
        sector="Civil Society",
        legal_form="Community Organizations",
        power_resources={
            "local_knowledge": 0.85,
            "cultural_competency": 0.9,
            "community_trust": 0.8,
            "social_networks": 0.75
        }
    )
    
    # Technology and Innovation Actors
    health_tech_companies = Actor(
        label="Health Technology Companies",
        sector="Technology",
        legal_form="Technology Companies",
        power_resources={
            "technological_innovation": 0.95,
            "data_capabilities": 0.9,
            "market_disruption": 0.8,
            "investment_capital": 0.85
        }
    )
    
    research_institutions = Actor(
        label="Health Research Institutions",
        sector="Research",
        legal_form="Academic Institutions",
        power_resources={
            "evidence_generation": 0.95,
            "scientific_credibility": 0.9,
            "methodology_expertise": 0.9,
            "knowledge_dissemination": 0.8
        }
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # INSTITUTIONAL FRAMEWORKS IN HEALTHCARE
    # ═══════════════════════════════════════════════════════════════════
    
    healthcare_regulations = Institution(
        label="Federal Healthcare Regulations",
        layer=InstitutionLayer.FORMAL_RULE,
        legitimacy_basis="Federal regulatory authority"
    )
    
    professional_standards = Institution(
        label="Medical Professional Standards",
        layer=InstitutionLayer.ORGANIZATION,
        legitimacy_basis="Professional self-regulation"
    )
    
    quality_improvement = Institution(
        label="Quality Improvement Collaboratives",
        layer=InstitutionLayer.ORGANIZATION,
        legitimacy_basis="Collaborative improvement"
    )
    
    patient_safety_culture = Institution(
        label="Patient Safety Culture",
        layer=InstitutionLayer.INFORMAL_NORM,
        legitimacy_basis="Professional ethical commitment"
    )
    
    value_based_care = Institution(
        label="Value-Based Care Framework",
        layer=InstitutionLayer.ORGANIZATION,
        legitimacy_basis="Outcome-focused incentives"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # ADVANCED HEALTHCARE TECHNOLOGY SYSTEMS
    # ═══════════════════════════════════════════════════════════════════
    
    electronic_health_records = TechnologySystem(
        label="Electronic Health Records System",
        maturity=TechnologyReadinessLevel.ACTUAL_SYSTEM,
        compatibility={
            "clinical_workflows": 0.8,
            "interoperability": 0.6,
            "provider_adoption": 0.85,
            "patient_engagement": 0.7
        }
    )
    
    ai_diagnostic_support = TechnologySystem(
        label="AI-Powered Diagnostic Support",
        maturity=TechnologyReadinessLevel.PROTOTYPE_DEMONSTRATION,
        compatibility={
            "clinical_decision_making": 0.7,
            "physician_workflows": 0.6,
            "diagnostic_accuracy": 0.9,
            "regulatory_compliance": 0.5
        }
    )
    
    telehealth_platform = TechnologySystem(
        label="Comprehensive Telehealth Platform",
        maturity=TechnologyReadinessLevel.SYSTEM_COMPLETE,
        compatibility={
            "remote_care_delivery": 0.9,
            "patient_access": 0.8,
            "provider_workflows": 0.75,
            "payment_systems": 0.7
        }
    )
    
    population_health_analytics = TechnologySystem(
        label="Population Health Analytics Platform",
        maturity=TechnologyReadinessLevel.SYSTEM_COMPLETE,
        compatibility={
            "data_integration": 0.8,
            "predictive_modeling": 0.85,
            "public_health_surveillance": 0.9,
            "policy_support": 0.75
        }
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # COGNITIVE FRAMEWORKS IN HEALTHCARE DECISION-MAKING
    # ═══════════════════════════════════════════════════════════════════
    
    # Clinical decision-making framework
    evidence_based_medicine = CognitiveFramework(
        label="Evidence-Based Medicine Framework",
        framing_effects={
            "treatment_decisions": "evidence_driven",
            "uncertainty": "managed_through_research",
            "outcomes": "measured_and_improved"
        },
        cognitive_biases=["confirmation_bias", "availability_heuristic", "anchoring_bias"],
        information_filters=["peer_reviewed_literature", "clinical_guidelines", "professional_experience"],
        learning_capacity=0.85
    )
    
    # Health economics framework
    cost_effectiveness_framework = CognitiveFramework(
        label="Health Economics Cost-Effectiveness Framework",
        framing_effects={
            "resource_allocation": "efficiency_maximization",
            "interventions": "cost_benefit_evaluation",
            "outcomes": "population_health_gains"
        },
        cognitive_biases=["economic_rationality_assumption", "quantification_bias"],
        information_filters=["economic_evaluations", "budget_constraints", "outcome_metrics"],
        learning_capacity=0.8
    )
    
    # Patient-centered care framework
    patient_centered_framework = CognitiveFramework(
        label="Patient-Centered Care Framework",
        framing_effects={
            "treatment_goals": "patient_preferences_focused",
            "care_quality": "patient_experience_driven",
            "success": "patient_satisfaction_measured"
        },
        cognitive_biases=["empathy_bias", "individual_focus_bias"],
        information_filters=["patient_feedback", "satisfaction_surveys", "care_coordination_metrics"],
        learning_capacity=0.75
    )
    
    # Public health prevention framework
    prevention_framework = CognitiveFramework(
        label="Public Health Prevention Framework",
        framing_effects={
            "health_problems": "preventable_through_intervention",
            "population": "risk_stratified_groups",
            "success": "incidence_reduction"
        },
        cognitive_biases=["prevention_paradox", "population_attribution_bias"],
        information_filters=["epidemiological_data", "surveillance_systems", "intervention_studies"],
        learning_capacity=0.9
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # BEHAVIORAL PATTERNS IN HEALTHCARE
    # ═══════════════════════════════════════════════════════════════════
    
    technology_adoption_behavior = BehavioralPattern(
        label="Healthcare Technology Adoption",
        pattern_type=BehaviorPatternType.ADAPTIVE,
        frequency=0.6,
        predictability=0.5,
        context_dependency=["technology_usability", "workflow_integration", "training_support"]
    )
    
    clinical_guideline_adherence = BehavioralPattern(
        label="Clinical Guideline Adherence",
        pattern_type=BehaviorPatternType.HABITUAL,
        frequency=0.7,
        predictability=0.8,
        context_dependency=["guideline_clarity", "clinical_context", "time_pressure"]
    )
    
    preventive_care_seeking = BehavioralPattern(
        label="Preventive Care Seeking Behavior",
        pattern_type=BehaviorPatternType.STRATEGIC,
        frequency=0.5,
        predictability=0.6,
        context_dependency=["health_literacy", "access_barriers", "insurance_coverage"]
    )
    
    collaborative_care_coordination = BehavioralPattern(
        label="Collaborative Care Coordination",
        pattern_type=BehaviorPatternType.STRATEGIC,
        frequency=0.6,
        predictability=0.7,
        context_dependency=["communication_systems", "shared_incentives", "role_clarity"]
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # CRITICAL HEALTHCARE RESOURCES
    # ═══════════════════════════════════════════════════════════════════
    
    # Human resources
    healthcare_workforce = Resource(
        label="Healthcare Professional Workforce",
        rtype=ResourceType.HUMAN,
        unit="FTE_professionals"
    )
    
    clinical_expertise = Resource(
        label="Clinical Knowledge and Expertise",
        rtype=ResourceType.KNOWLEDGE,
        unit="expertise_years"
    )
    
    # Financial resources
    healthcare_funding = Resource(
        label="Healthcare System Funding",
        rtype=ResourceType.FINANCIAL,
        unit="USD_billions"
    )
    
    research_funding = Resource(
        label="Health Research Funding",
        rtype=ResourceType.FINANCIAL,
        unit="USD_millions"
    )
    
    # Infrastructure and technology
    healthcare_infrastructure = Resource(
        label="Healthcare Infrastructure",
        rtype=ResourceType.BUILT,
        unit="facility_capacity"
    )
    
    health_data = Resource(
        label="Electronic Health Data",
        rtype=ResourceType.DATA,
        unit="patient_records"
    )
    
    # Information and evidence
    clinical_evidence = Resource(
        label="Clinical Research Evidence",
        rtype=ResourceType.KNOWLEDGE,
        unit="research_studies"
    )
    
    health_surveillance_data = Resource(
        label="Public Health Surveillance Data",
        rtype=ResourceType.DATA,
        unit="surveillance_indicators"
    )
    
    # Social and community resources
    community_health_capacity = Resource(
        label="Community Health Capacity",
        rtype=ResourceType.SOCIAL_CAPITAL,
        unit="community_health_workers"
    )
    
    patient_engagement = Resource(
        label="Patient and Family Engagement",
        rtype=ResourceType.SOCIAL_CAPITAL,
        unit="engagement_level"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # HEALTHCARE POLICIES AND REFORMS
    # ═══════════════════════════════════════════════════════════════════
    
    universal_coverage_expansion = Policy(
        label="Universal Healthcare Coverage Expansion",
        authority="Government Health Programs"
    )
    
    quality_payment_program = Policy(
        label="Quality-Based Payment Program",
        authority="Government Health Programs"
    )
    
    interoperability_mandate = Policy(
        label="Health Data Interoperability Mandate",
        authority="Federal Healthcare Regulations"
    )
    
    prevention_investment = Policy(
        label="Prevention and Public Health Investment",
        authority="Public Health Agencies"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # POLICY INSTRUMENTS FOR HEALTH IMPROVEMENT
    # ═══════════════════════════════════════════════════════════════════
    
    payment_incentives = PolicyInstrument(
        label="Value-Based Payment Incentives",
        instrument_type=PolicyInstrumentType.ECONOMIC,
        target_behavior="quality_improvement",
        effectiveness_measure=0.75
    )
    
    quality_reporting = PolicyInstrument(
        label="Mandatory Quality Reporting",
        instrument_type=PolicyInstrumentType.REGULATORY,
        target_behavior="transparency_and_accountability",
        effectiveness_measure=0.8
    )
    
    clinical_guidelines = PolicyInstrument(
        label="Evidence-Based Clinical Guidelines",
        instrument_type=PolicyInstrumentType.INFORMATION,
        target_behavior="evidence_based_practice",
        effectiveness_measure=0.7
    )
    
    quality_collaboratives = PolicyInstrument(
        label="Multi-Stakeholder Quality Collaboratives",
        instrument_type=PolicyInstrumentType.VOLUNTARY,
        target_behavior="collaborative_improvement",
        effectiveness_measure=0.65
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # VALUE SYSTEMS IN HEALTHCARE
    # ═══════════════════════════════════════════════════════════════════
    
    medical_ethics_values = ValueSystem(
        label="Medical Ethics and Professionalism",
        legitimacy_source=LegitimacySource.TRADITIONAL,
        cultural_domain="medical_professionalism"
    )
    
    population_health_values = ValueSystem(
        label="Population Health Improvement Values",
        legitimacy_source=LegitimacySource.EXPERT,
        cultural_domain="public_health"
    )
    
    patient_rights_values = ValueSystem(
        label="Patient Rights and Autonomy Values",
        legitimacy_source=LegitimacySource.LEGAL_RATIONAL,
        cultural_domain="patient_advocacy"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # HEALTHCARE PROCESS MODELS
    # ═══════════════════════════════════════════════════════════════════
    
    care_delivery_process = Process(
        label="Integrated Care Delivery Process",
        technology="care_coordination_system"
    )
    
    quality_improvement_process = Process(
        label="Continuous Quality Improvement Process",
        technology="quality_measurement_system"
    )
    
    evidence_generation_process = Process(
        label="Clinical Evidence Generation Process",
        technology="research_infrastructure"
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # HEALTHCARE INFORMATION AND VALUE FLOWS
    # ═══════════════════════════════════════════════════════════════════
    
    # Clinical information flows
    clinical_data_flow = Flow(
        label="Clinical Data Sharing Flow",
        nature=FlowNature.INFORMATION,
        flow_type=FlowType.INFORMATION,
        temporal_dynamics=implementation_dynamics
    )
    
    evidence_dissemination = Flow(
        label="Evidence Dissemination Flow",
        nature=FlowNature.INFORMATION,
        flow_type=FlowType.INFORMATION
    )
    
    # Financial flows
    healthcare_payments = Flow(
        label="Healthcare Payment Flow",
        nature=FlowNature.FINANCIAL,
        flow_type=FlowType.FINANCIAL,
        temporal_dynamics=outcome_dynamics
    )
    
    research_investment = Flow(
        label="Health Research Investment Flow",
        nature=FlowNature.FINANCIAL,
        flow_type=FlowType.FINANCIAL
    )
    
    # Service delivery flows
    care_services = Flow(
        label="Healthcare Service Delivery",
        nature=FlowNature.OUTPUT,
        flow_type=FlowType.MATERIAL
    )
    
    population_health_services = Flow(
        label="Population Health Intervention Flow",
        nature=FlowNature.OUTPUT,
        flow_type=FlowType.MATERIAL
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # COMPREHENSIVE HEALTH OUTCOME INDICATORS
    # ═══════════════════════════════════════════════════════════════════
    
    # Clinical quality indicators
    clinical_outcomes = Indicator(
        label="Clinical Quality Outcomes",
        value_category=ValueCategory.HEALTH,
        measurement_unit="quality_score",
        current_value=72.0,
        target_value=85.0,
        temporal_dynamics=outcome_dynamics
    )
    
    patient_safety = Indicator(
        label="Patient Safety Incidents",
        value_category=ValueCategory.HEALTH,
        measurement_unit="incidents_per_1000",
        current_value=12.5,
        target_value=6.0
    )
    
    # Access and equity indicators
    healthcare_access = Indicator(
        label="Healthcare Access Equity",
        value_category=ValueCategory.EQUITY,
        measurement_unit="access_index",
        current_value=68.0,
        target_value=85.0,
        temporal_dynamics=implementation_dynamics
    )
    
    health_disparities = Indicator(
        label="Health Outcome Disparities",
        value_category=ValueCategory.EQUITY,
        measurement_unit="disparity_ratio",
        current_value=1.8,
        target_value=1.2
    )
    
    # Economic indicators
    healthcare_costs = Indicator(
        label="Healthcare Cost per Capita",
        value_category=ValueCategory.ECONOMIC,
        measurement_unit="USD_per_person",
        current_value=8500.0,
        target_value=7500.0
    )
    
    cost_effectiveness = Indicator(
        label="Cost-Effectiveness of Interventions",
        value_category=ValueCategory.ECONOMIC,
        measurement_unit="QALY_per_dollar",
        current_value=0.0012,
        target_value=0.0018
    )
    
    # Population health indicators
    preventable_hospitalizations = Indicator(
        label="Preventable Hospitalizations",
        value_category=ValueCategory.HEALTH,
        measurement_unit="admissions_per_1000",
        current_value=45.0,
        target_value=25.0,
        temporal_dynamics=outcome_dynamics
    )
    
    population_health_metrics = Indicator(
        label="Population Health Composite Score",
        value_category=ValueCategory.HEALTH,
        measurement_unit="health_index",
        current_value=74.0,
        target_value=88.0
    )
    
    # Technology adoption indicators
    ehr_adoption = Indicator(
        label="Electronic Health Record Adoption",
        value_category=ValueCategory.TECHNOLOGICAL,
        measurement_unit="adoption_percentage",
        current_value=78.0,
        target_value=95.0
    )
    
    telehealth_utilization = Indicator(
        label="Telehealth Service Utilization",
        value_category=ValueCategory.TECHNOLOGICAL,
        measurement_unit="utilization_rate",
        current_value=24.0,
        target_value=45.0
    )
    
    # Social and community indicators
    patient_satisfaction = Indicator(
        label="Patient Experience Satisfaction",
        value_category=ValueCategory.SOCIAL,
        measurement_unit="satisfaction_score",
        current_value=7.8,
        target_value=9.0
    )
    
    community_health_engagement = Indicator(
        label="Community Health Engagement",
        value_category=ValueCategory.SOCIAL,
        measurement_unit="engagement_index",
        current_value=62.0,
        target_value=80.0
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # ADD ALL NODES TO REPOSITORY AND GRAPH
    # ═══════════════════════════════════════════════════════════════════
    
    nodes = [
        # Actors
        primary_care_physicians, community_health_centers, hospital_systems,
        public_health_agencies, insurance_companies, government_payers,
        patient_advocacy_groups, community_organizations, health_tech_companies,
        research_institutions,
        
        # Institutions
        healthcare_regulations, professional_standards, quality_improvement,
        patient_safety_culture, value_based_care,
        
        # Technology Systems
        electronic_health_records, ai_diagnostic_support, telehealth_platform,
        population_health_analytics,
        
        # Cognitive Frameworks
        evidence_based_medicine, cost_effectiveness_framework, patient_centered_framework,
        prevention_framework,
        
        # Behavioral Patterns
        technology_adoption_behavior, clinical_guideline_adherence, preventive_care_seeking,
        collaborative_care_coordination,
        
        # Resources
        healthcare_workforce, clinical_expertise, healthcare_funding, research_funding,
        healthcare_infrastructure, health_data, clinical_evidence, health_surveillance_data,
        community_health_capacity, patient_engagement,
        
        # Policies
        universal_coverage_expansion, quality_payment_program, interoperability_mandate,
        prevention_investment,
        
        # Policy Instruments
        payment_incentives, quality_reporting, clinical_guidelines, quality_collaboratives,
        
        # Value Systems
        medical_ethics_values, population_health_values, patient_rights_values,
        
        # Processes
        care_delivery_process, quality_improvement_process, evidence_generation_process,
        
        # Flows
        clinical_data_flow, evidence_dissemination, healthcare_payments, research_investment,
        care_services, population_health_services,
        
        # Indicators
        clinical_outcomes, patient_safety, healthcare_access, health_disparities,
        healthcare_costs, cost_effectiveness, preventable_hospitalizations,
        population_health_metrics, ehr_adoption, telehealth_utilization,
        patient_satisfaction, community_health_engagement
    ]
    
    print(f"Adding {len(nodes)} nodes to repository...")
    for node in nodes:
        repo.create_node(node)
        graph.add_node(node)
    
    # ═══════════════════════════════════════════════════════════════════
    # COMPLEX HEALTHCARE SYSTEM RELATIONSHIPS
    # ═══════════════════════════════════════════════════════════════════
    
    relationships = [
        # Clinical care delivery relationships
        Relationship(
            source_id=primary_care_physicians.id,
            target_id=care_services.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.9,
            meta={"description": "Primary care service delivery"}
        ),
        
        Relationship(
            source_id=hospital_systems.id,
            target_id=care_services.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.85,
            meta={"description": "Acute care and specialized services"}
        ),
        
        Relationship(
            source_id=community_health_centers.id,
            target_id=population_health_services.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.8,
            meta={"description": "Community-based health services"}
        ),
        
        # Financial and payment relationships
        Relationship(
            source_id=insurance_companies.id,
            target_id=healthcare_payments.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.9,
            meta={"description": "Private insurance payments"}
        ),
        
        Relationship(
            source_id=government_payers.id,
            target_id=healthcare_payments.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.8,
            meta={"description": "Public program payments"}
        ),
        
        Relationship(
            source_id=healthcare_payments.id,
            target_id=primary_care_physicians.id,
            kind=RelationshipKind.INFLUENCES,
            weight=0.8,
            meta={"description": "Provider payment flow"}
        ),
        
        # Technology integration relationships
        Relationship(
            source_id=electronic_health_records.id,
            target_id=clinical_data_flow.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.9,
            meta={"description": "EHR data sharing capabilities"}
        ),
        
        Relationship(
            source_id=telehealth_platform.id,
            target_id=care_services.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.7,
            meta={"description": "Remote care delivery enhancement"}
        ),
        
        Relationship(
            source_id=ai_diagnostic_support.id,
            target_id=clinical_outcomes.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.6,
            meta={"description": "AI-enhanced diagnostic accuracy"}
        ),
        
        # Knowledge and evidence relationships
        Relationship(
            source_id=research_institutions.id,
            target_id=clinical_evidence.id,
            kind=RelationshipKind.PRODUCES,
            weight=0.95,
            meta={"description": "Clinical research evidence generation"}
        ),
        
        Relationship(
            source_id=clinical_evidence.id,
            target_id=evidence_dissemination.id,
            kind=RelationshipKind.INFORMS,
            weight=0.9,
            meta={"description": "Evidence-based knowledge sharing"}
        ),
        
        Relationship(
            source_id=evidence_dissemination.id,
            target_id=clinical_guidelines.id,
            kind=RelationshipKind.INFORMS,
            weight=0.8,
            meta={"description": "Evidence informing guidelines"}
        ),
        
        # Note: Cognitive framework relationships temporarily removed due to validation constraints
        # They can be re-added once CognitiveFramework is integrated into relationship validation rules
        
        # Behavioral pattern relationships
        Relationship(
            source_id=technology_adoption_behavior.id,
            target_id=ehr_adoption.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.8,
            meta={"description": "Technology adoption patterns affecting EHR use"}
        ),
        
        Relationship(
            source_id=clinical_guideline_adherence.id,
            target_id=clinical_outcomes.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.85,
            meta={"description": "Guideline adherence improving outcomes"}
        ),
        
        Relationship(
            source_id=preventive_care_seeking.id,
            target_id=preventable_hospitalizations.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.7,
            meta={"description": "Prevention reducing hospitalizations"}
        ),
        
        # Policy and regulation relationships
        Relationship(
            source_id=healthcare_regulations.id,
            target_id=interoperability_mandate.id,
            kind=RelationshipKind.ENFORCES,
            weight=0.9,
            meta={"description": "Regulatory enforcement of interoperability"}
        ),
        
        Relationship(
            source_id=quality_payment_program.id,
            target_id=payment_incentives.id,
            kind=RelationshipKind.IMPLEMENTS,
            weight=0.8,
            meta={"description": "Quality-based payment implementation"}
        ),
        
        # Value system alignments
        Relationship(
            source_id=medical_ethics_values.id,
            target_id=patient_safety_culture.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.9,
            meta={"description": "Medical ethics supporting patient safety"}
        ),
        
        Relationship(
            source_id=population_health_values.id,
            target_id=prevention_investment.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.85,
            meta={"description": "Population health values driving prevention investment"}
        ),
        
        Relationship(
            source_id=patient_rights_values.id,
            target_id=patient_advocacy_groups.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.9,
            meta={"description": "Patient rights values supporting advocacy"}
        ),
        
        # Quality improvement relationships
        Relationship(
            source_id=quality_improvement.id,
            target_id=clinical_outcomes.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.8,
            meta={"description": "Quality improvement initiatives enhancing outcomes"}
        ),
        
        Relationship(
            source_id=quality_reporting.id,
            target_id=healthcare_access.id,
            kind=RelationshipKind.MEASURES,
            weight=0.7,
            meta={"description": "Quality reporting tracking access"}
        ),
        
        # Community and social relationships
        Relationship(
            source_id=community_organizations.id,
            target_id=community_health_engagement.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.85,
            meta={"description": "Community organizations driving engagement"}
        ),
        
        Relationship(
            source_id=patient_advocacy_groups.id,
            target_id=patient_satisfaction.id,
            kind=RelationshipKind.AFFECTS,
            weight=0.7,
            meta={"description": "Patient advocacy improving satisfaction"}
        ),
        
        # Resource allocation relationships - government manages funding and infrastructure
        Relationship(
            source_id=government_payers.id,
            target_id=healthcare_funding.id,
            kind=RelationshipKind.USES,
            weight=0.8,
            meta={"description": "Government manages healthcare funding"}
        ),
        
        Relationship(
            source_id=government_payers.id,
            target_id=healthcare_infrastructure.id,
            kind=RelationshipKind.USES,
            weight=0.8,
            meta={"description": "Government uses healthcare infrastructure"}
        ),
        
        Relationship(
            source_id=research_funding.id,
            target_id=government_payers.id,
            kind=RelationshipKind.SUPPLIES,
            weight=0.9,
            meta={"description": "Research funding supports government healthcare programs"}
        ),
        
        # Outcome measurement relationships
        Relationship(
            source_id=population_health_analytics.id,
            target_id=population_health_metrics.id,
            kind=RelationshipKind.MEASURES,
            weight=0.9,
            meta={"description": "Analytics platform measuring population health"}
        ),
        
        Relationship(
            source_id=clinical_data_flow.id,
            target_id=cost_effectiveness.id,
            kind=RelationshipKind.INFORMS,
            weight=0.75,
            meta={"description": "Clinical data informing cost-effectiveness analysis"}
        )
    ]
    
    print(f"Creating {len(relationships)} relationships...")
    for relationship in relationships:
        repo.create_relationship(relationship)
        graph.add_relationship(relationship)
    
    print(f"Healthcare Policy SFM Graph completed with {len(nodes)} nodes and {len(relationships)} relationships.")
    return graph


if __name__ == "__main__":
    # Initialize repository and graph
    repo = NetworkXSFMRepository()
    sfm_graph = SFMGraph()
    repo.save_graph(sfm_graph)
    
    # Create the comprehensive healthcare policy graph
    healthcare_graph = create_healthcare_policy_graph(repo, sfm_graph)
    
    # ═══════════════════════════════════════════════════════════════════
    # COMPREHENSIVE HEALTHCARE SYSTEM ANALYSIS
    # ═══════════════════════════════════════════════════════════════════
    
    print(f"\n{'='*75}")
    print("HEALTHCARE SYSTEM POLICY ANALYSIS")
    print(f"{'='*75}")
    
    print(f"\nGraph Structure Summary:")
    print(f"  Total entities: {len(healthcare_graph)} nodes")
    print(f"  Actors: {len(healthcare_graph.actors)}")
    print(f"  Institutions: {len(healthcare_graph.institutions)}")
    print(f"  Resources: {len(healthcare_graph.resources)}")
    print(f"  Policies: {len(healthcare_graph.policies)}")
    print(f"  Flows: {len(healthcare_graph.flows)}")
    print(f"  Indicators: {len(healthcare_graph.indicators)}")
    print(f"  Technology Systems: {len(healthcare_graph.technology_systems)}")
    print(f"  Policy Instruments: {len(healthcare_graph.policy_instruments)}")
    print(f"  Processes: {len(healthcare_graph.processes)}")
    print(f"  Relationships: {len(healthcare_graph.relationships)}")
    
    try:
        # Create advanced query engine
        query_engine = SFMQueryFactory.create_query_engine(healthcare_graph, "networkx")
        
        print(f"\n{'-'*55}")
        print("HEALTHCARE STAKEHOLDER ANALYSIS")
        print(f"{'-'*55}")
        
        # Analyze most central healthcare actors
        print("\n🎯 Most Central Healthcare Stakeholders (Betweenness Centrality):")
        from core.sfm_models import Actor
        central_actors = query_engine.get_most_central_nodes(Actor, "betweenness", 8)
        for node_id, score in central_actors:
            actor = healthcare_graph.actors.get(node_id)
            if actor:
                print(f"  • {actor.label}: {score:.3f}")
        
        # Network topology analysis
        print(f"\n📊 Healthcare Network Topology:")
        density = query_engine.get_network_density()
        print(f"  • Network density: {density:.3f}")
        
        # Stakeholder power analysis
        print(f"\n⚡ Healthcare Stakeholder Power Distribution:")
        power_rankings = []
        for actor_id, actor in healthcare_graph.actors.items():
            if hasattr(actor, 'power_resources') and actor.power_resources:
                total_power = sum(actor.power_resources.values())
                avg_power = total_power / len(actor.power_resources)
                power_rankings.append((actor.label, avg_power))
        
        power_rankings.sort(key=lambda x: x[1], reverse=True)
        for actor_name, avg_power in power_rankings[:8]:
            print(f"  • {actor_name}: {avg_power:.2f} average power")
        
        print(f"\n{'-'*55}")
        print("COGNITIVE FRAMEWORK ANALYSIS")
        print(f"{'-'*55}")
        
        # Analyze cognitive frameworks and their influence
        print(f"\n🧠 Cognitive Framework Influence Analysis:")
        cognitive_frameworks = [
            ("Evidence-Based Medicine Framework", "Clinical decision-making"),
            ("Health Economics Cost-Effectiveness Framework", "Resource allocation"),
            ("Patient-Centered Care Framework", "Care delivery approach"),
            ("Public Health Prevention Framework", "Population health strategy")
        ]
        
        for framework_name, domain in cognitive_frameworks:
            framework_connections = 0
            for rel in healthcare_graph.relationships.values():
                # Find framework node and count its connections
                for node_id, node in healthcare_graph.nodes.items() if hasattr(healthcare_graph, 'nodes') else []:
                    if hasattr(node, 'label') and node.label == framework_name:
                        if rel.source_id == node_id or rel.target_id == node_id:
                            framework_connections += 1
                        break
            print(f"  • {framework_name} ({domain}): {framework_connections} connections")
        
        print(f"\n{'-'*55}")
        print("POLICY INTERVENTION ANALYSIS")
        print(f"{'-'*55}")
        
        # Analyze policy impacts and effectiveness
        print(f"\n📋 Healthcare Policy Impact Analysis:")
        for policy_id, policy in healthcare_graph.policies.items():
            affected_nodes = query_engine.analyze_policy_impact(policy_id)
            print(f"  • {policy.label}: affects {len(affected_nodes)} nodes")
        
        print(f"\n🛠️ Policy Instrument Effectiveness:")
        for instr_id, instr in healthcare_graph.policy_instruments.items():
            connections = 0
            for rel in healthcare_graph.relationships.values():
                if rel.source_id == instr_id or rel.target_id == instr_id:
                    connections += 1
            effectiveness = getattr(instr, 'effectiveness_measure', 'N/A')
            print(f"  • {instr.label}: {connections} connections, {effectiveness} effectiveness")
        
        print(f"\n{'-'*55}")
        print("TECHNOLOGY INTEGRATION ANALYSIS")
        print(f"{'-'*55}")
        
        # Analyze healthcare technology adoption
        print(f"\n🔬 Healthcare Technology Integration Assessment:")
        for tech_id, tech_system in healthcare_graph.technology_systems.items():
            if hasattr(tech_system, 'maturity') and tech_system.maturity:
                print(f"  • {tech_system.label}: TRL {tech_system.maturity.value}")
                if hasattr(tech_system, 'compatibility') and tech_system.compatibility:
                    avg_compatibility = sum(tech_system.compatibility.values()) / len(tech_system.compatibility)
                    print(f"    └─ Average compatibility: {avg_compatibility:.2f}")
        
        print(f"\n{'-'*55}")
        print("BEHAVIORAL PATTERN ANALYSIS")
        print(f"{'-'*55}")
        
        # Analyze behavioral patterns in healthcare
        print(f"\n🎭 Healthcare Behavioral Pattern Analysis:")
        behavioral_patterns = [
            "Healthcare Technology Adoption",
            "Clinical Guideline Adherence", 
            "Preventive Care Seeking Behavior",
            "Collaborative Care Coordination"
        ]
        
        for pattern_name in behavioral_patterns:
            pattern_connections = 0
            for rel in healthcare_graph.relationships.values():
                # Find pattern node and count connections
                for collection_name in ['actors', 'institutions', 'resources', 'flows']:
                    collection = getattr(healthcare_graph, collection_name, {})
                    for node_id, node in collection.items():
                        if hasattr(node, 'label') and pattern_name in node.label:
                            if rel.source_id == node_id or rel.target_id == node_id:
                                pattern_connections += 1
                            break
            print(f"  • {pattern_name}: {pattern_connections} total connections")
        
        print(f"\n{'-'*55}")
        print("FLOW AND VALUE STREAM ANALYSIS")
        print(f"{'-'*55}")
        
        # Analyze healthcare flows
        print(f"\n💰 Healthcare Flow Analysis:")
        for flow_id, flow in healthcare_graph.flows.items():
            flow_connections = 0
            for rel in healthcare_graph.relationships.values():
                if rel.source_id == flow_id or rel.target_id == flow_id:
                    flow_connections += 1
            flow_nature = flow.nature.name if hasattr(flow.nature, 'name') else str(flow.nature)
            print(f"  • {flow.label} ({flow_nature}): {flow_connections} connections")
        
        print(f"\n{'-'*55}")
        print("QUALITY AND OUTCOME INDICATORS")
        print(f"{'-'*55}")
        
        # Categorize and analyze health outcomes
        print(f"\n📊 Health Outcome Indicators by Category:")
        indicator_categories = {
            ValueCategory.HEALTH: [],
            ValueCategory.EQUITY: [],
            ValueCategory.ECONOMIC: [],
            ValueCategory.TECHNOLOGICAL: [],
            ValueCategory.SOCIAL: []
        }
        
        for indicator in healthcare_graph.indicators.values():
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
        
        print(f"\n{'-'*55}")
        print("VALUE SYSTEM ALIGNMENT ANALYSIS")
        print(f"{'-'*55}")
        
        # Analyze value system influences
        print(f"\n💎 Healthcare Value System Analysis:")
        value_systems = [
            "Medical Ethics and Professionalism",
            "Population Health Improvement Values",
            "Patient Rights and Autonomy Values"
        ]
        
        for value_system_name in value_systems:
            connections = 0
            for rel in healthcare_graph.relationships.values():
                # Find value system node and count connections
                for collection_name in ['actors', 'institutions', 'policies']:
                    collection = getattr(healthcare_graph, collection_name, {})
                    for node_id, node in collection.items():
                        if hasattr(node, 'label') and value_system_name in node.label:
                            if rel.source_id == node_id or rel.target_id == node_id:
                                connections += 1
                            break
            print(f"  • {value_system_name}: {connections} relationships")
        
        print(f"\n{'-'*55}")
        print("TEMPORAL DYNAMICS ANALYSIS")
        print(f"{'-'*55}")
        
        # Analyze temporal patterns in healthcare reform
        print(f"\n⏰ Healthcare Reform Temporal Dynamics:")
        temporal_entities = 0
        implementation_patterns = 0
        outcome_patterns = 0
        
        all_collections = [
            healthcare_graph.flows, healthcare_graph.indicators,
            healthcare_graph.policies
        ]
        
        for collection in all_collections:
            for entity in collection.values():
                if hasattr(entity, 'temporal_dynamics') and entity.temporal_dynamics:
                    temporal_entities += 1
                    function_type = entity.temporal_dynamics.function_type
                    function_name = function_type.name if hasattr(function_type, 'name') else str(function_type)
                    print(f"  • {entity.label}: {function_name} dynamics")
                    
                    if "logistic" in function_name.lower():
                        implementation_patterns += 1
                    elif "linear" in function_name.lower():
                        outcome_patterns += 1
        
        print(f"\nTemporal dynamics summary:")
        print(f"  • Total entities with temporal patterns: {temporal_entities}")
        print(f"  • Implementation pattern entities: {implementation_patterns}")
        print(f"  • Outcome improvement entities: {outcome_patterns}")
        
        print(f"\n{'-'*55}")
        print("SYSTEM VULNERABILITY ASSESSMENT")
        print(f"{'-'*55}")
        
        # Healthcare system resilience analysis
        print(f"\n🔍 Healthcare System Vulnerability Assessment:")
        try:
            vulnerabilities = query_engine.system_vulnerability_analysis()
            print(f"  • Comprehensive vulnerability analysis completed")
            
            # Identify critical bridges in healthcare system
            bridges = query_engine.get_structural_holes()
            print(f"\n🌉 Critical Healthcare System Bridges:")
            for bridge_id in bridges[:6]:
                bridge_node = None
                for collection in [healthcare_graph.actors, healthcare_graph.institutions,
                                 healthcare_graph.technology_systems]:
                    if bridge_id in collection:
                        bridge_node = collection[bridge_id]
                        break
                if bridge_node:
                    print(f"  • {bridge_node.label}")
                    
        except Exception as e:
            print(f"  • Vulnerability assessment: {str(e)}")
        
    except Exception as e:
        print(f"\nAnalysis error: {e}")
        import traceback
        traceback.print_exc()
    
    # Clean up
    healthcare_graph.clear()
    repo.clear()
    
    print(f"\n{'='*75}")
    print("HEALTHCARE SYSTEM ANALYSIS COMPLETE - Graph cleared")
    print(f"{'='*75}")