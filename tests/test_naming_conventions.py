"""
Test module for SFM enum naming conventions.

This module tests that all SFM enum values follow the established naming
conventions documented in docs/naming-conventions.md.
"""

import unittest
from pathlib import Path
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.naming_convention_linter import NamingConventionLinter
from core.sfm_enums import (
    RelationshipKind, ValueCategory, InstitutionLayer, 
    ResourceType, FlowNature, FlowType
)


class TestNamingConventions(unittest.TestCase):
    """Test cases for SFM enum naming conventions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.linter = NamingConventionLinter()
        self.sfm_enums_path = Path("core/sfm_enums.py")
    
    def test_no_naming_convention_violations(self):
        """Test that the SFM enums file has no naming convention violations."""
        violations = self.linter.check_file(self.sfm_enums_path)
        
        if violations:
            violation_messages = [f"Line {line}: [{vtype}] {msg}" 
                                for line, vtype, msg in violations]
            self.fail(
                f"Found {len(violations)} naming convention violations:\n" +
                "\n".join(violation_messages)
            )
    
    def test_relationship_kind_consistency(self):
        """Test that RelationshipKind values follow consistent patterns."""
        # Check that all _WITH relationships are mutual/symmetric
        with_relationships = [
            name for name in dir(RelationshipKind) 
            if name.endswith('_WITH') and not name.startswith('_')
        ]
        
        mutual_concepts = [
            'COLLABORATES', 'COMPETES', 'CONTRACTS', 'COORDINATES',
            'EXCHANGES', 'COMMUNICATES', 'ALLIES', 'SYNCHRONIZES',
            'COEXISTS', 'EVOLVES', 'ALIGNS', 'DISAGREES'
        ]
        
        for rel_name in with_relationships:
            concept = rel_name.replace('_WITH', '')
            self.assertIn(
                concept, mutual_concepts,
                f"{rel_name} uses '_WITH' but may not be a mutual relationship"
            )
    
    def test_no_passive_voice_relationships(self):
        """Test that no RelationshipKind values use passive voice."""
        passive_relationships = [
            name for name in dir(RelationshipKind)
            if name.endswith('_BY') and not name.startswith('_')
        ]
        
        self.assertEqual(
            len(passive_relationships), 0,
            f"Found passive voice relationships: {passive_relationships}. "
            "Use active voice instead."
        )
    
    def test_institution_layer_singular_forms(self):
        """Test that InstitutionLayer values use singular forms."""
        problematic_plurals = []
        
        for name in dir(InstitutionLayer):
            if name.startswith('_'):
                continue
            
            # Check for common plural endings that should be singular
            if name.endswith('_RULES') and name != 'ENFORCEMENT_MECHANISMS':
                problematic_plurals.append(name)
            elif name.endswith('_NORMS') and name != 'INFORMAL_NORM':
                problematic_plurals.append(name)
            elif name.endswith('_INSTRUMENTS') and name != 'POLICY_INSTRUMENT':
                problematic_plurals.append(name)
        
        self.assertEqual(
            len(problematic_plurals), 0,
            f"Found plural forms that should be singular: {problematic_plurals}"
        )
    
    def test_value_category_naming_consistency(self):
        """Test that ValueCategory values follow consistent naming patterns."""
        # This test focuses on naming patterns rather than semantic redundancy
        value_names = [
            name for name in dir(ValueCategory) 
            if not name.startswith('_')
        ]
        
        # Check that all names use appropriate singular/plural forms
        # (This is a placeholder - specific naming issues would be checked here)
        for name in value_names:
            # Ensure names don't have obvious naming convention violations
            self.assertFalse(
                name.endswith('_BY'),
                f"{name} uses passive voice, should use active voice"
            )
    
    def test_preposition_pattern_consistency(self):
        """Test that preposition usage follows established patterns."""
        # Get all relationship names
        relationship_names = [
            name for name in dir(RelationshipKind)
            if not name.startswith('_')
        ]
        
        # Check _TO relationships are directional
        to_relationships = [name for name in relationship_names if name.endswith('_TO')]
        directional_concepts = [
            'SELLS', 'ACCOUNTABLE', 'RENTS', 'ATTACHES', 'TRANSITIONS', 'ADAPTS', 'BELONGS'
        ]
        
        for rel_name in to_relationships:
            concept = rel_name.replace('_TO', '')
            self.assertIn(
                concept, directional_concepts,
                f"{rel_name} uses '_TO' but may not be directional"
            )
        
        # Check _FROM relationships indicate source
        from_relationships = [name for name in relationship_names if name.endswith('_FROM')]
        source_concepts = ['BUYS', 'EMERGES', 'BENEFITS']
        
        for rel_name in from_relationships:
            concept = rel_name.replace('_FROM', '')
            self.assertIn(
                concept, source_concepts,
                f"{rel_name} uses '_FROM' but may not indicate source"
            )
    
    def test_enum_values_are_screaming_snake_case(self):
        """Test that all enum values use SCREAMING_SNAKE_CASE."""
        enums_to_check = [
            RelationshipKind, ValueCategory, InstitutionLayer,
            ResourceType, FlowNature, FlowType
        ]
        
        for enum_class in enums_to_check:
            for name in dir(enum_class):
                if name.startswith('_'):
                    continue
                
                # Check that it's all uppercase with underscores
                self.assertTrue(
                    name.isupper() and '_' in name or name.isupper(),
                    f"{enum_class.__name__}.{name} should use SCREAMING_SNAKE_CASE"
                )
                
                # Check that it doesn't have consecutive underscores
                self.assertNotIn(
                    '__', name,
                    f"{enum_class.__name__}.{name} should not have consecutive underscores"
                )
    
    def test_linter_tool_executable(self):
        """Test that the naming convention linter tool can be executed."""
        import subprocess
        
        result = subprocess.run([
            'python', 'tools/naming_convention_linter.py', 'core/sfm_enums.py'
        ], capture_output=True, text=True, cwd='.')
        
        self.assertEqual(
            result.returncode, 0,
            f"Naming convention linter failed: {result.stderr}"
        )
        
        self.assertIn(
            "No naming convention violations found",
            result.stdout,
            "Expected linter to pass on current SFM enums"
        )


if __name__ == '__main__':
    unittest.main()