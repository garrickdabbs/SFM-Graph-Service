# Type Safety and Validation Enhancement

## Issue Summary
The SFM framework has several type safety issues and incomplete validation that reduce code reliability and increase runtime error risks. Enhanced type checking, validation rules, and error handling are needed for production readiness.

## Type Safety Issues

### 1. Incomplete Type Annotations
**Location**: Various methods return `Any` type, reducing type safety benefits
```python
# Current problematic patterns:
def analyze_policy_impact(...) -> Dict[str, Any]:  # Too generic
def get_metadata(...) -> Optional[Any]:           # No type specificity
def _process_query_result(...) -> Any:            # No return type info
```

### 2. Missing Generic Type Parameters
**Problem**: Collection types don't specify contained types
```python
# Current:
def get_neighbors(...) -> List:           # List of what?
def find_relationships(...) -> Dict:      # Dict with what keys/values?

# Should be:
def get_neighbors(...) -> List[uuid.UUID]:
def find_relationships(...) -> Dict[uuid.UUID, Relationship]:
```

### 3. Union Types Without Proper Handling
**Problem**: Methods accept multiple types but don't handle them properly
```python
# Needs better type discrimination:
def process_entity(entity: Union[Actor, Institution, Policy]) -> NodeResponse:
    # Missing isinstance checks and type-specific handling
```

## Validation Gaps

### 1. Incomplete Cross-Entity Validation
**Location**: [`core/sfm_enums.py`](core/sfm_enums.py ) - `EnumValidator` class
**Problem**: Limited relationship validation rules
```python
def _generate_suggestions(kind: RelationshipKind, source_type: str, target_type: str) -> str:
    # Current implementation is very basic, missing intelligent suggestions
    pass
```

### 2. Missing Business Rule Validation
**Problems**:
- No validation for SFM-specific constraints (e.g., Actor sector compatibility)
- Missing temporal consistency checks (e.g., time-ordered relationships)
- No resource flow conservation validation
- Missing policy authority validation

### 3. Insufficient Input Sanitization
**Problem**: Limited validation of user inputs in API and service layers
- String inputs not sanitized for injection attacks
- Numeric ranges not validated
- UUID format validation incomplete

## Error Handling Deficiencies

### 1. Generic Exception Types
**Problem**: Most errors raise generic exceptions, making debugging difficult
```python
# Current pattern:
raise ValueError("Something went wrong")

# Should be:
raise InvalidRelationshipError(f"Cannot create {kind} relationship between {source_type} and {target_type}")
```

### 2. Missing Error Context
**Problem**: Errors lack sufficient context for debugging
- No entity IDs in error messages
- Missing operation context
- No suggested remediation actions

### 3. Inconsistent Error Handling Patterns
**Problem**: Different modules handle errors differently
- Some swallow exceptions and return None
- Others re-raise with generic messages
- No centralized error handling strategy

## Proposed Type Safety Enhancements

### Phase 1 - Strict Type Annotations
```python
# Enhanced type annotations for core methods
from typing import TypeVar, Generic, Protocol

T = TypeVar('T', bound=Node)

class QueryEngine(Generic[T]):
    def get_nodes_by_type(self, node_type: Type[T]) -> List[T]:
        """Return properly typed node list."""
        pass
    
    def analyze_policy_impact(self, policy_id: uuid.UUID) -> PolicyImpactResult:
        """Return structured result instead of Dict[str, Any]."""
        pass
```

### Phase 2 - Validation Rule Engine
```python
class ValidationRuleEngine:
    def __init__(self):
        self._rules: Dict[str, ValidationRule] = {}
        self._load_sfm_business_rules()
    
    def validate_entity(self, entity: Node) -> ValidationResult:
        """Apply all relevant validation rules to entity."""
        violations = []
        for rule in self._get_applicable_rules(entity):
            if not rule.validate(entity):
                violations.append(rule.get_violation_message(entity))
        return ValidationResult(violations)
    
    def validate_relationship(self, rel: Relationship) -> ValidationResult:
        """Validate relationship with context awareness."""
        # Check entity type compatibility
        # Validate temporal consistency
        # Check business rule constraints
        pass
```

