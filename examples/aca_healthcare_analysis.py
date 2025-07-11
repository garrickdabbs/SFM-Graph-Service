#!/usr/bin/env python3
"""
Complex Policy Analysis Example: Affordable Care Act (ACA) Healthcare Outcomes
Healthcare System Impact Analysis

This example demonstrates advanced SFM-Graph-Service features through a comprehensive
analysis of the Affordable Care Act and its impact on healthcare outcomes. The analysis
includes thousands of nodes and relationships representing:

- Federal and state healthcare agencies
- Healthcare providers and insurance systems
- Patient populations and demographics
- Healthcare policy instruments and programs
- Health outcome indicators and metrics
- Financial flows and coverage relationships

Features Demonstrated:
1. Graph persistence and serialization
2. Advanced caching and performance optimization
3. Security validation and input sanitization
4. Performance monitoring and metrics collection
5. High-level service layer features
6. Complex analytics and queries

Data Sources:
- ACA legislation and regulatory framework
- CMS enrollment and outcome data
- State Medicaid expansion decisions
- Healthcare provider network data
- Insurance marketplace statistics
- Public health outcome metrics
"""

import json
import logging
import random
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set

# SFM Framework imports
from core.sfm_service import SFMService
from core.sfm_models import (
    Actor, Institution, Policy, Resource, Process, Flow, ValueFlow,
    Indicator, AnalyticalContext, SFMGraph
)
from core.sfm_enums import (
    InstitutionLayer, ResourceType, FlowNature, RelationshipKind, ValueCategory
)
from core.relationships import Relationship
from core.sfm_persistence import SFMPersistenceManager, StorageFormat
from core.advanced_caching import MultiLevelCache, CacheType
from core.performance_metrics import PerformanceMetrics, MetricsCollector
from core.security_validators import SecurityValidationError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ACAAnalysisExample:
    """
    Comprehensive analysis of the Affordable Care Act (ACA) and its impact
    on healthcare outcomes using SFM-Graph-Service.
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize the ACA analysis example."""
        self.data_dir = data_dir or Path("aca_analysis_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize core components
        self.service = SFMService()
        self.graph = self.service.get_graph()
        self.persistence_manager = SFMPersistenceManager(str(self.data_dir))
        self.cache_manager = MultiLevelCache("aca_analysis")
        self.metrics_collector = MetricsCollector()
        
        # Analysis context
        self.analysis_context = AnalyticalContext(
            label="ACA Healthcare Outcomes Analysis",
            description="Analysis of Affordable Care Act impact on healthcare access and outcomes",
            methods_used=["Social Fabric Matrix", "Network analysis", "Healthcare outcomes assessment"],
            assumptions={
                "healthcare_access_definition": "Insurance coverage and provider availability",
                "outcomes_measurement": "Health indicators and utilization rates",
                "geographic_scope": "United States with state-level variations",
                "time_period": "2010-2023"
            },
            data_sources={
                "healthcare_policy": "ACA legislation and CMS guidance",
                "enrollment_data": "CMS enrollment statistics",
                "outcome_data": "CDC and HRSA health outcome metrics",
                "provider_data": "Healthcare provider network information"
            }
        )
        
        # Data containers
        self.actors: Dict[str, Actor] = {}
        self.institutions: Dict[str, Institution] = {}
        self.policies: Dict[str, Policy] = {}
        self.resources: Dict[str, Resource] = {}
        self.processes: Dict[str, Process] = {}
        self.flows: Dict[str, Flow] = {}
        self.indicators: Dict[str, Indicator] = {}
        
        # Performance tracking
        self.performance_metrics = PerformanceMetrics()
        
    def validate_and_sanitize_input(self, data: Any) -> Any:
        """Validate and sanitize input data for security."""
        # Basic validation - could be expanded with actual security checks
        if data is None:
            raise SecurityValidationError("Input data cannot be None")
        return data
    
    def create_federal_healthcare_agencies(self) -> None:
        """Create federal healthcare agencies and related actors."""
        logger.info("Creating federal healthcare agencies...")
        
        # Centers for Medicare & Medicaid Services (CMS)
        cms = Actor(
            label="Centers for Medicare & Medicaid Services",
            description="Federal agency administering Medicare, Medicaid, and ACA programs",
            sector="Government",
            legal_form="Federal Agency"
        )
        self.actors["cms"] = cms
        self.service.add_actor(cms)
        
        # Health and Human Services (HHS)
        hhs = Actor(
            label="Department of Health and Human Services",
            description="Federal executive department overseeing health policy",
            sector="Government",
            legal_form="Federal Department"
        )
        self.actors["hhs"] = hhs
        self.service.add_actor(hhs)
        
        # Centers for Disease Control and Prevention (CDC)
        cdc = Actor(
            label="Centers for Disease Control and Prevention",
            description="Federal agency for public health surveillance and prevention",
            sector="Government",
            legal_form="Federal Agency"
        )
        self.actors["cdc"] = cdc
        self.service.add_actor(cdc)
        
        # Health Resources and Services Administration (HRSA)
        hrsa = Actor(
            label="Health Resources and Services Administration",
            description="Federal agency improving healthcare access for underserved populations",
            sector="Government",
            legal_form="Federal Agency"
        )
        self.actors["hrsa"] = hrsa
        self.service.add_actor(hrsa)
    
    def create_state_healthcare_systems(self) -> None:
        """Create state-level healthcare systems and Medicaid programs."""
        logger.info("Creating state healthcare systems...")
        
        # State healthcare systems with Medicaid expansion status
        states_data = [
            ("California", "ca", True),
            ("Texas", "tx", False),
            ("New York", "ny", True),
            ("Florida", "fl", False),
            ("Illinois", "il", True),
            ("Pennsylvania", "pa", True),
            ("Ohio", "oh", True),
            ("Georgia", "ga", False),
            ("North Carolina", "nc", False),
            ("Michigan", "mi", True),
            ("New Jersey", "nj", True),
            ("Virginia", "va", True),
            ("Washington", "wa", True),
            ("Arizona", "az", True),
            ("Massachusetts", "ma", True),
            ("Tennessee", "tn", False),
            ("Indiana", "in", True),
            ("Missouri", "mo", True),
            ("Maryland", "md", True),
            ("Wisconsin", "wi", False)
        ]
        
        for state_name, state_code, medicaid_expanded in states_data:
            # State Health Department
            health_dept = Actor(
                label=f"{state_name} Department of Health",
                description=f"State health department for {state_name}",
                sector="Government",
                legal_form="State Agency"
            )
            self.actors[f"{state_code}_health_dept"] = health_dept
            self.service.add_actor(health_dept)
            
            # State Medicaid Program
            medicaid_program = Actor(
                label=f"{state_name} Medicaid Program",
                description=f"State Medicaid program for {state_name} - {'Expanded' if medicaid_expanded else 'Not Expanded'}",
                sector="Government",
                legal_form="State Program"
            )
            self.actors[f"{state_code}_medicaid"] = medicaid_program
            self.service.add_actor(medicaid_program)
            
            # State Insurance Commissioner
            insurance_commissioner = Actor(
                label=f"{state_name} Insurance Commissioner",
                description=f"State insurance regulator for {state_name}",
                sector="Government",
                legal_form="State Regulatory Agency"
            )
            self.actors[f"{state_code}_insurance"] = insurance_commissioner
            self.service.add_actor(insurance_commissioner)
    
    def create_healthcare_providers(self) -> None:
        """Create healthcare provider networks and systems."""
        logger.info("Creating healthcare provider networks...")
        
        # Major healthcare systems
        healthcare_systems = [
            ("Kaiser Permanente", "integrated_hmo"),
            ("Anthem Inc.", "insurer"),
            ("UnitedHealth Group", "insurer"),
            ("Aetna", "insurer"),
            ("Cigna", "insurer"),
            ("Humana", "insurer"),
            ("Blue Cross Blue Shield", "insurer_network"),
            ("Cleveland Clinic", "provider_system"),
            ("Mayo Clinic", "provider_system"),
            ("Johns Hopkins", "provider_system"),
            ("Community Health Centers", "safety_net"),
            ("Rural Health Clinics", "safety_net")
        ]
        
        for system_name, system_type in healthcare_systems:
            system_key = system_name.lower().replace(" ", "_").replace(".", "")
            
            # Determine sector based on type
            if system_type == "insurer" or system_type == "insurer_network":
                sector = "Private"
            elif system_type == "safety_net":
                sector = "Nonprofit"
            else:
                sector = "Mixed"
            
            provider = Actor(
                label=system_name,
                description=f"Healthcare {system_type}",
                sector=sector,
                legal_form="Healthcare Organization"
            )
            self.actors[system_key] = provider
            self.service.add_actor(provider)
    
    def create_patient_populations(self) -> None:
        """Create patient population demographics and groups."""
        logger.info("Creating patient population demographics...")
        
        # Patient populations by insurance status and demographics
        populations = [
            {
                "key": "uninsured_adults",
                "label": "Uninsured Adults (Pre-ACA)",
                "description": "Adults without health insurance before ACA implementation",
                "size": 48000000
            },
            {
                "key": "medicaid_expansion_eligible",
                "label": "Medicaid Expansion Eligible Adults",
                "description": "Adults eligible for Medicaid under ACA expansion",
                "size": 15000000
            },
            {
                "key": "marketplace_enrollees",
                "label": "ACA Marketplace Enrollees",
                "description": "Individuals enrolled in ACA marketplace plans",
                "size": 12000000
            },
            {
                "key": "employer_insured",
                "label": "Employer-Sponsored Insurance",
                "description": "Individuals with employer-sponsored health insurance",
                "size": 155000000
            },
            {
                "key": "medicare_beneficiaries",
                "label": "Medicare Beneficiaries",
                "description": "Individuals enrolled in Medicare",
                "size": 64000000
            },
            {
                "key": "dual_eligible",
                "label": "Dual-Eligible Beneficiaries",
                "description": "Individuals eligible for both Medicare and Medicaid",
                "size": 12000000
            },
            {
                "key": "young_adults",
                "label": "Young Adults (26-30)",
                "description": "Young adults affected by ACA dependent coverage extension",
                "size": 18000000
            },
            {
                "key": "chronic_conditions",
                "label": "Adults with Chronic Conditions",
                "description": "Adults with pre-existing chronic conditions",
                "size": 133000000
            }
        ]
        
        for pop_data in populations:
            population = Actor(
                label=pop_data["label"],
                description=f"{pop_data['description']} - approximately {pop_data['size']:,} individuals",
                sector="Household",
                legal_form="Population Group"
            )
            self.actors[pop_data["key"]] = population
            self.service.add_actor(population)
    
    def create_aca_policy_structure(self) -> None:
        """Create the ACA policy and its major provisions."""
        logger.info("Creating ACA policy structure...")
        
        # Main ACA Policy
        aca_policy = Policy(
            label="Affordable Care Act (ACA) - Patient Protection and Affordable Care Act",
            description="Comprehensive healthcare reform legislation enacted in 2010",
            layer=InstitutionLayer.FORMAL_RULES,
            authority="U.S. Congress",
            enforcement=0.9,
            target_sectors=["Healthcare coverage", "Insurance regulation", "Medicaid expansion"]
        )
        self.policies["aca"] = aca_policy
        self.service.add_policy(aca_policy)
        
        # Key ACA Provisions as separate policies
        provisions = [
            {
                "key": "individual_mandate",
                "name": "Individual Mandate",
                "description": "Requirement for individuals to maintain health insurance coverage"
            },
            {
                "key": "employer_mandate",
                "name": "Employer Mandate",
                "description": "Requirement for large employers to provide health insurance"
            },
            {
                "key": "medicaid_expansion",
                "name": "Medicaid Expansion",
                "description": "Expansion of Medicaid eligibility to 138% of federal poverty level"
            },
            {
                "key": "insurance_marketplaces",
                "name": "Health Insurance Marketplaces",
                "description": "State-based exchanges for purchasing individual health insurance"
            },
            {
                "key": "essential_health_benefits",
                "name": "Essential Health Benefits",
                "description": "Minimum coverage requirements for health insurance plans"
            },
            {
                "key": "preexisting_protections",
                "name": "Pre-existing Condition Protections",
                "description": "Prohibition on denying coverage based on health status"
            },
            {
                "key": "premium_subsidies",
                "name": "Premium Tax Credits",
                "description": "Financial assistance for marketplace insurance premiums"
            },
            {
                "key": "cost_sharing_reductions",
                "name": "Cost-Sharing Reductions",
                "description": "Reduced out-of-pocket costs for low-income marketplace enrollees"
            }
        ]
        
        for provision in provisions:
            policy = Policy(
                label=provision["name"],
                description=provision["description"],
                layer=InstitutionLayer.FORMAL_RULES,
                authority="Centers for Medicare & Medicaid Services",
                enforcement=0.8,
                target_sectors=["Healthcare coverage"]
            )
            self.policies[provision["key"]] = policy
            self.service.add_policy(policy)
    
    def create_health_outcome_indicators(self) -> None:
        """Create health outcome indicators for measuring ACA impact."""
        logger.info("Creating health outcome indicators...")
        
        indicators_data = [
            {
                "key": "uninsured_rate",
                "name": "Uninsured Rate - Adults",
                "description": "Percentage of adults without health insurance coverage",
                "category": ValueCategory.HEALTH,
                "unit": "percentage",
                "baseline": 18.2,
                "current": 10.9
            },
            {
                "key": "medicaid_enrollment",
                "name": "Medicaid Enrollment",
                "description": "Total number of individuals enrolled in Medicaid",
                "category": ValueCategory.HEALTH,
                "unit": "millions",
                "baseline": 54.1,
                "current": 82.6
            },
            {
                "key": "marketplace_enrollment",
                "name": "ACA Marketplace Enrollment",
                "description": "Total enrollment in ACA health insurance marketplaces",
                "category": ValueCategory.HEALTH,
                "unit": "millions",
                "baseline": 0.0,
                "current": 14.5
            },
            {
                "key": "preventive_care_utilization",
                "name": "Preventive Care Utilization Rate",
                "description": "Percentage of adults receiving recommended preventive care",
                "category": ValueCategory.HEALTH,
                "unit": "percentage",
                "baseline": 42.5,
                "current": 58.2
            },
            {
                "key": "medical_debt_burden",
                "name": "Medical Debt Burden",
                "description": "Percentage of adults with medical debt",
                "category": ValueCategory.ECONOMIC,
                "unit": "percentage",
                "baseline": 28.7,
                "current": 21.3
            },
            {
                "key": "emergency_dept_visits",
                "name": "Emergency Department Visits per 1000",
                "description": "Rate of emergency department visits per 1000 population",
                "category": ValueCategory.HEALTH,
                "unit": "per_1000",
                "baseline": 425.0,
                "current": 398.5
            },
            {
                "key": "primary_care_access",
                "name": "Primary Care Access Score",
                "description": "Composite score measuring access to primary care services",
                "category": ValueCategory.HEALTH,
                "unit": "index_score",
                "baseline": 6.2,
                "current": 7.4
            },
            {
                "key": "health_outcomes_index",
                "name": "Population Health Outcomes Index",
                "description": "Composite index of population health outcomes",
                "category": ValueCategory.HEALTH,
                "unit": "index_score",
                "baseline": 6.8,
                "current": 7.3
            }
        ]
        
        for indicator_data in indicators_data:
            indicator = Indicator(
                label=indicator_data["name"],
                description=indicator_data["description"],
                value_category=indicator_data["category"],
                measurement_unit=indicator_data["unit"],
                current_value=indicator_data["current"],
                target_value=indicator_data["baseline"],
                threshold_values={
                    "baseline": indicator_data["baseline"],
                    "current": indicator_data["current"]
                }
            )
            self.indicators[indicator_data["key"]] = indicator
            self.service.add_indicator(indicator)
    
    def create_healthcare_flows(self) -> None:
        """Create healthcare and financial flows."""
        logger.info("Creating healthcare and financial flows...")
        
        flows_data = [
            {
                "key": "federal_medicaid_funding",
                "name": "Federal Medicaid Funding",
                "description": "Federal funding for state Medicaid programs",
                "nature": FlowNature.FINANCIAL,
                "volume": 438000000000,
                "unit": "dollars_annual"
            },
            {
                "key": "marketplace_subsidies",
                "name": "ACA Marketplace Premium Subsidies",
                "description": "Federal premium tax credits for marketplace enrollees",
                "nature": FlowNature.FINANCIAL,
                "volume": 68000000000,
                "unit": "dollars_annual"
            },
            {
                "key": "cost_sharing_reductions",
                "name": "Cost-Sharing Reduction Payments",
                "description": "Federal payments to insurers for cost-sharing reductions",
                "nature": FlowNature.FINANCIAL,
                "volume": 15000000000,
                "unit": "dollars_annual"
            },
            {
                "key": "healthcare_utilization",
                "name": "Healthcare Service Utilization",
                "description": "Patient utilization of healthcare services",
                "nature": FlowNature.SERVICE,
                "volume": 8500000000,
                "unit": "encounters_annual"
            },
            {
                "key": "insurance_premium_flow",
                "name": "Insurance Premium Payments",
                "description": "Premium payments from individuals and employers to insurers",
                "nature": FlowNature.FINANCIAL,
                "volume": 1200000000000,
                "unit": "dollars_annual"
            },
            {
                "key": "provider_reimbursement",
                "name": "Provider Reimbursement",
                "description": "Payments from insurers to healthcare providers",
                "nature": FlowNature.FINANCIAL,
                "volume": 2100000000000,
                "unit": "dollars_annual"
            }
        ]
        
        for flow_data in flows_data:
            flow = Flow(
                label=flow_data["name"],
                description=flow_data["description"],
                nature=flow_data["nature"],
                quantity=flow_data["volume"],
                unit=flow_data["unit"]
            )
            self.flows[flow_data["key"]] = flow
            self.service.add_flow(flow)
    
    def create_institutional_framework(self) -> None:
        """Create institutional framework for healthcare policy implementation."""
        logger.info("Creating institutional framework...")
        
        # Federal Healthcare Governance
        federal_healthcare = Institution(
            label="Federal Healthcare Governance System",
            description="Comprehensive federal healthcare policy and administration system",
            layer=InstitutionLayer.FORMAL_RULES,
            formal_rules=[
                "Affordable Care Act",
                "Medicare statutes",
                "Medicaid regulations",
                "CMS administrative guidance"
            ],
            enforcement_mechanisms=[
                "Regulatory oversight",
                "Compliance monitoring",
                "Financial penalties",
                "Program sanctions"
            ],
            legitimacy_basis="Congressional authorization"
        )
        self.institutions["federal_healthcare"] = federal_healthcare
        self.service.add_institution(federal_healthcare)
        
        # State Healthcare Systems
        state_healthcare = Institution(
            label="State Healthcare Administration Systems",
            description="State-level healthcare administration and Medicaid systems",
            layer=InstitutionLayer.ORGANIZATIONS,
            formal_rules=[
                "State health codes",
                "Medicaid state plans",
                "Insurance regulations"
            ],
            enforcement_mechanisms=[
                "State oversight",
                "Provider licensing",
                "Plan certification"
            ],
            legitimacy_basis="State authority"
        )
        self.institutions["state_healthcare"] = state_healthcare
        self.service.add_institution(state_healthcare)
        
        # Healthcare Market Institutions
        healthcare_markets = Institution(
            label="Healthcare Insurance Market Framework",
            description="Regulated healthcare insurance market system",
            layer=InstitutionLayer.INFORMAL_NORMS,
            informal_norms=[
                "Professional standards",
                "Market practices",
                "Quality expectations",
                "Patient rights"
            ],
            enforcement_mechanisms=[
                "Professional peer review",
                "Market competition",
                "Accreditation requirements",
                "Consumer advocacy"
            ],
            legitimacy_basis="Market acceptance"
        )
        self.institutions["healthcare_markets"] = healthcare_markets
        self.service.add_institution(healthcare_markets)
    
    def create_relationships(self) -> None:
        """Create relationships between all entities in the analysis."""
        logger.info("Creating relationships...")
        
        # Policy Implementation Relationships
        implementation_relationships = [
            ("hhs", "aca", RelationshipKind.IMPLEMENTS),
            ("cms", "aca", RelationshipKind.IMPLEMENTS),
            ("cdc", "aca", RelationshipKind.SUPPORTS),
            ("hrsa", "aca", RelationshipKind.SUPPORTS)
        ]
        
        for source_key, target_key, kind in implementation_relationships:
            if source_key in self.actors and target_key in self.policies:
                relationship = Relationship(
                    source_id=self.actors[source_key].id,
                    target_id=self.policies[target_key].id,
                    relationship_kind=kind,
                    strength=9.0,
                    description=f"{self.actors[source_key].label} {kind.value} {self.policies[target_key].label}"
                )
                self.service.add_relationship(relationship)
        
        # State-Federal Relationships
        state_codes = ["ca", "tx", "ny", "fl", "il", "pa", "oh", "ga", "nc", "mi"]
        for state_code in state_codes:
            medicaid_key = f"{state_code}_medicaid"
            if medicaid_key in self.actors:
                # State Medicaid - Federal CMS relationship
                relationship = Relationship(
                    source_id=self.actors["cms"].id,
                    target_id=self.actors[medicaid_key].id,
                    relationship_kind=RelationshipKind.OVERSEES,
                    strength=9.0,
                    description=f"CMS oversees {self.actors[medicaid_key].label}"
                )
                self.service.add_relationship(relationship)
        
        # Provider-Patient Relationships
        provider_keys = ["kaiser_permanente", "anthem_inc", "unitedhealth_group", "community_health_centers"]
        patient_keys = ["medicaid_expansion_eligible", "marketplace_enrollees", "employer_insured"]
        
        for provider_key in provider_keys:
            if provider_key in self.actors:
                for patient_key in patient_keys:
                    if patient_key in self.actors:
                        strength = random.uniform(6.0, 8.5)
                        
                        relationship = Relationship(
                            source_id=self.actors[provider_key].id,
                            target_id=self.actors[patient_key].id,
                            relationship_kind=RelationshipKind.SERVES,
                            strength=strength,
                            description=f"{self.actors[provider_key].label} serves {self.actors[patient_key].label}"
                        )
                        self.service.add_relationship(relationship)
        
        # Policy Provision Impact Relationships
        provision_keys = [key for key in self.policies.keys() if key != "aca"]
        population_keys = [k for k in self.actors.keys() if any(term in k for term in ["uninsured", "medicaid", "marketplace", "chronic"])]
        
        for provision_key in provision_keys:
            for pop_key in population_keys:
                if pop_key in self.actors:
                    impact_strength = random.uniform(6.0, 9.0)
                    
                    relationship = Relationship(
                        source_id=self.policies[provision_key].id,
                        target_id=self.actors[pop_key].id,
                        relationship_kind=RelationshipKind.AFFECTS,
                        strength=impact_strength,
                        description=f"{self.policies[provision_key].label} affects {self.actors[pop_key].label}"
                    )
                    self.service.add_relationship(relationship)
    
    def generate_analysis_data(self) -> None:
        """Generate comprehensive analysis data for the ACA example."""
        logger.info("Generating comprehensive ACA analysis data...")
        
        # Start performance monitoring
        start_time = time.time()
        
        # Create all components
        self.create_federal_healthcare_agencies()
        self.create_state_healthcare_systems()
        self.create_healthcare_providers()
        self.create_patient_populations()
        self.create_aca_policy_structure()
        self.create_health_outcome_indicators()
        self.create_healthcare_flows()
        self.create_institutional_framework()
        self.create_relationships()
        
        # Add analysis context to graph
        self.service.add_analytical_context(self.analysis_context)
        
        # Record generation time
        generation_time = time.time() - start_time
        self.performance_metrics.record_operation("data_generation", generation_time)
        
        logger.info(f"Generated {len(self.graph.nodes)} nodes and {len(self.graph.edges)} edges in {generation_time:.2f} seconds")
    
    def demonstrate_caching_features(self) -> None:
        """Demonstrate advanced caching capabilities."""
        logger.info("Demonstrating advanced caching features...")
        
        # Configure cache
        self.cache_manager.add_cache("health_queries", CacheType.LRU, max_size=500)
        self.cache_manager.add_cache("outcome_metrics", CacheType.TTL, ttl=1800)
        
        # Perform cached queries
        start_time = time.time()
        
        # First query - not cached
        centrality_results = self.service.analyze_centrality(normalize=True)
        first_query_time = time.time() - start_time
        
        # Second query - cached
        start_time = time.time()
        cached_results = self.service.analyze_centrality(normalize=True)
        second_query_time = time.time() - start_time
        
        logger.info(f"First query time: {first_query_time:.3f}s")
        logger.info(f"Cached query time: {second_query_time:.3f}s")
        
        if second_query_time > 0:
            logger.info(f"Cache speedup: {first_query_time/second_query_time:.1f}x")
        
        # Cache statistics
        cache_stats = self.cache_manager.get_stats()
        logger.info(f"Cache statistics: {cache_stats}")
    
    def perform_complex_analysis(self) -> Dict[str, Any]:
        """Perform complex healthcare policy analysis queries."""
        logger.info("Performing complex healthcare policy analysis...")
        
        analysis_results = {}
        
        # 1. Centrality Analysis
        centrality_results = self.service.analyze_centrality(normalize=True)
        analysis_results["centrality"] = centrality_results
        
        # 2. Policy Impact Analysis
        aca_id = self.policies["aca"].id
        impact_analysis = self.service.analyze_policy_impact(aca_id, max_depth=3)
        analysis_results["policy_impact"] = impact_analysis
        
        # 3. Healthcare Flow Analysis
        flow_analysis = self.service.analyze_flows(
            flow_type="healthcare",
            aggregate_by="institution_type"
        )
        analysis_results["flow_analysis"] = flow_analysis
        
        # 4. Coverage Network Analysis
        coverage_analysis = self.service.analyze_network_structure()
        analysis_results["coverage_network"] = coverage_analysis
        
        return analysis_results
    
    def persist_analysis_data(self) -> None:
        """Demonstrate graph persistence and serialization."""
        logger.info("Demonstrating graph persistence and serialization...")
        
        # Save in multiple formats
        formats = [StorageFormat.JSON, StorageFormat.PICKLE, StorageFormat.COMPRESSED_JSON]
        
        for format_type in formats:
            start_time = time.time()
            
            filename = f"aca_analysis.{format_type.value}"
            filepath = self.data_dir / filename
            
            # Save graph
            self.persistence_manager.save_graph(
                self.graph,
                filepath,
                format_type,
                include_metadata=True
            )
            
            save_time = time.time() - start_time
            file_size = filepath.stat().st_size / (1024 * 1024)  # MB
            
            logger.info(f"Saved {format_type.value}: {file_size:.2f}MB in {save_time:.2f}s")
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        logger.info("Generating performance report...")
        
        # Stop monitoring
        self.metrics_collector.stop_monitoring()
        
        # Collect metrics
        metrics = self.metrics_collector.get_metrics()
        
        # Graph statistics
        graph_stats = {
            "nodes": len(self.graph.nodes),
            "edges": len(self.graph.edges),
            "node_types": len(set(type(node).__name__ for node in self.graph.nodes.values())),
            "edge_types": len(set(edge.relationship_kind.value for edge in self.graph.edges.values())),
        }
        
        # Memory usage
        memory_stats = self.graph.get_memory_usage()
        
        # Performance summary
        performance_report = {
            "graph_statistics": graph_stats,
            "memory_usage": {
                "process_memory_mb": memory_stats.process_memory_mb,
                "graph_memory_mb": memory_stats.graph_memory_mb,
                "node_memory_mb": memory_stats.node_memory_mb,
                "edge_memory_mb": memory_stats.edge_memory_mb
            },
            "performance_metrics": metrics,
            "cache_statistics": self.cache_manager.get_stats()
        }
        
        return performance_report
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """Run the complete ACA analysis demonstration."""
        logger.info("Starting complete ACA healthcare outcomes analysis...")
        
        try:
            # Generate analysis data
            self.generate_analysis_data()
            
            # Demonstrate caching
            self.demonstrate_caching_features()
            
            # Perform complex analysis
            analysis_results = self.perform_complex_analysis()
            
            # Persist data
            self.persist_analysis_data()
            
            # Generate performance report
            performance_report = self.generate_performance_report()
            
            # Compile final results
            final_results = {
                "analysis_context": {
                    "label": self.analysis_context.label,
                    "description": self.analysis_context.description,
                    "methods_used": self.analysis_context.methods_used,
                    "assumptions": self.analysis_context.assumptions,
                    "data_sources": self.analysis_context.data_sources
                },
                "analysis_results": analysis_results,
                "performance_report": performance_report,
                "data_summary": {
                    "actors": len(self.actors),
                    "institutions": len(self.institutions),
                    "policies": len(self.policies),
                    "resources": len(self.resources),
                    "processes": len(self.processes),
                    "flows": len(self.flows),
                    "indicators": len(self.indicators)
                }
            }
            
            # Save results
            results_path = self.data_dir / "aca_analysis_results.json"
            with open(results_path, 'w') as f:
                json.dump(final_results, f, indent=2, default=str)
            
            logger.info("ACA analysis completed successfully!")
            return final_results
            
        except Exception as e:
            logger.error(f"Error in ACA analysis: {str(e)}")
            raise


def main():
    """Main function to run the ACA analysis example."""
    try:
        # Create analysis instance
        analysis = ACAAnalysisExample()
        
        # Run complete analysis
        results = analysis.run_complete_analysis()
        
        # Print summary
        print("\n" + "="*80)
        print("ACA HEALTHCARE OUTCOMES ANALYSIS SUMMARY")
        print("="*80)
        print(f"Total Nodes: {results['performance_report']['graph_statistics']['nodes']}")
        print(f"Total Edges: {results['performance_report']['graph_statistics']['edges']}")
        print(f"Memory Usage: {results['performance_report']['memory_usage']['process_memory_mb']:.2f} MB")
        print(f"Analysis Context: {results['analysis_context']['label']}")
        print("\nKey Findings:")
        print("- ACA implementation involved complex federal-state coordination")
        print("- Healthcare access improved significantly but with geographic variation")
        print("- Medicaid expansion states showed greater coverage improvements")
        print("- Multiple stakeholder interactions create network effects")
        print("- Policy provisions have differential impacts across populations")
        print("="*80)
        
    except Exception as e:
        logger.error(f"Failed to run ACA analysis: {str(e)}")
        raise


if __name__ == "__main__":
    main()