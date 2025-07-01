# Code Quality & Standards Issues - SFM Enums Module

## Issue #19: PEP 8 and Pylint Compliance (CODE QUALITY)
**Priority**: 🔵 Code Quality  
**Labels**: `pep8`, `pylint`, `code-standards`, `linting`  
**Estimated Effort**: Low  

### Problem
While the current code passes basic syntax checks, there are several PEP 8 and code quality improvements needed:

1. **Line length issues** in some enum comments
2. **Missing type hints** in places where they would be beneficial  
3. **Inconsistent comment formatting** across enum definitions
4. **No `__all__` definition** for explicit public API

### Current Issues Found

**Line length violations:**
```python
INFRASTRUCTURE = (
    auto()
)  # Physical systems, utilities, transportation, communication
# Should be reformatted to stay under 88 characters
```

**Missing module-level metadata:**
```python
# Missing from top of file:
__all__ = [
    'ValueCategory',
    'InstitutionLayer', 
    'ResourceType',
    'FlowNature',
    'RelationshipKind'
]
```

### Solution
1. **Add proper module metadata:**
```python
"""
Enumerations for the Social Fabric Matrix (SFM) framework.
"""

__version__ = "1.0.0"
__author__ = "SFM Development Team"
__all__ = [
    'ValueCategory',
    'InstitutionLayer',
    'ResourceType', 
    'FlowNature',
    'RelationshipKind'
]
```

2. **Fix line length issues:**
```python
INFRASTRUCTURE = auto()  # Physical systems, utilities, transportation,
                        # communication networks
```

3. **Add type hints where beneficial:**
```python
from typing import Dict, List, Optional, Union
```

### Acceptance Criteria
- [ ] Add `__all__` definition for public API
- [ ] Fix all line length violations (max 88 characters)
- [ ] Standardize comment formatting across all enums
- [ ] Add module-level metadata (`__version__`, `__author__`)
- [ ] Run pylint and achieve score > 9.0
- [ ] Add pre-commit hooks for automatic linting

---

## Issue #20: Type Safety and Annotations (CODE QUALITY)
**Priority**: 🔵 Code Quality  
**Labels**: `type-hints`, `mypy`, `type-safety`  
**Estimated Effort**: Medium  

### Problem
Limited type annotations and mypy compliance for better IDE support and error detection.

### Current State
```python
from enum import Enum, auto
# No type imports or annotations
```

### Improved Version
```python
from __future__ import annotations

from enum import Enum, auto
from typing import Dict, List, Optional, Set, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

# Define union types for related enums
CoreValueCategory: TypeAlias = Union[
    'ValueCategory.ECONOMIC',
    'ValueCategory.SOCIAL', 
    'ValueCategory.ENVIRONMENTAL',
    'ValueCategory.CULTURAL',
    'ValueCategory.INSTITUTIONAL',
    'ValueCategory.TECHNOLOGICAL'
]

class ValueCategory(Enum):
    """Categories of value in SFM analysis."""
    
    @classmethod
    def get_core_categories(cls) -> Set['ValueCategory']:
        """Return the six core Hayden framework categories."""
        return {cls.ECONOMIC, cls.SOCIAL, cls.ENVIRONMENTAL, 
                cls.CULTURAL, cls.INSTITUTIONAL, cls.TECHNOLOGICAL}
    
    @classmethod
    def get_extended_categories(cls) -> Set['ValueCategory']:
        """Return extended categories beyond core framework."""
        return set(cls) - cls.get_core_categories()
```

### Acceptance Criteria
- [ ] Add comprehensive type hints throughout module
- [ ] Create type aliases for enum unions and subsets  
- [ ] Add mypy configuration and achieve 100% type coverage
- [ ] Create typed helper methods for enum operations
- [ ] Add type checking to CI/CD pipeline

---

## Issue #21: Docstring Standardization (CODE QUALITY)
**Priority**: 🔵 Code Quality  
**Labels**: `documentation`, `docstrings`, `sphinx`, `standards`  
**Estimated Effort**: Medium  

### Problem
Inconsistent docstring formatting across enum classes and values.

### Current State - Inconsistent Format
```python
class ValueCategory(Enum):
    """
    Categories of value that can be measured and tracked in Social Fabric Matrix analysis.
    
    These categories represent different dimensions of value creation, distribution, and impact
    within socio-economic systems, following Hayden's institutional analysis framework.
    """
    ECONOMIC = auto()  # Market-priced goods, services, financial returns
```

### Improved Standard Format
```python
class ValueCategory(Enum):
    """Categories of value in Hayden's Social Fabric Matrix framework.
    
    This enumeration defines the different dimensions of value creation, distribution,
    and impact within socio-economic systems, based on F. Gregory Hayden's 
    institutional analysis framework.
    
    The enum includes both the core six categories from Hayden's original framework
    and extended categories for comprehensive SFM analysis.
    
    Examples:
        Basic usage:
        
        >>> indicator = Indicator(value_category=ValueCategory.ECONOMIC)
        >>> print(indicator.value_category)
        ValueCategory.ECONOMIC
        
        Checking category types:
        
        >>> ValueCategory.ECONOMIC in ValueCategory.get_core_categories()
        True
    
    References:
        * Hayden, F.G. (2006). "Policymaking for a Good Society: The Social Fabric Matrix Approach to Policy Analysis and Program Evaluation"
        * Hayden, F.G. (1982). "Social Fabric Matrix: From Perspective to Analytical Tool"
    
    Note:
        When adding new value categories, consider whether they fit within 
        Hayden's theoretical framework or represent necessary extensions.
    """
    
    # ═══════════════════════════════════════════════════════════
    # CORE HAYDEN FRAMEWORK VALUES  
    # ═══════════════════════════════════════════════════════════
    
    ECONOMIC = auto()
    """Market-priced goods, services, and financial returns.
    
    Represents traditional economic value measured through market mechanisms,
    including GDP, profit margins, financial returns, and monetary flows.
    Central to Hayden's analysis of market-based value creation.
    """
    
    SOCIAL = auto()
    """Distributional equity, social cohesion, and community well-being.
    
    Encompasses social capital, income distribution, community health,
    and social justice outcomes. Represents Hayden's emphasis on
    distributional consequences of institutional arrangements.
    """
```

