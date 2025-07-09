# SFMGraph Performance Optimizations

This document describes the performance optimizations implemented in the SFMGraph class to address scalability issues with large datasets.

## Background

The original SFMGraph implementation had several performance bottlenecks:

1. **O(n) node lookups**: The `_find_node_by_id` method iterated through all nodes in the graph
2. **No relationship caching**: Repeated relationship queries were recalculated each time
3. **Memory inefficiency**: No optimization for frequently instantiated classes
4. **No lazy loading**: All nodes were loaded immediately

## Implemented Optimizations

### 1. Central Node Index (O(1) Lookups)

**Problem**: Original `_find_node_by_id` had O(n) complexity
```python
# Old implementation - O(n)
def _find_node_by_id(self, node_id: uuid.UUID) -> Optional[Node]:
    for node in self:  # Iterates through ALL nodes
        if node.id == node_id:
            return node
    return None
```

**Solution**: Added central index for O(1) lookups
```python
# New implementation - O(1)
_node_index: Dict[uuid.UUID, Node] = field(default_factory=lambda: {}, init=False)

def _find_node_by_id(self, node_id: uuid.UUID) -> Optional[Node]:
    return self._node_index.get(node_id)  # O(1) dictionary lookup
```

**Performance Impact**: 
- Single lookup: ~0.001-0.002ms (vs. increasing with graph size)
- Lookup throughput: 3-4 million lookups/second

### 2. Relationship Caching

**Problem**: Repeated relationship queries were expensive
**Solution**: Added LRU-style cache with automatic invalidation

```python
_relationship_cache: Dict[uuid.UUID, List[Relationship]] = field(default_factory=lambda: {}, init=False)

def get_node_relationships(self, node_id: uuid.UUID) -> List[Relationship]:
    # Check cache first
    if node_id in self._relationship_cache:
        return self._relationship_cache[node_id]
    # ... compute and cache result
```

**Performance Impact**: 
- 25-35x speedup for repeated relationship access
- Automatic cache invalidation when relationships change
- Configurable cache size (default: 1000 entries)

### 3. Lazy Loading Support

**Problem**: Large graphs required loading all nodes into memory
**Solution**: Optional lazy loading mechanism

```python
def enable_lazy_loading(self, node_loader: Callable[[uuid.UUID], Optional[Node]]) -> None:
    """Enable lazy loading with a custom node loader function."""
    self._lazy_loading_enabled = True
    self._node_loader = node_loader
```

**Benefits**:
- Load nodes on-demand for large datasets
- Reduces initial memory footprint
- Configurable with custom loader functions
- **Robust error handling**: Failed loads are logged with warnings
- **Exception safety**: Loader exceptions don't crash the graph operations

## Usage Examples

### Basic Usage (Automatic)
```python
# Optimizations are enabled automatically
graph = SFMGraph()
actor = Actor("Test Actor")
graph.add_node(actor)

# Fast O(1) lookup
found = graph._find_node_by_id(actor.id)

# Cached relationship access
relationships = graph.get_node_relationships(actor.id)
```

### Lazy Loading
```python
graph = SFMGraph()

# Define a loader function
def load_from_database(node_id: uuid.UUID) -> Optional[Node]:
    # Your custom loading logic here
    return database.load_node(node_id)

# Enable lazy loading
graph.enable_lazy_loading(load_from_database)

# Nodes will be loaded on-demand
node = graph._find_node_by_id(some_id)  # May trigger loading
```

### Robust Lazy Loading with Error Handling
```python
import logging

# Set up logging to see warnings
logging.basicConfig(level=logging.WARNING)

graph = SFMGraph()

# Define a robust loader function with potential error scenarios
def robust_database_loader(node_id: uuid.UUID) -> Optional[Node]:
    try:
        # Your database connection and loading logic
        return database.load_node(node_id)
    except DatabaseConnectionError:
        # Let the SFMGraph handle the exception and logging
        raise  # Re-raise to be caught by SFMGraph's error handling

# Enable lazy loading
graph.enable_lazy_loading(robust_database_loader)

# Failed loads will be logged automatically
node = graph.get_node_by_id(some_id)  # Returns None if loading fails
```

## Performance Benchmarks

Run the performance benchmark to see improvements:

```bash
python performance_benchmark.py
```

Sample results:
- **Graph construction**: ~200,000 nodes/second
- **Node lookups**: 3-4 million lookups/second  
- **Single lookup**: <0.002ms regardless of graph size
- **Relationship cache**: 25-35x speedup for repeated access

## Testing

Performance optimizations are thoroughly tested:

```bash
# Run performance-specific tests
python -m pytest tests/test_performance_optimizations.py -v

# Run all performance tests
python -m pytest tests/test_lookup_performance.py tests/test_sfm_models_ext.py::PerformanceTestCase tests/test_performance_optimizations.py -v
```

## Compatibility

All optimizations are backwards compatible:
- Existing code continues to work unchanged
- All original tests pass
- New features are opt-in (lazy loading)

## Future Considerations

For even larger scale deployments, consider:
- Graph database backends (Neo4j, etc.)
- Distributed caching (Redis)
- Database connection pooling
- Async/await patterns for I/O operations