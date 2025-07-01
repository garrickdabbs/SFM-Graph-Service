# Medium Priority Issues - SFM Enums Module

## Issue #8: Enum Organization and Grouping (MEDIUM)
**Priority**: 🟡 Medium  
**Labels**: `organization`, `readability`, `maintainability`  
**Estimated Effort**: Low-Medium  

### Problem
Large enums are difficult to navigate and understand:

1. **ValueCategory** (68 values) lacks logical grouping
2. **RelationshipKind** (148 values) needs section organization  
3. **ResourceType** categories are mixed without clear hierarchy
4. **FlowNature** combines different conceptual dimensions

### Current State - No Clear Organization
```python
class ValueCategory(Enum):
    ECONOMIC = auto()
    SOCIAL = auto() 
    ENVIRONMENTAL = auto()
    # ... 65 more values in no particular order
```

### Proposed Solution - Add Section Comments
```python
class ValueCategory(Enum):
    """Value categories for Social Fabric Matrix analysis."""
    
    # ═══════════════════════════════════════════════════════════
    # CORE HAYDEN FRAMEWORK VALUES
    # ═══════════════════════════════════════════════════════════
    ECONOMIC = auto()        # Market-priced goods, services, financial returns
    SOCIAL = auto()          # Distributional equity, social cohesion, well-being  
    ENVIRONMENTAL = auto()   # Resource stocks, ecological integrity
    CULTURAL = auto()        # Norms, beliefs, heritage
    INSTITUTIONAL = auto()   # Governance quality, rule consistency
    TECHNOLOGICAL = auto()   # Knowledge base, production techniques
    
    # ═══════════════════════════════════════════════════════════
    # GOVERNANCE AND POLITICAL VALUES
    # ═══════════════════════════════════════════════════════════
    POLITICAL = auto()       # Power distribution, democratic participation
    LEGAL = auto()           # Legal frameworks, rights, justice, compliance
    TRANSPARENCY = auto()    # Openness, accountability, information access
    PARTICIPATION = auto()   # Stakeholder involvement, democratic engagement
    ACCOUNTABILITY = auto()  # Responsibility, oversight, governance
    LEGITIMACY = auto()      # Acceptance, authority, credibility
    
    # ═══════════════════════════════════════════════════════════
    # SYSTEM PERFORMANCE VALUES  
    # ═══════════════════════════════════════════════════════════
    EFFICIENCY = auto()      # Resource optimization, productivity
    EFFECTIVENESS = auto()   # Goal achievement, impact, outcomes
    RESILIENCE = auto()      # Adaptability, recovery capacity, robustness
    SUSTAINABILITY = auto()  # Long-term viability, resource preservation
```

### Acceptance Criteria
- [ ] Add logical section comments to all large enums
- [ ] Group related enum values together
- [ ] Create hierarchical organization where appropriate
- [ ] Update documentation to explain grouping rationale
- [ ] Consider creating sub-enums for major sections

---

## Issue #9: Enum Hierarchy and Relationships (MEDIUM)
**Priority**: 🟡 Medium  
**Labels**: `architecture`, `relationships`, `enhancement`  
**Estimated Effort**: Medium  

### Problem
Some enum values have implicit hierarchical relationships that should be explicit:

1. **Resource type hierarchies**: `NATURAL` → `LAND`, `WATER`, `MINERAL`
2. **Value category relationships**: Core values vs derived values  
3. **Flow nature dependencies**: Some flows require specific resource types
4. **Relationship strength indicators**: Some relationships are stronger than others

### Solution
Add enum relationship methods:

```python
class ResourceType(Enum):
    # Parent categories
    NATURAL = auto()
    PRODUCED = auto()
    HUMAN = auto()
    
    # Natural subcategories  
    LAND = auto()
    WATER = auto()
    MINERAL = auto()
    BIOLOGICAL = auto()
    
    def is_subcategory_of(self, parent: 'ResourceType') -> bool:
        """Check if this resource type is a subcategory of parent."""
        subcategories = {
            ResourceType.NATURAL: [ResourceType.LAND, ResourceType.WATER, 
                                 ResourceType.MINERAL, ResourceType.BIOLOGICAL],
            ResourceType.PRODUCED: [ResourceType.BUILT, ResourceType.UTILITY],
            # ...
        }
        return self in subcategories.get(parent, [])
    
    @property
    def parent_category(self) -> Optional['ResourceType']:
        """Get the parent category for this resource type."""
        for parent, children in self._hierarchy.items():
            if self in children:
                return parent
        return None
```

### Acceptance Criteria
- [ ] Define explicit hierarchies for resource types
- [ ] Add parent-child relationship methods
- [ ] Create compatibility checking between related enums
- [ ] Document enum relationships in module docstring
- [ ] Add tests for hierarchical relationships

---

## Issue #10: Better String Representations (MEDIUM)
**Priority**: 🟡 Medium  
**Labels**: `usability`, `debugging`, `string-representation`  
**Estimated Effort**: Low  

### Problem
Default enum string representations are not user-friendly:

```python
>>> str(ValueCategory.ECONOMIC)
'ValueCategory.ECONOMIC'
>>> repr(RelationshipKind.GOVERNS)  
'<RelationshipKind.GOVERNS: 1>'
```

