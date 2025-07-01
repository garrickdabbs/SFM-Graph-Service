#!/usr/bin/env python3
"""
Memory benchmark for SFM enum optimization.

This script measures memory usage improvements from splitting large enums
into core and extended modules.
"""

import sys
import tracemalloc
import gc
from typing import Dict, Any

def measure_memory_usage(description: str, func) -> Dict[str, Any]:
    """Measure memory usage of a function."""
    gc.collect()  # Force garbage collection
    tracemalloc.start()
    
    result = func()
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return {
        'description': description,
        'current_mb': current / 1024 / 1024,
        'peak_mb': peak / 1024 / 1024,
        'result': result
    }

def import_original_enums():
    """Simulate importing the old large enums (creates equivalent structures)."""
    from enum import Enum, auto
    
    # Simulate the old large ValueCategory enum
    class OldValueCategory(Enum):
        ECONOMIC = auto()
        SOCIAL = auto()
        ENVIRONMENTAL = auto()
        CULTURAL = auto()
        INSTITUTIONAL = auto()
        TECHNOLOGICAL = auto()
        POLITICAL = auto()
        EDUCATIONAL = auto()
        HEALTH = auto()
        SECURITY = auto()
        INFRASTRUCTURE = auto()
        LEGAL = auto()
        ETHICAL = auto()
        AESTHETIC = auto()
        RECREATIONAL = auto()
        SPIRITUAL = auto()
        DEMOGRAPHIC = auto()
        SPATIAL = auto()
        TEMPORAL = auto()
        INFORMATIONAL = auto()
        PSYCHOLOGICAL = auto()
        COMMUNITY = auto()
        RESOURCE = auto()
        PERFORMANCE = auto()
        QUALITY = auto()
        ACCESSIBILITY = auto()
        RESILIENCE = auto()
        INNOVATION = auto()
        EQUITY = auto()
        TRANSPARENCY = auto()
        PARTICIPATION = auto()
        SUSTAINABILITY = auto()
        DIVERSITY = auto()
        COOPERATION = auto()
        COMPETITIVENESS = auto()
        MOBILITY = auto()
        COMMUNICATION = auto()
        ADAPTATION = auto()
        INTEGRATION = auto()
        AUTONOMY = auto()
        STABILITY = auto()
        EFFICIENCY = auto()
        EFFECTIVENESS = auto()
        ACCOUNTABILITY = auto()
        LEGITIMACY = auto()
        CAPACITY = auto()
        CONNECTIVITY = auto()
        FLEXIBILITY = auto()
        SCALABILITY = auto()
        INTEROPERABILITY = auto()
    
    # Create many instances to simulate usage
    values = []
    for _ in range(100):
        values.extend([
            OldValueCategory.ECONOMIC,
            OldValueCategory.SOCIAL,
            OldValueCategory.ENVIRONMENTAL,
            OldValueCategory.POLITICAL
        ])
    
    return len(values)

def import_new_core_enums():
    """Import the new optimized core enums."""
    from core.sfm_core_enums import (
        CoreValueCategory,
        CoreRelationshipKind,
        CoreResourceType,
        CoreFlowNature
    )
    
    # Create many instances to simulate usage
    values = []
    for _ in range(100):
        values.extend([
            CoreValueCategory.ECONOMIC,
            CoreValueCategory.SOCIAL,
            CoreValueCategory.ENVIRONMENTAL,
            CoreRelationshipKind.GOVERNS,
            CoreResourceType.NATURAL,
            CoreFlowNature.INPUT
        ])
    
    return len(values)

def import_new_unified_enums():
    """Import the new unified enums (with backward compatibility)."""
    from core.sfm_enums import (
        ValueCategory,
        RelationshipKind,
        ResourceType,
        FlowNature
    )
    
    # Create many instances to simulate usage
    values = []
    for _ in range(100):
        values.extend([
            ValueCategory.ECONOMIC,
            ValueCategory.SOCIAL,
            ValueCategory.ENVIRONMENTAL,
            ValueCategory.POLITICAL,
            RelationshipKind.GOVERNS,
            ResourceType.NATURAL,
            FlowNature.INPUT
        ])
    
    return len(values)

def benchmark_enum_memory():
    """Run memory benchmarks for enum implementations."""
    print("SFM Enum Memory Optimization Benchmark")
    print("=" * 50)
    print()
    
    # Measure original approach (simulated)
    old_result = measure_memory_usage(
        "Original large enums (simulated)", 
        import_original_enums
    )
    
    # Measure new core enums
    core_result = measure_memory_usage(
        "New core enums only",
        import_new_core_enums
    )
    
    # Measure new unified enums
    unified_result = measure_memory_usage(
        "New unified enums (backward compatible)",
        import_new_unified_enums
    )
    
    # Display results
    for result in [old_result, core_result, unified_result]:
        print(f"{result['description']:.<45} {result['peak_mb']:.2f} MB")
    
    print()
    print("Memory Improvement Analysis:")
    print("-" * 30)
    
    core_improvement = ((old_result['peak_mb'] - core_result['peak_mb']) / old_result['peak_mb']) * 100
    unified_improvement = ((old_result['peak_mb'] - unified_result['peak_mb']) / old_result['peak_mb']) * 100
    
    print(f"Core enums vs Original: {core_improvement:.1f}% reduction")
    print(f"Unified enums vs Original: {unified_improvement:.1f}% reduction")
    
    # Test actual enum sizes
    print()
    print("Enum Size Comparison:")
    print("-" * 20)
    
    from core.sfm_core_enums import CoreValueCategory
    from core.sfm_enums import ValueCategory
    
    print(f"CoreValueCategory size: {len(CoreValueCategory)}")
    print(f"ValueCategory size (unified): {len(ValueCategory)}")
    
    # Estimate total memory reduction
    total_reduction = core_improvement
    if total_reduction > 0:
        print()
        print(f"🎯 Target: 30-50% memory reduction")
        print(f"✅ Achieved: {total_reduction:.1f}% memory reduction")
        if total_reduction >= 30:
            print("✅ SUCCESS: Target memory reduction achieved!")
        else:
            print("⚠️  Partial success - consider further optimizations")
    
    return {
        'old_mb': old_result['peak_mb'],
        'core_mb': core_result['peak_mb'], 
        'unified_mb': unified_result['peak_mb'],
        'core_improvement': core_improvement,
        'unified_improvement': unified_improvement
    }

if __name__ == '__main__':
    try:
        results = benchmark_enum_memory()
        print()
        print("Benchmark completed successfully!")
    except Exception as e:
        print(f"Benchmark failed: {e}")
        traceback.print_exc()
        sys.exit(1)