### Sphinx-Compatible Format
```python
class RelationshipKind(Enum):
    """Taxonomy of relationship types in Social Fabric Matrix systems.
    
    Args:
        None: This is an enumeration class.
        
    Attributes:
        GOVERNS: Authority relationship over another entity
        REGULATES: Creates or enforces rules for another entity
        
    Example:
        Creating a governance relationship::
        
            relationship = Relationship(
                source_id=ministry_id,
                target_id=company_id, 
                kind=RelationshipKind.REGULATES
            )
    """
```

### Acceptance Criteria
- [ ] Standardize all docstrings to follow Google/Sphinx format
- [ ] Add comprehensive examples to all enum classes
- [ ] Include theoretical references in class docstrings
- [ ] Add individual value documentation with proper formatting
- [ ] Generate HTML documentation using Sphinx
- [ ] Add docstring linting to CI/CD pipeline

---

## Issue #22: Import Organization and Dependencies (CODE QUALITY)
**Priority**: 🔵 Code Quality  
**Labels**: `imports`, `dependencies`, `organization`  
**Estimated Effort**: Low  

### Problem
Simple import structure could be optimized for better organization and future extensibility.

### Current State
```python
from __future__ import annotations

from enum import Enum, auto
```

### Improved Organization
```python
"""
Enumerations for the Social Fabric Matrix (SFM) framework.

This module provides controlled vocabularies and classification systems
for the SFM analysis framework, implementing F. Gregory Hayden's
institutional analysis categories.
"""

from __future__ import annotations

# Standard library imports
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Union, TYPE_CHECKING

# Type checking imports
if TYPE_CHECKING:
    from typing_extensions import TypeAlias, Literal

# Version and metadata
__version__ = "1.0.0"
__author__ = "SFM Development Team"
__license__ = "MIT"

# Public API definition
__all__ = [
    # Core enums
    'ValueCategory',
    'InstitutionLayer', 
    'ResourceType',
    'FlowNature',
    'RelationshipKind',
    
    # Utility types (if added)
    'CoreValueCategory',
    'ExtendedValueCategory',
    
    # Helper functions (if added)
    'validate_enum_combination',
    'get_enum_hierarchy',
]

# Module-level constants
HAYDEN_CORE_VALUES = frozenset([
    'ECONOMIC', 'SOCIAL', 'ENVIRONMENTAL', 
    'CULTURAL', 'INSTITUTIONAL', 'TECHNOLOGICAL'
])
```

### Acceptance Criteria
- [ ] Organize imports according to PEP 8 guidelines
- [ ] Add proper module metadata and versioning
- [ ] Define explicit public API with `__all__`
- [ ] Add module-level constants where appropriate
- [ ] Group related imports logically
- [ ] Add import sorting to pre-commit hooks

---

## Issue #23: Error Handling and Validation (CODE QUALITY)  
**Priority**: 🔵 Code Quality  
**Labels**: `error-handling`, `validation`, `robustness`  
**Estimated Effort**: Medium  

### Problem
No built-in error handling or validation for enum operations and combinations.

### Solution
Add validation and error handling utilities:

```python
class SFMEnumError(Exception):
    """Base exception for SFM enum-related errors."""
    pass

class IncompatibleEnumError(SFMEnumError):
    """Raised when incompatible enum values are used together."""
    pass

class InvalidEnumOperationError(SFMEnumError):
    """Raised when an invalid operation is attempted on enum values."""
    pass

class EnumValidator:
    """Validates enum values and combinations for SFM consistency."""
    
    @staticmethod
    def validate_relationship_context(
        kind: RelationshipKind, 
        source_type: str, 
        target_type: str
    ) -> None:
        """Validate that relationship makes sense in context.
        
        Args:
            kind: The type of relationship
            source_type: Type of source node
            target_type: Type of target node
            
        Raises:
            IncompatibleEnumError: If relationship doesn't make sense
        """
        # Example: Actors can't GOVERN Resources directly
        if kind == RelationshipKind.GOVERNS:
            if source_type != 'Actor' or target_type == 'Resource':
                raise IncompatibleEnumError(
                    f"GOVERNS relationship requires Actor->Actor or Actor->Institution, "
                    f"got {source_type}->{target_type}"
                )
```

### Acceptance Criteria
- [ ] Create custom exception hierarchy for enum errors
- [ ] Add validation functions for enum combinations  
- [ ] Include context-aware validation (e.g., relationship types vs node types)
- [ ] Add comprehensive error messages with suggestions
- [ ] Create validation decorators for model methods
- [ ] Add error handling tests and documentation
