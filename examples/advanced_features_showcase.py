#!/usr/bin/env python3
"""
Advanced SFM Features Showcase Example

This example demonstrates advanced capabilities of the SFM framework that go beyond
basic entity modeling, including:

- Graph persistence and serialization capabilities
- Advanced caching and performance optimization features  
- Security validation and input sanitization
- Memory management and performance monitoring
- Service layer features with health monitoring
- Query engine optimization and metrics

The example models a financial system to demonstrate these technical capabilities
in a realistic domain context.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add the workspace root to Python path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

from core.sfm_models import (
    Actor, Institution, Resource, Policy, Flow, Relationship, SFMGraph
)
from core.sfm_enums import RelationshipKind, ResourceType, FlowNature, FlowType
from core.sfm_query import SFMQueryFactory
from core.sfm_service import SFMService, SFMServiceConfig
from core.sfm_persistence import SFMPersistenceManager, StorageFormat
from core.advanced_caching import MultiLevelCache
from core.performance_metrics import PerformanceMetrics
from core.security_validators import sanitize_string, validate_metadata
from db.sfm_dao import NetworkXSFMRepository


def create_financial_system_graph(repo: NetworkXSFMRepository, graph: SFMGraph):
    """
    Create a financial system model to demonstrate advanced SFM features.
    """
    
    # Financial institutions
    central_bank = Actor(
        label="Central Bank",
        sector="Government",
        description="National monetary authority"
    )
    
    commercial_bank = Actor(
        label="Commercial Bank",
        sector="Finance",
        description="Private lending institution"
    )
    
    investment_firm = Actor(
        label="Investment Management Firm", 
        sector="Finance",
        description="Asset management and investment services"
    )
    
    regulatory_agency = Actor(
        label="Financial Regulatory Agency",
        sector="Government",
        description="Financial system oversight and regulation"
    )
    
    # Institutions and frameworks
    monetary_system = Institution(
        label="Monetary Policy Framework",
        description="Institutional framework for monetary policy implementation"
    )
    
    banking_regulation = Institution(
        label="Banking Regulatory Framework",
        description="Rules and oversight for banking operations"
    )
    
    # Financial resources
    money_supply = Resource(
        label="National Money Supply",
        rtype=ResourceType.FINANCIAL,
        description="Total money in circulation",
        unit="billions USD"
    )
    
    credit = Resource(
        label="Bank Credit",
        rtype=ResourceType.FINANCIAL,
        description="Lending capacity of banking system",
        unit="billions USD"
    )
    
    investment_capital = Resource(
        label="Investment Capital",
        rtype=ResourceType.FINANCIAL,
        description="Capital available for investments",
        unit="billions USD"
    )
    
    financial_data = Resource(
        label="Financial Market Data",
        rtype=ResourceType.INFORMATION,
        description="Real-time financial market information",
        unit="data feeds"
    )
    
    # Policies
    monetary_policy = Policy(
        label="Monetary Policy",
        authority="Central Bank",
        description="Interest rate and money supply management"
    )
    
    banking_supervision = Policy(
        label="Banking Supervision Policy",
        authority="Financial Regulatory Agency", 
        description="Oversight and regulation of banking activities"
    )
    
    # Flows
    money_creation = Flow(
        label="Money Creation Process",
        nature=FlowNature.OUTPUT,
        flow_type=FlowType.FINANCIAL,
        description="Process of creating new money through lending"
    )
    
    credit_flow = Flow(
        label="Credit Allocation Flow",
        nature=FlowNature.TRANSFER,
        flow_type=FlowType.FINANCIAL,
        description="Flow of credit from banks to borrowers"
    )
    
    investment_flow = Flow(
        label="Investment Capital Flow",
        nature=FlowNature.TRANSFER,
        flow_type=FlowType.FINANCIAL,
        description="Flow of capital to investment opportunities"
    )
    
    information_flow = Flow(
        label="Financial Information Flow",
        nature=FlowNature.INFORMATION,
        flow_type=FlowType.INFORMATION,
        description="Distribution of financial market information"
    )
    
    # Add all entities
    entities = [
        central_bank, commercial_bank, investment_firm, regulatory_agency,
        monetary_system, banking_regulation,
        money_supply, credit, investment_capital, financial_data,
        monetary_policy, banking_supervision,
        money_creation, credit_flow, investment_flow, information_flow
    ]
    
    for entity in entities:
        repo.create_node(entity)
        graph.add_node(entity)
    
    # Create relationships
    relationships = [
        # Institutional relationships
        Relationship(source_id=central_bank.id, target_id=monetary_system.id, kind=RelationshipKind.IMPLEMENTS, weight=0.95),
        Relationship(source_id=regulatory_agency.id, target_id=banking_regulation.id, kind=RelationshipKind.IMPLEMENTS, weight=0.90),
        
        # Resource management
        Relationship(source_id=central_bank.id, target_id=money_supply.id, kind=RelationshipKind.MANAGES, weight=0.95),
        Relationship(source_id=commercial_bank.id, target_id=credit.id, kind=RelationshipKind.MANAGES, weight=0.85),
        Relationship(source_id=investment_firm.id, target_id=investment_capital.id, kind=RelationshipKind.MANAGES, weight=0.80),
        
        # Policy implementation
        Relationship(source_id=central_bank.id, target_id=monetary_policy.id, kind=RelationshipKind.IMPLEMENTS, weight=0.95),
        Relationship(source_id=regulatory_agency.id, target_id=banking_supervision.id, kind=RelationshipKind.IMPLEMENTS, weight=0.90),
        
        # Flow relationships
        Relationship(source_id=money_supply.id, target_id=money_creation.id, kind=RelationshipKind.ENABLES, weight=0.90),
        Relationship(source_id=credit.id, target_id=credit_flow.id, kind=RelationshipKind.ENABLES, weight=0.85),
        Relationship(source_id=investment_capital.id, target_id=investment_flow.id, kind=RelationshipKind.ENABLES, weight=0.80),
        Relationship(source_id=financial_data.id, target_id=information_flow.id, kind=RelationshipKind.ENABLES, weight=0.85),
        
        # Regulatory relationships
        Relationship(source_id=regulatory_agency.id, target_id=commercial_bank.id, kind=RelationshipKind.REGULATES, weight=0.85),
        Relationship(source_id=regulatory_agency.id, target_id=investment_firm.id, kind=RelationshipKind.REGULATES, weight=0.75),
        
        # Information relationships
        Relationship(source_id=commercial_bank.id, target_id=financial_data.id, kind=RelationshipKind.USES, weight=0.70),
        Relationship(source_id=investment_firm.id, target_id=financial_data.id, kind=RelationshipKind.USES, weight=0.85),
        
        # Economic relationships
        Relationship(source_id=monetary_policy.id, target_id=money_supply.id, kind=RelationshipKind.AFFECTS, weight=0.90),
        Relationship(source_id=monetary_policy.id, target_id=credit.id, kind=RelationshipKind.AFFECTS, weight=0.75)
    ]
    
    for rel in relationships:
        repo.create_relationship(rel)
        graph.add_relationship(rel)
    
    repo.save_graph(graph)
    return graph


def demonstrate_persistence_features(graph: SFMGraph):
    """Demonstrate graph persistence and serialization capabilities."""
    print("-" * 60)
    print("PERSISTENCE AND SERIALIZATION FEATURES")
    print("-" * 60)
    print()
    
    try:
        # Create persistence manager
        persistence_manager = SFMPersistenceManager()
        
        # Create temporary directory for demo
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Save graph in different formats
            json_file = temp_path / "financial_system.json"
            pickle_file = temp_path / "financial_system.pkl"
            
            print("💾 Graph Serialization:")
            
            # Save as JSON
            persistence_manager.save_graph(graph, json_file, StorageFormat.JSON)
            json_size = json_file.stat().st_size
            print(f"  • JSON format: {json_size:,} bytes")
            
            # Save as Pickle  
            persistence_manager.save_graph(graph, pickle_file, StorageFormat.PICKLE)
            pickle_size = pickle_file.stat().st_size
            print(f"  • Pickle format: {pickle_size:,} bytes")
            
            # Load and verify
            loaded_graph = persistence_manager.load_graph(json_file, StorageFormat.JSON)
            print(f"  • Loaded graph: {len(loaded_graph)} entities, {len(loaded_graph.relationships)} relationships")
            
            # Create incremental backup
            backup_file = temp_path / "backup.json"
            persistence_manager.create_backup(graph, backup_file)
            backup_size = backup_file.stat().st_size
            print(f"  • Backup created: {backup_size:,} bytes")
            
            print("✓ Persistence operations completed successfully")
            
    except Exception as e:
        print(f"⚠️ Persistence demo error: {e}")
    
    print()


def demonstrate_caching_features():
    """Demonstrate advanced caching capabilities."""
    print("-" * 60)
    print("ADVANCED CACHING FEATURES")
    print("-" * 60)
    print()
    
    try:
        # Create multi-level cache
        cache = MultiLevelCache()
        
        print("🚀 Cache Configuration:")
        print(f"  • Multi-level caching system initialized")
        print(f"  • Memory and TTL cache layers available")
        
        # Simulate cache operations
        test_key = "centrality_analysis"
        test_data = {"centrality": {"node1": 0.85, "node2": 0.72}}
        
        # Store data in cache
        cache.set(test_key, test_data)
        print(f"  • Cached analysis result for key: {test_key}")
        
        # Retrieve from cache
        cached_result = cache.get(test_key)
        if cached_result:
            print("  • Cache hit successful - data retrieved")
        else:
            print("  • Cache miss")
        
        # Get cache statistics
        stats = cache.get_stats()
        print(f"  • Cache Statistics: hits={stats.hits}, misses={stats.misses}")
        
        print("✓ Caching system operational")
        
    except Exception as e:
        print(f"⚠️ Caching demo error: {e}")
    
    print()


def demonstrate_security_features():
    """Demonstrate security validation capabilities."""
    print("-" * 60)
    print("SECURITY VALIDATION FEATURES")
    print("-" * 60)
    print()
    
    try:
        # Test input sanitization
        print("🔒 Input Security Validation:")
        
        # Test safe input
        safe_input = "Financial System Analysis"
        sanitized = sanitize_string(safe_input)
        print(f"  • Safe input: '{safe_input}' → '{sanitized}'")
        
        # Test potentially dangerous input
        dangerous_input = "<script>alert('xss')</script>Banking Data"
        sanitized_dangerous = sanitize_string(dangerous_input)
        print(f"  • Dangerous input sanitized: '{sanitized_dangerous}'")
        
        # Test metadata validation
        metadata = {"source": "central_bank_data", "type": "financial"}
        try:
            validate_metadata(metadata)
            print(f"  • Metadata validation: ✓ Valid ({len(metadata)} fields)")
        except Exception as e:
            print(f"  • Metadata validation: ✗ Error - {e}")
        
        # Test invalid metadata
        invalid_metadata = {"x" * 100: "value"}  # Very long key
        try:
            validate_metadata(invalid_metadata)
            print(f"  • Invalid metadata: ✓ Passed (unexpected)")
        except Exception as e:
            print(f"  • Invalid metadata: ✗ Caught as expected")
        
        print("✓ Security validation operational")
        
    except Exception as e:
        print(f"⚠️ Security demo error: {e}")
    
    print()


def demonstrate_performance_monitoring():
    """Demonstrate performance monitoring capabilities."""
    print("-" * 60)
    print("PERFORMANCE MONITORING FEATURES")
    print("-" * 60)
    print()
    
    try:
        # Create performance metrics collector
        perf_metrics = PerformanceMetrics()
        
        print("📊 Performance Monitoring:")
        
        # Start operation timing
        with perf_metrics.time_operation("graph_analysis"):
            # Simulate graph analysis work
            import time
            time.sleep(0.1)  # Simulate processing time
        
        # Record custom metrics
        perf_metrics.record_metric("entities_processed", 16)
        perf_metrics.record_metric("relationships_analyzed", 17)
        perf_metrics.record_metric("cache_hit_rate", 0.85)
        
        # Get performance summary
        summary = perf_metrics.get_performance_summary()
        
        print(f"  • Operations timed: {len(summary.get('operation_times', {}))}")
        print(f"  • Custom metrics: {len(summary.get('custom_metrics', {}))}")
        
        # Show recent operation times
        times = summary.get('operation_times', {})
        if 'graph_analysis' in times:
            avg_time = sum(times['graph_analysis']) / len(times['graph_analysis'])
            print(f"  • Graph analysis avg time: {avg_time:.3f} seconds")
        
        # Show custom metrics
        metrics = summary.get('custom_metrics', {})
        if metrics:
            print(f"  • Entities processed: {metrics.get('entities_processed', [])[0] if metrics.get('entities_processed') else 'N/A'}")
            print(f"  • Cache hit rate: {metrics.get('cache_hit_rate', [])[0] if metrics.get('cache_hit_rate') else 'N/A'}")
        
        print("✓ Performance monitoring active")
        
    except Exception as e:
        print(f"⚠️ Performance monitoring demo error: {e}")
    
    print()


def demonstrate_service_layer_features(graph: SFMGraph):
    """Demonstrate high-level service layer capabilities."""
    print("-" * 60)
    print("SERVICE LAYER FEATURES")
    print("-" * 60)
    print()
    
    try:
        # Create service with advanced configuration
        config = SFMServiceConfig(
            storage_backend="networkx",
            enable_validation=True,
            enable_caching=True,
            cache_ttl_seconds=300,
            enable_performance_monitoring=True
        )
        
        service = SFMService(config)
        
        print("⚙️ Service Configuration:")
        print(f"  • Storage Backend: {config.storage_backend}")
        print(f"  • Validation Enabled: {config.enable_validation}")
        print(f"  • Caching Enabled: {config.enable_caching}")
        print(f"  • Performance Monitoring: {config.enable_performance_monitoring}")
        
        # Load existing graph into service
        service.load_graph(graph)
        
        # Get service health
        health = service.get_service_health()
        print(f"\n🏥 Service Health:")
        print(f"  • Status: {health.get('status', 'unknown')}")
        print(f"  • Graph entities: {health.get('graph_size', 0)}")
        print(f"  • Memory usage: {health.get('memory_usage', 'unknown')}")
        
        # Get network statistics through service
        stats = service.get_network_statistics()
        print(f"\n📈 Network Statistics:")
        print(f"  • Total nodes: {stats.get('total_nodes', 0)}")
        print(f"  • Total relationships: {stats.get('total_relationships', 0)}")
        print(f"  • Network density: {stats.get('density', 0):.3f}")
        
        # Find most influential actors using service
        influential = service.find_most_influential_actors(limit=3)
        print(f"\n🎯 Most Influential Actors:")
        for actor_info in influential[:3]:
            print(f"  • {actor_info.get('label', 'Unknown')}: {actor_info.get('centrality', 0):.3f}")
        
        print("\n✓ Service layer operational")
        
    except Exception as e:
        print(f"⚠️ Service layer demo error: {e}")
    
    print()


if __name__ == "__main__":
    """
    Advanced SFM Features Showcase
    
    This example demonstrates the technical infrastructure and advanced
    capabilities that support sophisticated SFM modeling and analysis.
    """
    
    print("=" * 80)
    print("ADVANCED SFM FEATURES SHOWCASE")
    print("=" * 80)
    print()
    print("This example demonstrates advanced technical capabilities:")
    print("• Graph persistence and serialization")
    print("• Advanced caching and performance optimization")
    print("• Security validation and input sanitization")
    print("• Performance monitoring and metrics collection")
    print("• High-level service layer features")
    print()
    
    # Create example financial system
    repo = NetworkXSFMRepository()
    graph = SFMGraph(
        name="Financial System - Advanced Features Demo",
        description="Financial system model for demonstrating advanced SFM capabilities"
    )
    repo.save_graph(graph)
    
    print("Creating financial system model...")
    financial_graph = create_financial_system_graph(repo, graph)
    
    print(f"✓ Financial system created: {len(financial_graph)} entities, {len(financial_graph.relationships)} relationships")
    print()
    
    # Demonstrate advanced features
    demonstrate_persistence_features(financial_graph)
    demonstrate_caching_features()
    demonstrate_security_features()
    demonstrate_performance_monitoring()
    demonstrate_service_layer_features(financial_graph)
    
    print("=" * 80)
    print("ADVANCED FEATURES SHOWCASE COMPLETE")
    print("=" * 80)
    print()
    print("Advanced capabilities demonstrated:")
    print("✓ Graph persistence with multiple serialization formats")
    print("✓ Multi-level caching with configurable policies")
    print("✓ Comprehensive security validation and sanitization")
    print("✓ Performance monitoring and metrics collection")
    print("✓ High-level service layer with health monitoring")
    print("✓ Enterprise-ready infrastructure for production systems")
    print()
    print("These features enable the SFM framework to scale from research")
    print("prototypes to production-grade policy analysis systems.")
    
    # Cleanup
    financial_graph.clear()
    repo.clear()
    print("\nGraph and repository cleared.")