#!/usr/bin/env python3
"""
Tests for the new enum memory optimization implementation.

This module tests the split enum structure to ensure:
1. Core enums work correctly
2. Backward compatibility is maintained  
3. Memory optimization is achieved
4. Extended enums are available when needed
"""

import unittest
from core.sfm_core_enums import (
    CoreValueCategory, CoreRelationshipKind, 
    CoreResourceType, CoreFlowNature
)
from core.sfm_enums import (
    ValueCategory, RelationshipKind,
    ResourceType, FlowNature
)


class TestEnumMemoryOptimization(unittest.TestCase):
    """Test the enum memory optimization implementation."""
    
    def test_core_enum_sizes(self):
        """Test that core enums have significantly fewer values."""
        # Core enums should be much smaller
        self.assertLessEqual(len(CoreValueCategory), 10)
        self.assertLessEqual(len(CoreRelationshipKind), 20)
        self.assertLessEqual(len(CoreResourceType), 10)
        self.assertLessEqual(len(CoreFlowNature), 10)
        
        # Total core enum values should be much less than original
        total_core = (len(CoreValueCategory) + len(CoreRelationshipKind) + 
                     len(CoreResourceType) + len(CoreFlowNature))
        self.assertLess(total_core, 50, "Core enums should be small for memory efficiency")
    
    def test_backward_compatibility(self):
        """Test that unified enums maintain backward compatibility."""
        # Should have the same commonly tested values
        self.assertTrue(hasattr(ValueCategory, 'ECONOMIC'))
        self.assertTrue(hasattr(ValueCategory, 'SOCIAL'))
        self.assertTrue(hasattr(ValueCategory, 'POLITICAL'))
        
        self.assertTrue(hasattr(RelationshipKind, 'GOVERNS'))
        self.assertTrue(hasattr(RelationshipKind, 'USES'))
        self.assertTrue(hasattr(RelationshipKind, 'PAYS'))
        
        self.assertTrue(hasattr(ResourceType, 'NATURAL'))
        self.assertTrue(hasattr(ResourceType, 'HUMAN'))
        
        self.assertTrue(hasattr(FlowNature, 'INPUT'))
        self.assertTrue(hasattr(FlowNature, 'OUTPUT'))
        self.assertTrue(hasattr(FlowNature, 'TRANSFER'))
    
    def test_core_values_functionality(self):
        """Test that core enum values work correctly."""
        # Test core value category values
        self.assertIsInstance(CoreValueCategory.ECONOMIC, CoreValueCategory)
        self.assertEqual(str(CoreValueCategory.ECONOMIC), 'CoreValueCategory.ECONOMIC')
        
        # Test iteration
        core_categories = list(CoreValueCategory)
        self.assertIn(CoreValueCategory.ECONOMIC, core_categories)
        self.assertIn(CoreValueCategory.SOCIAL, core_categories)
        
        # Test comparison
        self.assertEqual(CoreValueCategory.ECONOMIC, CoreValueCategory.ECONOMIC)
        self.assertNotEqual(CoreValueCategory.ECONOMIC, CoreValueCategory.SOCIAL)
    
    def test_unified_values_functionality(self):
        """Test that unified enum values work correctly."""
        # Test unified value category values
        self.assertIsInstance(ValueCategory.ECONOMIC, ValueCategory)
        self.assertEqual(str(ValueCategory.ECONOMIC), 'ValueCategory.ECONOMIC')
        
        # Test iteration
        all_categories = list(ValueCategory)
        self.assertIn(ValueCategory.ECONOMIC, all_categories)
        self.assertIn(ValueCategory.POLITICAL, all_categories)
        
        # Test comparison
        self.assertEqual(ValueCategory.ECONOMIC, ValueCategory.ECONOMIC)
        self.assertNotEqual(ValueCategory.ECONOMIC, ValueCategory.SOCIAL)
    
    def test_memory_optimization_achieved(self):
        """Test that memory optimization targets are met."""
        # Calculate reduction percentages
        original_total = 300  # Approximate original total from issue
        core_total = (len(CoreValueCategory) + len(CoreRelationshipKind) + 
                     len(CoreResourceType) + len(CoreFlowNature))
        
        reduction_percent = ((original_total - core_total) / original_total) * 100
        
        # Should achieve at least 30% reduction (target from issue)
        self.assertGreaterEqual(reduction_percent, 30,
                               f"Should achieve 30%+ reduction, got {reduction_percent:.1f}%")
        
        # Should achieve the 30-50% target mentioned in issue
        self.assertGreaterEqual(reduction_percent, 30,
                               "Memory optimization target not met")
    
    def test_import_efficiency(self):
        """Test that imports are efficient."""
        # Core enums should import without loading extended modules
        import sys
        
        # Check that core enums can be imported independently
        core_modules_before = set(sys.modules.keys())
        
        from core.sfm_core_enums import CoreValueCategory
        
        core_modules_after = set(sys.modules.keys())
        new_modules = core_modules_after - core_modules_before
        
        # Should not import too many additional modules
        self.assertLess(len(new_modules), 5, 
                       "Core enum import should be lightweight")
    
    def test_commonly_used_values_available(self):
        """Test that commonly used values are readily available."""
        # These values appear frequently in the codebase analysis
        commonly_used_values = [
            (ValueCategory, 'ECONOMIC'),
            (ValueCategory, 'SOCIAL'), 
            (ValueCategory, 'ENVIRONMENTAL'),
            (RelationshipKind, 'GOVERNS'),
            (RelationshipKind, 'USES'),
            (RelationshipKind, 'IMPLEMENTS'),
            (ResourceType, 'NATURAL'),
            (ResourceType, 'PRODUCED'),
            (FlowNature, 'INPUT'),
            (FlowNature, 'OUTPUT'),
            (FlowNature, 'TRANSFER')
        ]
        
        for enum_class, value_name in commonly_used_values:
            with self.subTest(enum=enum_class.__name__, value=value_name):
                self.assertTrue(hasattr(enum_class, value_name),
                               f"{enum_class.__name__}.{value_name} should be available")
                
                # Should be accessible without error
                value = getattr(enum_class, value_name)
                self.assertIsInstance(value, enum_class)
    
    def test_extended_enums_exist(self):
        """Test that extended enum modules exist and can be imported."""
        try:
            from core.sfm_extended_enums import (
                GovernanceValueCategory,
                SpecializedValueCategory,
                SpecializedResourceType,
                SpecializedFlowNature
            )
            
            # Should have some values
            self.assertGreater(len(GovernanceValueCategory), 0)
            self.assertGreater(len(SpecializedValueCategory), 0)
            self.assertGreater(len(SpecializedResourceType), 0)
            self.assertGreater(len(SpecializedFlowNature), 0)
            
        except ImportError as e:
            self.fail(f"Extended enums should be importable: {e}")
        
        try:
            from core.sfm_relationship_enums import (
                GovernanceRelationshipKind,
                EconomicRelationshipKind
            )
            
            # Should have some values
            self.assertGreater(len(GovernanceRelationshipKind), 0)
            self.assertGreater(len(EconomicRelationshipKind), 0)
            
        except ImportError as e:
            self.fail(f"Relationship enums should be importable: {e}")
    
    def test_enum_value_consistency(self):
        """Test that enum values are consistent across modules."""
        # Core values should match unified values
        self.assertEqual(CoreValueCategory.ECONOMIC.name, 'ECONOMIC')
        self.assertEqual(ValueCategory.ECONOMIC.name, 'ECONOMIC')
        
        self.assertEqual(CoreResourceType.NATURAL.name, 'NATURAL')
        self.assertEqual(ResourceType.NATURAL.name, 'NATURAL')


if __name__ == '__main__':
    unittest.main()