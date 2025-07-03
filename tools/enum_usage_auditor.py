#!/usr/bin/env python3
"""
Enum Usage Auditor for SFM Enums

This script analyzes usage of enum values across the codebase to help identify
unused or infrequently used values that may need review.
"""

import re
import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set


class EnumUsageAuditor:
    """Auditor for SFM enum usage patterns."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.enum_usage = defaultdict(int)
        self.enum_locations = defaultdict(list)
    
    def audit_usage(self) -> Dict[str, Dict[str, int]]:
        """Audit enum usage across the entire codebase."""
        # Define enum patterns to search for
        enum_patterns = [
            r'RelationshipKind\.([A-Z_]+)',
            r'ValueCategory\.([A-Z_]+)',
            r'InstitutionLayer\.([A-Z_]+)',
            r'ResourceType\.([A-Z_]+)',
            r'FlowNature\.([A-Z_]+)',
            r'FlowType\.([A-Z_]+)',
        ]
        
        # Search through Python files
        for py_file in self._find_python_files():
            self._scan_file(py_file, enum_patterns)
        
        return self._organize_results()
    
    def _find_python_files(self) -> List[Path]:
        """Find all Python files in the project."""
        python_files = []
        
        # Search in key directories
        search_dirs = ['core', 'tests', 'api', 'db', '.']
        
        for search_dir in search_dirs:
            dir_path = self.project_root / search_dir
            if dir_path.exists():
                python_files.extend(dir_path.glob('*.py'))
                # Also search subdirectories
                python_files.extend(dir_path.glob('**/*.py'))
        
        return list(set(python_files))  # Remove duplicates
    
    def _scan_file(self, file_path: Path, patterns: List[str]) -> None:
        """Scan a file for enum usage patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (FileNotFoundError, UnicodeDecodeError):
            return
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                enum_name = match.group(1)
                enum_class = pattern.split(r'\.')[0].replace(r'\\', '')
                full_name = f"{enum_class}.{enum_name}"
                
                self.enum_usage[full_name] += 1
                self.enum_locations[full_name].append(str(file_path))
    
    def _organize_results(self) -> Dict[str, Dict[str, int]]:
        """Organize results by enum class."""
        results = defaultdict(dict)
        
        for full_name, count in self.enum_usage.items():
            enum_class, enum_value = full_name.split('.', 1)
            results[enum_class][enum_value] = count
        
        return dict(results)
    
    def print_usage_report(self, min_usage: int = 0) -> None:
        """Print a usage report showing enum value usage counts."""
        results = self.audit_usage()
        
        print("SFM Enum Usage Report")
        print("=" * 50)
        print()
        
        for enum_class, usage_counts in results.items():
            print(f"{enum_class}:")
            print("-" * len(enum_class))
            
            # Sort by usage count (least used first)
            sorted_usage = sorted(usage_counts.items(), key=lambda x: x[1])
            
            unused_count = 0
            for enum_value, count in sorted_usage:
                if count >= min_usage:
                    if count == 0:
                        unused_count += 1
                        print(f"  {enum_value:30} - UNUSED")
                    else:
                        print(f"  {enum_value:30} - {count:3d} uses")
            
            if unused_count > 0:
                print(f"  >>> {unused_count} unused values found")
            
            print()
    
    def find_unused_enums(self) -> Dict[str, List[str]]:
        """Find enum values that are never used in the codebase."""
        results = self.audit_usage()
        unused = defaultdict(list)
        
        for enum_class, usage_counts in results.items():
            for enum_value, count in usage_counts.items():
                if count == 0:
                    unused[enum_class].append(enum_value)
        
        return dict(unused)
    
    def print_unused_report(self) -> None:
        """Print a report of unused enum values."""
        unused = self.find_unused_enums()
        
        if not unused:
            print("✅ No unused enum values found!")
            return
        
        print("Unused Enum Values Report")
        print("=" * 30)
        print()
        
        total_unused = 0
        for enum_class, unused_values in unused.items():
            if unused_values:
                print(f"{enum_class} ({len(unused_values)} unused):")
                for value in sorted(unused_values):
                    print(f"  - {value}")
                print()
                total_unused += len(unused_values)
        
        print(f"Total unused enum values: {total_unused}")


def main():
    """Main entry point for the auditor."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Audit SFM enum usage")
    parser.add_argument("--unused-only", action="store_true",
                      help="Show only unused enum values")
    parser.add_argument("--min-usage", type=int, default=0,
                      help="Minimum usage count to display")
    
    args = parser.parse_args()
    
    auditor = EnumUsageAuditor()
    
    if args.unused_only:
        auditor.print_unused_report()
    else:
        auditor.print_usage_report(args.min_usage)


if __name__ == "__main__":
    main()