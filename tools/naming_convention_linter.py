#!/usr/bin/env python3
"""
Naming Convention Linter for SFM Enums

This script validates that enum values in sfm_enums.py follow the established
naming conventions documented in docs/naming-conventions.md.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


class NamingConventionLinter:
    """Linter for SFM enum naming conventions."""
    
    def __init__(self):
        self.violations = []
        
        # Patterns that violate naming conventions
        self.passive_voice_pattern = re.compile(r'[A-Z_]+_BY\s*=\s*auto\(\)')
        self.plural_endings_pattern = re.compile(r'[A-Z_]+(S|ES|IES)\s*=\s*auto\(\)')
        self.inconsistent_preposition_pattern = re.compile(r'[A-Z_]+_(WITH|TO|FROM)\s*=\s*auto\(\)')
        
        # Valid preposition patterns
        self.valid_with_relationships = {
            'COLLABORATES_WITH', 'COMPETES_WITH', 'CONTRACTS_WITH',
            'COORDINATES_WITH', 'EXCHANGES_WITH', 'COMMUNICATES_WITH',
            'ALLIES_WITH', 'SYNCHRONIZES_WITH', 'COEXISTS_WITH',
            'EVOLVES_WITH', 'ALIGNS_WITH', 'DISAGREES_WITH'
        }
        
        self.valid_to_relationships = {
            'SELLS_TO', 'ACCOUNTABLE_TO', 'RENTS_TO', 'ATTACHES_TO',
            'TRANSITIONS_TO', 'ADAPTS_TO', 'BELONGS_TO'
        }
        
        self.valid_from_relationships = {
            'BUYS_FROM', 'EMERGES_FROM', 'BENEFITS_FROM'
        }
    
    def check_file(self, filepath: Path) -> List[Tuple[int, str, str]]:
        """Check a file for naming convention violations."""
        violations = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            return [(-1, "FILE_NOT_FOUND", f"File not found: {filepath}")]
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#') or line.startswith('"""'):
                continue
            
            # Check for enum value definitions
            if '= auto()' in line:
                violations.extend(self._check_line(line_num, line))
        
        return violations
    
    def _check_line(self, line_num: int, line: str) -> List[Tuple[int, str, str]]:
        """Check a single line for violations."""
        violations = []
        
        # Extract enum name
        enum_match = re.match(r'\s*([A-Z_]+)\s*=\s*auto\(\)', line)
        if not enum_match:
            return violations
        
        enum_name = enum_match.group(1)
        
        # Check for passive voice (_BY endings)
        if enum_name.endswith('_BY'):
            violations.append((
                line_num, 
                "PASSIVE_VOICE", 
                f"Avoid passive voice: '{enum_name}' should use active voice"
            ))
        
        # Check for problematic plural endings
        if self._is_problematic_plural(enum_name):
            violations.append((
                line_num,
                "PLURAL_FORM",
                f"Use singular form: '{enum_name}' should be singular"
            ))
        
        # Check preposition consistency
        preposition_violation = self._check_preposition_usage(enum_name)
        if preposition_violation:
            violations.append((
                line_num,
                "PREPOSITION_INCONSISTENCY",
                preposition_violation
            ))
        
        return violations
    
    def _is_problematic_plural(self, enum_name: str) -> bool:
        """Check if enum name uses problematic plural forms."""
        # Allow some legitimate plurals
        allowed_plurals = {
            'ENFORCEMENT_MECHANISMS',  # Inherently plural concept
            'ECOSYSTEM_SERVICES',      # Inherently plural concept
        }
        
        if enum_name in allowed_plurals:
            return False
        
        # Check for common plural endings
        problematic_endings = ['_RULES', '_NORMS', '_INSTRUMENTS', '_MECHANISMS']
        return any(enum_name.endswith(ending) for ending in problematic_endings)
    
    def _check_preposition_usage(self, enum_name: str) -> str:
        """Check if preposition usage follows conventions."""
        # Only check for exact preposition patterns at the end of names
        if enum_name.endswith('_WITH'):
            if enum_name not in self.valid_with_relationships:
                return f"'{enum_name}' uses '_WITH' but may not be symmetric/mutual"
        
        elif enum_name.endswith('_TO'):
            if enum_name not in self.valid_to_relationships:
                return f"'{enum_name}' uses '_TO' but may not be directional"
        
        elif enum_name.endswith('_FROM'):
            if enum_name not in self.valid_from_relationships:
                return f"'{enum_name}' uses '_FROM' but may not indicate source"
        
        return ""
    
    def lint_sfm_enums(self, file_path: Path) -> bool:
        """Lint the SFM enums file and return True if no violations found."""
        violations = self.check_file(file_path)
        
        if not violations:
            print(f"✓ No naming convention violations found in {file_path}")
            return True
        
        print(f"✗ Found {len(violations)} naming convention violations in {file_path}:")
        print()
        
        for line_num, violation_type, message in violations:
            print(f"  Line {line_num}: [{violation_type}] {message}")
        
        print()
        print("See docs/naming-conventions.md for detailed guidelines.")
        return False


def main():
    """Main entry point for the linter."""
    linter = NamingConventionLinter()
    
    # Default to checking the SFM enums file
    sfm_enums_path = Path("core/sfm_enums.py")
    
    # Allow custom file path as command line argument
    if len(sys.argv) > 1:
        sfm_enums_path = Path(sys.argv[1])
    
    success = linter.lint_sfm_enums(sfm_enums_path)
    
    if not success:
        sys.exit(1)
    
    print("All naming convention checks passed!")


if __name__ == "__main__":
    main()