Better representations would help with:
- **Debugging and logging**
- **User interface display**  
- **Database storage and serialization**
- **API responses**

### Solution
Add custom string methods:

```python
class ValueCategory(Enum):
    ECONOMIC = auto()
    SOCIAL = auto()
    
    def __str__(self) -> str:
        """Return human-readable string representation."""
        descriptions = {
            ValueCategory.ECONOMIC: "Economic Value",
            ValueCategory.SOCIAL: "Social Value",
            # ...
        }
        return descriptions.get(self, self.name.replace('_', ' ').title())
    
    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"{self.__class__.__name__}.{self.name}"
    
    @property
    def description(self) -> str:
        """Get detailed description of this value category."""
        descriptions = {
            ValueCategory.ECONOMIC: "Market-priced goods, services, and financial returns",
            ValueCategory.SOCIAL: "Distributional equity, social cohesion, and well-being",
            # ...
        }
        return descriptions.get(self, "No description available")
```

### Acceptance Criteria
- [ ] Add custom `__str__` methods to all enum classes
- [ ] Add `description` property for detailed explanations
- [ ] Create human-readable representations for UI display
- [ ] Add internationalization support structure
- [ ] Update logging and debugging to use new representations

---

## Issue #11: Enum Performance Optimization (MEDIUM)
**Priority**: 🟡 Medium  
**Labels**: `performance`, `optimization`, `lazy-loading`  
**Estimated Effort**: Medium  

### Problem
Large enums impact performance:

1. **Memory usage**: All enum values loaded at import time
2. **Import time**: Large enums slow down module loading
3. **Serialization**: Converting large enums to/from JSON is slow
4. **Comparison operations**: Many enum comparisons in tight loops

### Solution
Implement performance optimizations:

```python
# Lazy loading for enum descriptions
class ValueCategory(Enum):
    ECONOMIC = auto()
    SOCIAL = auto()
    
    _descriptions = None  # Loaded only when needed
    
    @property  
    def description(self) -> str:
        if ValueCategory._descriptions is None:
            ValueCategory._descriptions = self._load_descriptions()
        return ValueCategory._descriptions[self]
    
    @classmethod
    def _load_descriptions(cls) -> Dict['ValueCategory', str]:
        """Load descriptions only when first accessed."""
        # Load from file or define inline
        return {...}
```

### Performance Targets
- Reduce memory usage by 30-50%
- Improve import time by 20%  
- Optimize serialization performance
- Add caching for frequently used enum operations

### Acceptance Criteria
- [ ] Implement lazy loading for enum metadata
- [ ] Add caching for expensive enum operations
- [ ] Benchmark performance improvements
- [ ] Add performance regression tests
- [ ] Document performance characteristics

---

## Issue #12: Missing SFM-Specific Enums (MEDIUM)
**Priority**: 🟡 Medium  
**Labels**: `enhancement`, `sfm-theory`, `completeness`  
**Estimated Effort**: Medium  

### Problem
Several SFM concepts referenced in models lack corresponding enums:

1. **Technology Readiness Levels** (referenced in `TechnologySystem.maturity`)
2. **Legitimacy Sources** (referenced in `ValueSystem.legitimacy_source`)  
3. **Authority Types** (Weber's traditional/charismatic/legal-rational)
4. **Path dependency types and strength levels**
5. **Institutional change mechanisms**

### Solution
Add missing SFM-specific enums:

```python
class TechnologyReadinessLevel(Enum):
    """NASA Technology Readiness Levels adapted for SFM."""
    BASIC_PRINCIPLES = 1        # Basic principles observed
    TECHNOLOGY_CONCEPT = 2      # Technology concept formulated  
    EXPERIMENTAL_PROOF = 3      # Experimental proof of concept
    LABORATORY_VALIDATION = 4   # Technology validated in lab
    RELEVANT_ENVIRONMENT = 5    # Technology validated in relevant environment
    DEMONSTRATION = 6           # Technology demonstrated in relevant environment  
    PROTOTYPE_DEMONSTRATION = 7 # System prototype demonstration
    SYSTEM_COMPLETE = 8         # System complete and qualified
    ACTUAL_SYSTEM = 9          # Actual system proven in operational environment

class LegitimacySource(Enum):
    """Weber's types of authority/legitimacy."""
    TRADITIONAL = auto()        # Custom, precedent, "eternal yesterday"
    CHARISMATIC = auto()        # Personal qualities of leader
    LEGAL_RATIONAL = auto()     # Rules, procedures, offices
    EXPERT = auto()            # Technical knowledge and competence
    DEMOCRATIC = auto()         # Popular consent and participation

class PathDependencyStrength(Enum):
    """Strength of institutional path dependencies."""
    WEAK = auto()              # Easy to change, low switching costs
    MODERATE = auto()          # Some resistance, moderate costs  
    STRONG = auto()            # High resistance, high switching costs
    LOCKED_IN = auto()         # Extremely difficult to change
```

### Acceptance Criteria
- [ ] Create all missing SFM-specific enums
- [ ] Update models to use new enums instead of strings
- [ ] Add comprehensive documentation with SFM theory references
- [ ] Update existing data migration scripts
- [ ] Add validation for new enum usage