### Phase 3 - Enhanced Error Hierarchy
```python
# Create SFM-specific exception hierarchy
class SFMError(Exception):
    """Base exception for SFM framework."""
    def __init__(self, message: str, entity_id: Optional[uuid.UUID] = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.entity_id = entity_id
        self.context = context or {}

class ValidationError(SFMError):
    """Raised when entity or relationship validation fails."""
    pass

class PolicyAnalysisError(SFMError):
    """Raised during policy analysis operations."""
    pass

class GraphConsistencyError(SFMError):
    """Raised when graph consistency is violated."""
    pass
```

## Validation Rule Implementation

### Business Rules for SFM
```python
class SFMBusinessRules:
    @staticmethod
    def validate_actor_sector_consistency(actor: Actor) -> bool:
        """Ensure actor properties align with sector classification."""
        pass
    
    @staticmethod
    def validate_policy_authority_scope(policy: Policy) -> bool:
        """Verify policy authority matches target sectors."""
        pass
    
    @staticmethod
    def validate_resource_flow_conservation(flow: Flow) -> bool:
        """Check that resource flows obey conservation principles."""
        pass
    
    @staticmethod
    def validate_temporal_relationship_order(rel: Relationship) -> bool:
        """Ensure relationships respect temporal ordering."""
        pass
```

### Input Validation Enhancement
```python
class InputValidator:
    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """Sanitize string input against injection attacks."""
        # Remove/escape dangerous characters
        # Enforce length limits
        # Validate character encoding
        pass
    
    @staticmethod
    def validate_uuid(value: str) -> uuid.UUID:
        """Validate and convert UUID string."""
        try:
            return uuid.UUID(value)
        except ValueError:
            raise ValidationError(f"Invalid UUID format: {value}")
    
    @staticmethod
    def validate_numeric_range(value: float, min_val: float, max_val: float) -> float:
        """Validate numeric value within acceptable range."""
        if not min_val <= value <= max_val:
            raise ValidationError(f"Value {value} outside valid range [{min_val}, {max_val}]")
        return value
```

## Type Safety Testing

### Static Type Checking
```python
# Add mypy configuration
# mypy.ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
```

### Runtime Type Validation
```python
from typeguard import typechecked

@typechecked
def create_relationship(self, source_id: uuid.UUID, target_id: uuid.UUID, kind: RelationshipKind) -> Relationship:
    """Runtime type checking for critical methods."""
    pass
```

## Implementation Priority

### Phase 1 - Critical Type Safety (Week 1)
- Fix all `Any` return types with proper structured types
- Add comprehensive type annotations to core methods
- Implement basic input validation

### Phase 2 - Validation Rules (Week 2)
- Create SFM business rule validation engine
- Implement cross-entity consistency checking
- Add temporal and spatial validation rules

### Phase 3 - Error Handling (Week 2-3)
- Create comprehensive exception hierarchy
- Add contextual error messages with entity IDs
- Implement centralized error handling patterns

### Phase 4 - Advanced Validation (Week 3-4)
- Add runtime type checking for critical paths
- Implement performance-optimized validation
- Create validation rule configuration system

## Testing Requirements

### Type Safety Tests
- Static type checking in CI pipeline
- Runtime type validation tests
- Type consistency across API boundaries

### Validation Tests
- Business rule validation scenarios
- Edge case input validation
- Cross-entity consistency testing

## Acceptance Criteria
- [ ] 100% type annotation coverage for public APIs
- [ ] Zero mypy type checking errors
- [ ] Comprehensive business rule validation
- [ ] Structured exception hierarchy with context
- [ ] Input sanitization for all user-facing interfaces
- [ ] Runtime type checking for critical operations
- [ ] Validation performance impact <5%

## Priority
🔥 **HIGH** - Essential for reliability and maintainability

## Dependencies
- mypy for static type checking
- typeguard for runtime validation
- pydantic for data validation models

## Related Issues
- Links to Issue #23 (Validation Enhancements)
- Links to API security requirements
- Links to error handling improvements
