"""
Performance benchmark demonstration.

This script demonstrates the performance improvements made to SFMGraph
by comparing lookup times with different graph sizes.
"""

import time
import uuid
from typing import List
from core.graph import SFMGraph
from core.core_nodes import Actor
from core.relationships import Relationship


def benchmark_node_lookups(graph: SFMGraph, nodes: List[Actor], num_lookups: int = 1000) -> float:
    """Benchmark node lookup performance."""
    start_time = time.time()
    
    for i in range(num_lookups):
        # Lookup nodes at various positions
        node_idx = i % len(nodes)
        found_node = graph._find_node_by_id(nodes[node_idx].id)
        assert found_node is not None
    
    return time.time() - start_time


def benchmark_relationship_caching(graph: SFMGraph, nodes: List[Actor]) -> tuple:
    """Benchmark relationship caching performance."""
    # Create relationships
    for i in range(0, min(len(nodes) - 1, 100)):
        rel = Relationship(
            source_id=nodes[i].id,
            target_id=nodes[i + 1].id,
            kind="AFFECTS"
        )
        graph.add_relationship(rel)
    
    # First access (cache miss)
    test_node_id = nodes[0].id
    start_time = time.time()
    rels_first = graph.get_node_relationships(test_node_id)
    first_access_time = time.time() - start_time
    
    # Second access (cache hit)
    start_time = time.time()
    rels_second = graph.get_node_relationships(test_node_id)
    second_access_time = time.time() - start_time
    
    return first_access_time, second_access_time


def run_benchmark():
    """Run comprehensive performance benchmark."""
    print("SFMGraph Performance Benchmark")
    print("=" * 50)
    
    # Test with different graph sizes
    sizes = [100, 500, 1000, 2000]
    
    for size in sizes:
        print(f"\nTesting with {size} nodes:")
        print("-" * 30)
        
        # Create graph and nodes
        graph = SFMGraph()
        nodes = []
        
        # Time graph construction
        start_time = time.time()
        for i in range(size):
            actor = Actor(label=f"Actor_{i}")
            nodes.append(actor)
            graph.add_node(actor)
        construction_time = time.time() - start_time
        
        print(f"Graph construction: {construction_time:.4f}s ({size/construction_time:.0f} nodes/sec)")
        
        # Benchmark lookups
        lookup_time = benchmark_node_lookups(graph, nodes, 1000)
        print(f"1000 node lookups: {lookup_time:.4f}s ({1000/lookup_time:.0f} lookups/sec)")
        
        # Test single lookup performance
        start_time = time.time()
        found_node = graph._find_node_by_id(nodes[size//2].id)
        single_lookup_time = time.time() - start_time
        print(f"Single lookup: {single_lookup_time*1000:.4f}ms")
        
        # Test relationship caching (for smaller graphs)
        if size <= 1000:
            first_time, second_time = benchmark_relationship_caching(graph, nodes)
            speedup = first_time / second_time if second_time > 0 else float('inf')
            print(f"Relationship cache - First: {first_time*1000:.4f}ms, Second: {second_time*1000:.4f}ms")
            print(f"Cache speedup: {speedup:.1f}x")
        
        # Memory usage info
        print(f"Nodes in index: {len(graph._node_index)}")
        print(f"Cache entries: {len(graph._relationship_cache)}")


if __name__ == "__main__":
    run_benchmark()