# Critical Priority Issues - SFM Enums Module

## Issue #1: Missing Enums for String-Based Fields (CRITICAL)
**Priority**: 🔴 Critical  
**Labels**: `bug`, `type-safety`, `refactor`  
**Estimated Effort**: High  

### Problem
Several model classes use string fields that should be enums for type safety and consistency:

1. `Flow.flow_type` - currently string, should be enum
2. `PolicyInstrument.instrument_type` - currently string, should be enum  
3. `ChangeProcess.change_type` - currently string, should be enum
4. `BehavioralPattern.pattern_type` - currently string, should be enum
5. `FeedbackLoop.polarity` and `FeedbackLoop.type` - currently strings
6. `TemporalDynamics.function_type` - currently string
7. `ValidationRule.rule_type` - currently string
8. `SystemProperty.property_type` - currently string

### Solution
Create new enums:
```python
class FlowType(Enum):
    MATERIAL = auto()
    ENERGY = auto()
    INFORMATION = auto()
    FINANCIAL = auto()
    SOCIAL = auto()

class PolicyInstrumentType(Enum):
    REGULATORY = auto()
    ECONOMIC = auto()
    VOLUNTARY = auto()
    INFORMATION = auto()

class ChangeType(Enum):
    EVOLUTIONARY = auto()
    REVOLUTIONARY = auto()
    CYCLICAL = auto()
    INCREMENTAL = auto()

class BehaviorPatternType(Enum):
    HABITUAL = auto()
    STRATEGIC = auto()
    ADAPTIVE = auto()
    RESISTANT = auto()

class FeedbackPolarity(Enum):
    REINFORCING = auto()
    BALANCING = auto()

class FeedbackType(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()
    NEUTRAL = auto()
```

### Acceptance Criteria
- [ ] Create all missing enums in `sfm_enums.py`
- [ ] Update corresponding model classes to use enums
- [ ] Update all existing code to use new enums
- [ ] Add migration script for existing data
- [ ] Update tests to verify enum usage

---

## Issue #2: Memory Inefficiency from Oversized Enums (CRITICAL)
**Priority**: 🔴 Critical  
**Labels**: `performance`, `memory`, `refactor`  
**Estimated Effort**: High  

### Problem
Current enum sizes are memory-intensive:
- `ValueCategory`: 68 values
- `RelationshipKind`: 148 values  
- `ResourceType`: 47 values
- `FlowNature`: 54 values

These large enums consume significant memory even when only a subset is used.

### Solution
1. **Split into logical sub-enums**:
   ```python
   class CoreValueCategory(Enum):
       ECONOMIC = auto()
       SOCIAL = auto()
       ENVIRONMENTAL = auto()
       CULTURAL = auto()
       INSTITUTIONAL = auto()
       TECHNOLOGICAL = auto()

   class GovernanceValueCategory(Enum):
       POLITICAL = auto()
       LEGAL = auto()
       TRANSPARENCY = auto()
       ACCOUNTABILITY = auto()
   ```

2. **Implement lazy loading patterns**

### Acceptance Criteria
- [ ] Analyze enum usage patterns across codebase
- [ ] Split large enums into focused sub-enums
- [ ] Maintain backward compatibility
- [ ] Benchmark memory usage improvements
- [ ] Update documentation with new structure

---

## Issue #3: Inconsistent Hayden SFM Framework Alignment (CRITICAL)
**Priority**: 🔴 Critical  
**Labels**: `framework-alignment`, `theory`, `enhancement`  
**Estimated Effort**: Medium  

### Problem
Many enum values don't clearly align with F. Gregory Hayden's Social Fabric Matrix framework:

1. **Missing ceremonial vs. instrumental categorization** in relationships
2. **Insufficient coverage of power dynamics** in resource types
3. **Limited tool-skill-technology complex representation**
4. **Missing path dependency and institutional change patterns**

### Solution
1. **Add metadata to relationships**:
   ```python
   class RelationshipKind(Enum):
       # Add properties indicating ceremonial/instrumental tendency
       CEREMONIALLY_REINFORCES = auto()  # ✅ Already exists
       INSTRUMENTALLY_ADAPTS = auto()    # ✅ Already exists
       
       @property
       def ceremonial_tendency(self) -> float:
           """Returns 0.0-1.0 indicating ceremonial vs instrumental nature"""
   ```

2. **Add missing SFM-specific categories**:
   ```python
   class PowerResourceType(Enum):
       INSTITUTIONAL_AUTHORITY = auto()
       ECONOMIC_CONTROL = auto()
       INFORMATION_ACCESS = auto()
       NETWORK_POSITION = auto()
       CULTURAL_LEGITIMACY = auto()
   ```

### Acceptance Criteria
- [ ] Review Hayden's SFM literature for missing concepts
- [ ] Add ceremonial/instrumental metadata to relationships
- [ ] Create power resource type enum
- [ ] Add tool-skill-technology complex enums
- [ ] Validate alignment with SFM theory
