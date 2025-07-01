# High Priority Issues - SFM Enums Module

## Issue #4: Unused and Redundant Enum Values (HIGH)
**Priority**: 🟠 High  
**Labels**: `cleanup`, `maintenance`, `audit`  
**Estimated Effort**: Medium  

### Problem
Analysis reveals numerous enum values that are never used in the codebase or are redundant:

**ValueCategory redundancies**:
- `EFFICIENCY` vs `PERFORMANCE` - overlapping concepts
- `COMMUNICATION` vs `INFORMATIONAL` - duplicate meaning
- `ADAPTATION` vs `FLEXIBILITY` - similar concepts
- `EFFECTIVENESS` vs `PERFORMANCE` - overlapping

**Potentially unused values** (need verification):
- Many of the 68 `ValueCategory` values may not be referenced
- Several `RelationshipKind` values might be theoretical only
- Some `ResourceType` subcategories may be over-specified

### Solution
1. **Audit enum usage across entire codebase**
2. **Create usage frequency analysis**
3. **Consolidate redundant categories**
4. **Mark deprecated values with warnings**
5. **Create migration path for removed values**

### Code Analysis Needed
```bash
# Find all enum usage patterns
grep -r "ValueCategory\." --include="*.py" .
grep -r "RelationshipKind\." --include="*.py" .
grep -r "ResourceType\." --include="*.py" .
grep -r "FlowNature\." --include="*.py" .
```

### Acceptance Criteria
- [ ] Complete usage audit of all enum values
- [ ] Document usage frequency for each enum value
- [ ] Consolidate redundant categories (reduce by ~20%)
- [ ] Add deprecation warnings for unused values
- [ ] Create enum value migration utilities

---

## Issue #5: Poor Documentation and Missing Examples (HIGH)
**Priority**: 🟠 High  
**Labels**: `documentation`, `usability`, `examples`  
**Estimated Effort**: Medium  

### Problem
Current enum documentation lacks:
1. **Practical usage examples** with SFM models
2. **References to Hayden's theoretical framework**
3. **Clear guidance** on when to use specific enum values
4. **Integration examples** showing enum relationships

### Current State
```python
class ValueCategory(Enum):
    """
    Categories of value that can be measured and tracked in Social Fabric Matrix analysis.
    
    These categories represent different dimensions of value creation, distribution, and impact
    within socio-economic systems, following Hayden's institutional analysis framework.
    """
    ECONOMIC = auto()  # Market-priced goods, services, financial returns
```

### Improved Documentation Example
```python
class ValueCategory(Enum):
    """
    Categories of value in Hayden's Social Fabric Matrix framework.
    
    Based on F. Gregory Hayden's institutional analysis, these categories represent
    different dimensions of value creation, distribution, and impact within
    socio-economic systems.
    
    Usage Examples:
        >>> indicator = Indicator(
        ...     label="GDP Growth",
        ...     value_category=ValueCategory.ECONOMIC,
        ...     measurement_unit="percent"
        ... )
        
        >>> # Multiple value categories for complex indicators
        >>> sustainability_index = Indicator(
        ...     label="Sustainability Index",
        ...     value_category=ValueCategory.ENVIRONMENTAL,
        ...     secondary_categories=[ValueCategory.SOCIAL, ValueCategory.ECONOMIC]
        ... )
    
    References:
        - Hayden, F.G. (2006). "Policymaking for a Good Society"
        - Hayden, F.G. (1982). "Social Fabric Matrix: From Perspective to Analytical Tool"
    """
    
    # Core Hayden Categories (from original SFM framework)
    ECONOMIC = auto()    # Market transactions, monetary flows, financial returns
                        # Examples: GDP, profit margins, market prices
    SOCIAL = auto()      # Distributional equity, social cohesion, community well-being
                        # Examples: income inequality, social capital, community health
```

### Acceptance Criteria
- [ ] Add comprehensive docstrings to all enum classes
- [ ] Include practical usage examples for each major enum
- [ ] Add references to Hayden's theoretical work
- [ ] Create enum integration guide in module docstring
- [ ] Add type hints and usage patterns documentation

---

## Issue #6: Inconsistent Naming Conventions (HIGH)
**Priority**: 🟠 High  
**Labels**: `style`, `consistency`, `pep8`  
**Estimated Effort**: Low-Medium  

### Problem
Inconsistent naming patterns across enums:

1. **Verb tense inconsistencies** in `RelationshipKind`:
   - `GOVERNS` (present) vs `GOVERNED_BY` (passive)
   - `FUNDS` (present) vs `FUNDED_BY` (passive)

2. **Singular vs plural inconsistencies**:
   - `FORMAL_RULE` vs `FORMAL_RULES`
   - `POLICY_INSTRUMENT` vs `ENFORCEMENT_MECHANISMS`

3. **Preposition usage**:
   - Some relationships use `_WITH`, others use `_TO`, others use `_FROM`
   - Inconsistent directional indicators

### Solution
**Standardize relationship naming**:
```python
# Current inconsistent:
BUYS_FROM = auto()
SELLS_TO = auto()
COLLABORATES_WITH = auto()

# Proposed consistent:
BUYS_FROM = auto()      # Actor A buys from Actor B
SELLS_TO = auto()       # Actor A sells to Actor B  
COLLABORATES_WITH = auto()  # Actor A collaborates with Actor B
```

**Standardize institution naming**:
```python
# Use singular forms consistently
FORMAL_RULE = auto()     # not FORMAL_RULES
INFORMAL_NORM = auto()   # not INFORMAL_NORMS
```

### Acceptance Criteria
- [ ] Define naming convention standards document
- [ ] Audit all enum values for consistency
- [ ] Rename inconsistent values (with deprecation warnings)
- [ ] Update all code references to use new names
- [ ] Add linting rules to enforce naming conventions

---

## Issue #7: Missing Enum Validation and Constraints (HIGH)
**Priority**: 🟠 High  
**Labels**: `validation`, `robustness`, `type-safety`  
**Estimated Effort**: Medium  

### Problem
No validation for:
1. **Enum combination compatibility** (some combinations don't make sense)
2. **Required vs optional** enum usage contexts
3. **Value constraints** for specific SFM scenarios
4. **Cross-enum relationships** and dependencies

### Solution
Add validation utilities:

```python
class EnumValidator:
    """Validates enum combinations for SFM consistency."""
    
    @staticmethod
    def validate_flow_combination(nature: FlowNature, flow_type: FlowType) -> bool:
        """Validate that flow nature and type are compatible."""
        incompatible = {
            (FlowNature.FINANCIAL, FlowType.MATERIAL),
            (FlowNature.ENERGY, FlowType.INFORMATION),
        }
        return (nature, flow_type) not in incompatible
    
    @staticmethod  
    def validate_relationship_actors(kind: RelationshipKind, 
                                   source_type: type, 
                                   target_type: type) -> bool:
        """Validate relationship makes sense between node types."""
        # e.g., only Actors can EMPLOY other Actors
        if kind == RelationshipKind.EMPLOYS:
            return isinstance(source_type, Actor) and isinstance(target_type, Actor)
```

### Acceptance Criteria
- [ ] Create enum validation utility class
- [ ] Define compatibility matrices for enum combinations
- [ ] Add validation to model constructors
- [ ] Create comprehensive validation test suite
- [ ] Document validation rules and constraints
