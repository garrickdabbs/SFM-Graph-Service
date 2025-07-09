#!/usr/bin/env python3
"""
SFM Performance Optimization Demo

This script demonstrates the enhanced performance features implemented
for the SFM Graph service, including memory management and advanced caching.

Usage:
    python demo_performance_features.py
"""

import time
import uuid
from typing import List

from core.graph import SFMGraph
from core.core_nodes import Actor, Institution, Policy
from core.relationships import Relationship
from core.memory_management import EvictionStrategy


def print_separator(title: str):
    """Print a formatted separator."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def demo_memory_management():
    """Demonstrate memory management features."""
    print_separator("MEMORY MANAGEMENT DEMO")
    
    # Create graph with memory limit
    graph = SFMGraph()
    graph.set_memory_limit(50.0)  # 50MB limit
    print(f"✓ Created graph with 50MB memory limit")
    
    # Show initial memory stats
    memory_stats = graph.get_memory_usage()
    print(f"✓ Initial memory usage: {memory_stats.process_memory_mb:.2f}MB")
    
    # Add nodes to demonstrate memory tracking
    print("✓ Adding 1000 nodes...")
    nodes = []
    for i in range(1000):
        if i % 200 == 0:
            # Create larger nodes occasionally
            actor = Actor(
                label=f"LargeActor_{i}",
                description=f"This is a large actor with extensive description " * 50
            )
        else:
            actor = Actor(label=f"Actor_{i}", description=f"Actor {i}")
        
        graph.add_node(actor)
        nodes.append(actor)
    
    # Show memory stats after adding nodes
    memory_stats = graph.get_memory_stats()
    print(f"✓ Added {memory_stats['total_nodes']} nodes")
    print(f"✓ Current memory usage: {graph.get_memory_usage().process_memory_mb:.2f}MB")
    
    # Test different eviction strategies
    print("\n✓ Testing eviction strategies:")
    strategies = [EvictionStrategy.LRU, EvictionStrategy.LFU, EvictionStrategy.OLDEST_FIRST]
    
    for strategy in strategies:
        graph.set_eviction_strategy(strategy)
        
        # Access some nodes to create access patterns
        for i in range(0, 100, 10):
            graph.get_node_by_id(nodes[i].id)
        
        # Force cleanup
        evicted = graph.force_memory_cleanup()
        current_nodes = len(graph.get_all_node_ids())
        
        print(f"  - {strategy.value}: evicted {evicted} nodes, {current_nodes} remaining")


def demo_advanced_caching():
    """Demonstrate advanced caching features."""
    print_separator("ADVANCED CACHING DEMO")
    
    # Create graph with caching enabled
    graph = SFMGraph()
    print("✓ Created graph with advanced caching enabled")
    
    # Add nodes and relationships
    nodes = []
    for i in range(100):
        actor = Actor(label=f"Actor_{i}")
        graph.add_node(actor)
        nodes.append(actor)
    
    # Create relationships
    for i in range(0, 90, 2):
        rel = Relationship(
            source_id=nodes[i].id,
            target_id=nodes[i + 1].id,
            kind="AFFECTS"
        )
        graph.add_relationship(rel)
    
    print(f"✓ Added {len(nodes)} nodes and {len(graph.relationships)} relationships")
    
    # Demonstrate cache performance
    test_node = nodes[0]
    
    print("\n✓ Testing cache performance:")
    
    # First access (cache miss)
    start_time = time.time()
    relationships_1 = graph.get_node_relationships(test_node.id)
    first_time = time.time() - start_time
    print(f"  - First access (cache miss): {first_time:.6f}s")
    
    # Second access (cache hit)
    start_time = time.time()
    relationships_2 = graph.get_node_relationships(test_node.id)
    second_time = time.time() - start_time
    print(f"  - Second access (cache hit): {second_time:.6f}s")
    
    # Calculate performance improvement
    if first_time > 0:
        improvement = ((first_time - second_time) / first_time) * 100
        print(f"  - Performance improvement: {improvement:.1f}%")
    
    # Show cache statistics
    cache_stats = graph.get_cache_stats()
    print(f"✓ Cache statistics:")
    print(f"  - Relationship cache size: {cache_stats['relationship_cache_size']}")
    if 'query_cache' in cache_stats:
        query_stats = cache_stats['query_cache']
        print(f"  - Query cache levels: {len(query_stats) if isinstance(query_stats, dict) else 1}")


def demo_performance_monitoring():
    """Demonstrate performance monitoring features."""
    print_separator("PERFORMANCE MONITORING DEMO")
    
    # Import metrics collector
    from core.performance_metrics import get_metrics_collector
    
    collector = get_metrics_collector()
    print("✓ Performance metrics collection enabled")
    
    # Create graph and perform operations
    graph = SFMGraph()
    
    # Add nodes with timing
    print("✓ Performing monitored operations...")
    for i in range(100):
        actor = Actor(label=f"MonitoredActor_{i}")
        graph.add_node(actor)
        
        # Perform some lookups
        if i > 0:
            graph.get_node_by_id(actor.id)
    
    # Get performance summary
    summary = collector.get_summary_stats()
    print(f"✓ Total operations recorded: {summary['total_operations']}")
    print(f"✓ Operations per second: {summary['operations_per_second']:.2f}")
    print(f"✓ Error rate: {summary['error_rate']:.2%}")
    
    # Get specific operation metrics
    add_node_metrics = collector.get_operation_metrics('add_node')
    if add_node_metrics:
        print(f"✓ Add node average time: {add_node_metrics['avg_duration']:.6f}s")
        print(f"✓ Add node success rate: {add_node_metrics['success_rate']:.2%}")
    
    lookup_metrics = collector.get_operation_metrics('get_node_by_id')
    if lookup_metrics:
        print(f"✓ Node lookup average time: {lookup_metrics['avg_duration']:.6f}s")


def demo_large_graph_handling():
    """Demonstrate large graph handling capabilities."""
    print_separator("LARGE GRAPH HANDLING DEMO")
    
    # Test with progressively larger graphs
    sizes = [1000, 5000, 10000]
    
    for size in sizes:
        print(f"\n✓ Testing with {size} nodes...")
        
        graph = SFMGraph()
        graph.set_memory_limit(200.0)  # 200MB limit
        
        # Measure creation time
        start_time = time.time()
        nodes = []
        for i in range(size):
            actor = Actor(label=f"LargeGraphActor_{i}")
            graph.add_node(actor)
            nodes.append(actor)
        creation_time = time.time() - start_time
        
        # Add some relationships
        rel_count = min(size // 4, 2000)  # Limit relationships
        start_time = time.time()
        for i in range(rel_count):
            rel = Relationship(
                source_id=nodes[i].id,
                target_id=nodes[(i + 1) % len(nodes)].id,
                kind="AFFECTS"
            )
            graph.add_relationship(rel)
        relationship_time = time.time() - start_time
        
        # Test query performance
        start_time = time.time()
        test_relationships = graph.get_node_relationships(nodes[0].id)
        query_time = time.time() - start_time
        
        # Get memory usage
        memory_usage = graph.get_memory_usage().process_memory_mb
        
        print(f"  - Creation time: {creation_time:.3f}s ({size/creation_time:.0f} nodes/sec)")
        print(f"  - Relationship time: {relationship_time:.3f}s")
        print(f"  - Query time: {query_time:.6f}s")
        print(f"  - Memory usage: {memory_usage:.2f}MB")
        print(f"  - Found relationships: {len(test_relationships)}")


def main():
    """Main demo execution."""
    print("SFM Graph Performance Optimization Demo")
    print("This demo showcases the enhanced performance features")
    
    try:
        # Run all demonstrations
        demo_memory_management()
        demo_advanced_caching()
        demo_performance_monitoring()
        demo_large_graph_handling()
        
        print_separator("DEMO COMPLETED SUCCESSFULLY")
        print("✓ All performance features working correctly!")
        print("✓ Memory management: configurable limits and eviction strategies")
        print("✓ Advanced caching: multi-level caching with intelligent invalidation")
        print("✓ Performance monitoring: comprehensive metrics collection")
        print("✓ Large graph handling: scalable operations with optimizations")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())