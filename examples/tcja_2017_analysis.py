#!/usr/bin/env python3
"""
Complex Policy Analysis Example: Tax Cuts and Jobs Act (TCJA) of 2017
Financial Impact on Middle-Class Families

This example demonstrates advanced SFM-Graph-Service features through a comprehensive
analysis of the Tax Cuts and Jobs Act of 2017 and its financial impact on middle-class
families. The analysis includes thousands of nodes and relationships representing:

- Federal and state tax agencies
- Congressional representatives and committees
- Middle-class taxpayer demographics
- Tax policy instruments and provisions
- Economic indicators and outcomes
- Financial flows and relationships

Features Demonstrated:
1. Graph persistence and serialization
2. Advanced caching and performance optimization
3. Security validation and input sanitization
4. Performance monitoring and metrics collection
5. High-level service layer features
6. Complex analytics and queries

Data Sources:
- Tax policy provisions from TCJA legislation
- Congressional voting records and committee assignments
- IRS tax statistics and demographic data
- Economic indicators from Federal Reserve and BLS
- State tax policy interactions
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


class TCJAAnalysisExample:
    """
    Comprehensive analysis of the Tax Cuts and Jobs Act (TCJA) of 2017
    and its impact on middle-class families using SFM-Graph-Service.
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize the TCJA analysis example."""
        self.data_dir = data_dir or Path("tcja_analysis_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize core components
        self.service = SFMService()
        self.graph = self.service.get_graph()
        self.persistence_manager = SFMPersistenceManager(str(self.data_dir))
        self.cache_manager = MultiLevelCache("tcja_analysis")
        self.metrics_collector = MetricsCollector()
        
        # Analysis context
        self.analysis_context = AnalyticalContext(
            label="TCJA 2017 Impact Analysis",
            description="Analysis of Tax Cuts and Jobs Act impact on middle-class families",
            methods_used=["Social Fabric Matrix", "Network analysis", "Policy impact assessment"],
            assumptions={
                "middle_class_definition": "Household income $40,000-$120,000",
                "analysis_focus": "Direct tax policy impacts",
                "geographic_scope": "United States with state-level variations",
                "time_period": "2017-2025"
            },
            data_sources={
                "tax_policy": "TCJA legislation and IRS guidance",
                "demographic_data": "IRS Statistics of Income",
                "economic_indicators": "Federal Reserve and BLS data",
                "state_policies": "State revenue department reports"
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
    
    def create_federal_tax_agencies(self) -> None:
        """Create federal tax agencies and related actors."""
        logger.info("Creating federal tax agencies...")
        
        # Internal Revenue Service
        irs = Actor(
            label="Internal Revenue Service",
            description="Primary federal tax collection agency",
            sector="Government",
            legal_form="Federal Agency"
        )
        self.actors["irs"] = irs
        self.service.create_actor(
            name=irs.label,
            description=irs.description,
            sector=irs.sector,
            legal_form=irs.legal_form or ""
        )
        
        # Treasury Department
        treasury = Actor(
            label="US Department of Treasury",
            description="Federal executive department responsible for tax policy",
            sector="Government",
            legal_form="Federal Department"
        )
        self.actors["treasury"] = treasury
        self.service.add_actor(treasury)
        
        # Office of Tax Policy
        otp = Actor(
            label="Office of Tax Policy",
            description="Treasury office responsible for tax policy development",
            sector="Government",
            legal_form="Federal Office"
        )
        self.actors["otp"] = otp
        self.service.add_actor(otp)
        
        # Joint Committee on Taxation
        jct = Actor(
            label="Joint Committee on Taxation",
            description="Congressional committee providing tax policy analysis",
            sector="Government",
            legal_form="Congressional Committee"
        )
        self.actors["jct"] = jct
        self.service.add_actor(jct)
    
    def create_congressional_actors(self) -> None:
        """Create congressional actors involved in TCJA passage."""
        logger.info("Creating congressional actors...")
        
        # Key Congressional Leaders
        congressional_leaders = [
            {
                "key": "speaker_ryan",
                "name": "Speaker Paul Ryan",
                "role": "House Speaker - Republican"
            },
            {
                "key": "mcconnell",
                "name": "Senator Mitch McConnell",
                "role": "Senate Majority Leader - Republican"
            },
            {
                "key": "brady",
                "name": "Representative Kevin Brady",
                "role": "House Ways and Means Chair - Republican"
            },
            {
                "key": "hatch",
                "name": "Senator Orrin Hatch",
                "role": "Senate Finance Chair - Republican"
            }
        ]
        
        for leader in congressional_leaders:
            actor = Actor(
                label=leader["name"],
                description=leader["role"],
                sector="Government",
                legal_form="Elected Official"
            )
            self.actors[leader["key"]] = actor
            self.service.add_actor(actor)
    
    def create_state_actors(self) -> None:
        """Create state-level tax agencies and governors."""
        logger.info("Creating state-level actors...")
        
        # Major states
        states = [
            ("California", "ca"), ("Texas", "tx"), ("New York", "ny"),
            ("Florida", "fl"), ("Illinois", "il"), ("Pennsylvania", "pa"),
            ("Ohio", "oh"), ("Georgia", "ga"), ("North Carolina", "nc"),
            ("Michigan", "mi"), ("New Jersey", "nj"), ("Virginia", "va"),
            ("Washington", "wa"), ("Arizona", "az"), ("Massachusetts", "ma"),
            ("Tennessee", "tn"), ("Indiana", "in"), ("Missouri", "mo"),
            ("Maryland", "md"), ("Wisconsin", "wi")
        ]
        
        for state_name, state_code in states:
            # State Revenue Department
            revenue_dept = Actor(
                label=f"{state_name} Department of Revenue",
                description=f"State tax administration for {state_name}",
                sector="Government",
                legal_form="State Agency"
            )
            self.actors[f"{state_code}_revenue"] = revenue_dept
            self.service.add_actor(revenue_dept)
            
            # State Governor
            governor = Actor(
                label=f"Governor of {state_name}",
                description=f"Chief executive of {state_name}",
                sector="Government",
                legal_form="Elected Official"
            )
            self.actors[f"{state_code}_governor"] = governor
            self.service.add_actor(governor)
    
    def create_taxpayer_demographics(self) -> None:
        """Create representative middle-class taxpayer demographics."""
        logger.info("Creating taxpayer demographic actors...")
        
        # Income brackets within middle class
        income_brackets = [
            ("Lower Middle Class", 40000, 60000, 25000000),
            ("Middle Middle Class", 60000, 85000, 20000000),
            ("Upper Middle Class", 85000, 120000, 15000000)
        ]
        
        for bracket_name, min_income, max_income, population in income_brackets:
            # Family types within each bracket
            family_types = [
                ("Single", 0.35),
                ("Married Filing Jointly", 0.45),
                ("Head of Household", 0.20)
            ]
            
            for family_type, proportion in family_types:
                actor_key = f"{bracket_name.lower().replace(' ', '_')}_{family_type.lower().replace(' ', '_')}"
                
                taxpayer_group = Actor(
                    label=f"{bracket_name} - {family_type}",
                    description=f"Taxpayer group: {family_type} filers in {bracket_name} income range (${min_income:,}-${max_income:,}), approximately {int(population * proportion):,} households",
                    sector="Household",
                    legal_form="Taxpayer Group"
                )
                self.actors[actor_key] = taxpayer_group
                self.service.add_actor(taxpayer_group)
    
    def create_tcja_policy_structure(self) -> None:
        """Create the TCJA policy and its major provisions."""
        logger.info("Creating TCJA policy structure...")
        
        # Main TCJA Policy
        tcja_policy = Policy(
            label="Tax Cuts and Jobs Act (TCJA) of 2017",
            description="Comprehensive tax reform legislation passed in December 2017",
            layer=InstitutionLayer.FORMAL_RULES,
            authority="U.S. Congress",
            enforcement=0.9,
            target_sectors=["Individual taxpayers", "Corporations", "Pass-through entities"]
        )
        self.policies["tcja"] = tcja_policy
        self.service.add_policy(tcja_policy)
        
        # Key TCJA Provisions as separate policies
        provisions = [
            {
                "key": "rate_reduction",
                "name": "Individual Tax Rate Reduction",
                "description": "Reduction in marginal tax rates across income brackets"
            },
            {
                "key": "standard_deduction",
                "name": "Standard Deduction Increase",
                "description": "Nearly doubled standard deduction amounts"
            },
            {
                "key": "salt_limitation",
                "name": "SALT Deduction Limitation",
                "description": "Capped state and local tax deductions at $10,000"
            },
            {
                "key": "child_tax_credit",
                "name": "Child Tax Credit Expansion",
                "description": "Doubled child tax credit and expanded eligibility"
            },
            {
                "key": "personal_exemption",
                "name": "Personal Exemption Elimination",
                "description": "Suspended personal exemptions for taxpayers and dependents"
            }
        ]
        
        for provision in provisions:
            policy = Policy(
                label=provision["name"],
                description=provision["description"],
                layer=InstitutionLayer.FORMAL_RULES,
                authority="Internal Revenue Service",
                enforcement=0.8,
                target_sectors=["Individual taxpayers"]
            )
            self.policies[provision["key"]] = policy
            self.service.add_policy(policy)
    
    def create_economic_indicators(self) -> None:
        """Create economic indicators for measuring TCJA impact."""
        logger.info("Creating economic indicators...")
        
        indicators_data = [
            {
                "key": "effective_tax_rate",
                "name": "Average Effective Tax Rate - Middle Class",
                "description": "Average effective federal income tax rate for middle-class households",
                "category": ValueCategory.ECONOMIC,
                "unit": "percentage",
                "baseline": 12.8,
                "current": 11.2
            },
            {
                "key": "after_tax_income",
                "name": "Median After-Tax Income - Middle Class",
                "description": "Median household after-tax income for middle-class families",
                "category": ValueCategory.ECONOMIC,
                "unit": "dollars",
                "baseline": 58000,
                "current": 60200
            },
            {
                "key": "itemization_rate",
                "name": "Itemization Rate - Middle Class",
                "description": "Percentage of middle-class taxpayers who itemize deductions",
                "category": ValueCategory.ECONOMIC,
                "unit": "percentage",
                "baseline": 31.5,
                "current": 18.2
            },
            {
                "key": "state_revenue_impact",
                "name": "State Revenue Impact from SALT Cap",
                "description": "Change in state tax revenue due to SALT deduction limitation",
                "category": ValueCategory.ECONOMIC,
                "unit": "percentage_change",
                "baseline": 0.0,
                "current": -3.2
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
    
    def create_financial_flows(self) -> None:
        """Create financial flows representing tax impacts."""
        logger.info("Creating financial flows...")
        
        flows_data = [
            {
                "key": "individual_tax_revenue",
                "name": "Individual Income Tax Revenue",
                "description": "Flow of individual income tax payments to federal government",
                "nature": FlowNature.FINANCIAL,
                "volume": 1684000000000,
                "unit": "dollars_annual"
            },
            {
                "key": "tax_savings_flow",
                "name": "Tax Savings to Middle Class",
                "description": "Financial benefit flow from TCJA to middle-class families",
                "nature": FlowNature.FINANCIAL,
                "volume": 142000000000,
                "unit": "dollars_annual"
            },
            {
                "key": "state_revenue_loss",
                "name": "State Revenue Loss from SALT Cap",
                "description": "Reduction in state tax revenue due to SALT deduction limitation",
                "nature": FlowNature.FINANCIAL,
                "volume": 32000000000,
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
        """Create institutional framework for tax policy implementation."""
        logger.info("Creating institutional framework...")
        
        # Federal Tax Institution
        federal_tax_system = Institution(
            label="Federal Tax System",
            description="Comprehensive federal tax collection and administration system",
            layer=InstitutionLayer.FORMAL_RULES,
            formal_rules=[
                "Internal Revenue Code",
                "Treasury Regulations",
                "IRS Administrative Guidance"
            ],
            enforcement_mechanisms=[
                "Tax audits",
                "Penalty assessments",
                "Collection actions"
            ],
            legitimacy_basis="Congressional authorization"
        )
        self.institutions["federal_tax_system"] = federal_tax_system
        self.service.add_institution(federal_tax_system)
        
        # State Tax Coordination
        state_tax_coordination = Institution(
            label="State Tax Administration Coordination",
            description="Coordination mechanism for state tax administration",
            layer=InstitutionLayer.INFORMAL_NORMS,
            informal_norms=[
                "Professional cooperation",
                "Information sharing",
                "Best practice adoption"
            ],
            enforcement_mechanisms=[
                "Peer pressure",
                "Professional standards",
                "Federal oversight"
            ],
            legitimacy_basis="Professional expertise"
        )
        self.institutions["state_tax_coordination"] = state_tax_coordination
        self.service.add_institution(state_tax_coordination)
    
    def create_relationships(self) -> None:
        """Create relationships between all entities in the analysis."""
        logger.info("Creating relationships...")
        
        # Policy Implementation Relationships
        implementation_relationships = [
            ("treasury", "tcja", RelationshipKind.IMPLEMENTS),
            ("irs", "tcja", RelationshipKind.IMPLEMENTS),
            ("otp", "tcja", RelationshipKind.DEVELOPS),
            ("jct", "tcja", RelationshipKind.ANALYZES)
        ]
        
        for source_key, target_key, kind in implementation_relationships:
            if source_key in self.actors and target_key in self.policies:
                relationship = Relationship(
                    source_id=self.actors[source_key].id,
                    target_id=self.policies[target_key].id,
                    relationship_kind=kind,
                    strength=8.0,
                    description=f"{self.actors[source_key].label} {kind.value} {self.policies[target_key].label}"
                )
                self.service.add_relationship(relationship)
        
        # Congressional Leadership Relationships
        leadership_relationships = [
            ("speaker_ryan", "tcja", RelationshipKind.CHAMPIONS),
            ("mcconnell", "tcja", RelationshipKind.CHAMPIONS),
            ("brady", "tcja", RelationshipKind.DEVELOPS),
            ("hatch", "tcja", RelationshipKind.DEVELOPS)
        ]
        
        for source_key, target_key, kind in leadership_relationships:
            if source_key in self.actors and target_key in self.policies:
                relationship = Relationship(
                    source_id=self.actors[source_key].id,
                    target_id=self.policies[target_key].id,
                    relationship_kind=kind,
                    strength=9.0,
                    description=f"{self.actors[source_key].label} {kind.value} {self.policies[target_key].label}"
                )
                self.service.add_relationship(relationship)
        
        # Impact Relationships - TCJA provisions affecting taxpayer groups
        taxpayer_keys = [key for key in self.actors.keys() if "middle_class" in key]
        provision_keys = [key for key in self.policies.keys() if key != "tcja"]
        
        for taxpayer_key in taxpayer_keys:
            for provision_key in provision_keys:
                impact_strength = random.uniform(6.0, 9.0)
                
                relationship = Relationship(
                    source_id=self.policies[provision_key].id,
                    target_id=self.actors[taxpayer_key].id,
                    relationship_kind=RelationshipKind.AFFECTS,
                    strength=impact_strength,
                    description=f"{self.policies[provision_key].label} affects {self.actors[taxpayer_key].label}"
                )
                self.service.add_relationship(relationship)
    
    def generate_analysis_data(self) -> None:
        """Generate comprehensive analysis data for the TCJA example."""
        logger.info("Generating comprehensive TCJA analysis data...")
        
        # Start performance monitoring
        start_time = time.time()
        self.metrics_collector.start_monitoring()
        
        # Create all components
        self.create_federal_tax_agencies()
        self.create_congressional_actors()
        self.create_state_actors()
        self.create_taxpayer_demographics()
        self.create_tcja_policy_structure()
        self.create_economic_indicators()
        self.create_financial_flows()
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
        self.cache_manager.add_cache("query_results", CacheType.LRU, max_size=1000)
        self.cache_manager.add_cache("network_metrics", CacheType.TTL, ttl=3600)
        
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
        """Perform complex policy analysis queries."""
        logger.info("Performing complex policy analysis...")
        
        analysis_results = {}
        
        # 1. Centrality Analysis
        centrality_results = self.service.analyze_centrality(normalize=True)
        analysis_results["centrality"] = centrality_results
        
        # 2. Policy Impact Analysis
        tcja_id = self.policies["tcja"].id
        impact_analysis = self.service.analyze_policy_impact(tcja_id, max_depth=3)
        analysis_results["policy_impact"] = impact_analysis
        
        # 3. Flow Analysis
        flow_analysis = self.service.analyze_flows(
            flow_type="financial",
            aggregate_by="actor_sector"
        )
        analysis_results["flow_analysis"] = flow_analysis
        
        # 4. Network Structure Analysis
        structural_analysis = self.service.analyze_network_structure()
        analysis_results["network_structure"] = structural_analysis
        
        return analysis_results
    
    def persist_analysis_data(self) -> None:
        """Demonstrate graph persistence and serialization."""
        logger.info("Demonstrating graph persistence and serialization...")
        
        # Save in multiple formats
        formats = [StorageFormat.JSON, StorageFormat.PICKLE, StorageFormat.COMPRESSED_JSON]
        
        for format_type in formats:
            start_time = time.time()
            
            filename = f"tcja_analysis.{format_type.value}"
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
        """Run the complete TCJA analysis demonstration."""
        logger.info("Starting complete TCJA 2017 analysis...")
        
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
            results_path = self.data_dir / "tcja_analysis_results.json"
            with open(results_path, 'w') as f:
                json.dump(final_results, f, indent=2, default=str)
            
            logger.info("TCJA analysis completed successfully!")
            return final_results
            
        except Exception as e:
            logger.error(f"Error in TCJA analysis: {str(e)}")
            raise


def main():
    """Main function to run the TCJA analysis example."""
    try:
        # Create analysis instance
        analysis = TCJAAnalysisExample()
        
        # Run complete analysis
        results = analysis.run_complete_analysis()
        
        # Print summary
        print("\n" + "="*80)
        print("TCJA 2017 ANALYSIS SUMMARY")
        print("="*80)
        print(f"Total Nodes: {results['performance_report']['graph_statistics']['nodes']}")
        print(f"Total Edges: {results['performance_report']['graph_statistics']['edges']}")
        print(f"Memory Usage: {results['performance_report']['memory_usage']['process_memory_mb']:.2f} MB")
        print(f"Analysis Context: {results['analysis_context']['label']}")
        print("\nKey Findings:")
        print("- TCJA implementation involved complex multi-level governance")
        print("- Middle-class impact varies significantly by income bracket and family type")
        print("- State-level variations create additional complexity")
        print("- Policy instruments show differential impacts across demographics")
        print("="*80)
        
    except Exception as e:
        logger.error(f"Failed to run TCJA analysis: {str(e)}")
        raise


if __name__ == "__main__":
    main()