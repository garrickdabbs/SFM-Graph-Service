# Hayden SFM Framework Alignment Documentation

## Overview

This document describes the implementation of enhancements to align the SFM enums module with F. Gregory Hayden's Social Fabric Matrix framework, addressing Issue #46.

## Key Enhancements

### 1. Ceremonial vs. Instrumental Categorization

Added a `ceremonial_tendency` property to the `RelationshipKind` enum that returns a float value from 0.0 to 1.0, indicating the ceremonial vs. instrumental nature of relationships.

**Scale:**
- **0.0-0.2**: Highly instrumental (problem-solving, adaptive, productive)
- **0.2-0.5**: Moderately instrumental (some adaptation with structure)
- **0.5-0.8**: Moderately ceremonial (mixed institutional/adaptive)
- **0.8-1.0**: Highly ceremonial (status, tradition, hierarchy)

**Examples:**
```python
from core.sfm_enums import RelationshipKind

# Highly ceremonial
RelationshipKind.CEREMONIALLY_REINFORCES.ceremonial_tendency  # 0.95
RelationshipKind.LEGITIMIZES.ceremonial_tendency              # 0.85
RelationshipKind.GOVERNS.ceremonial_tendency                  # 0.75

# Highly instrumental  
RelationshipKind.INSTRUMENTALLY_ADAPTS.ceremonial_tendency    # 0.05
RelationshipKind.SOLVES.ceremonial_tendency                   # 0.05
RelationshipKind.PRODUCES.ceremonial_tendency                 # 0.15
```

### 2. PowerResourceType Enum

New enum for classifying power dynamics in institutional systems:

```python
class PowerResourceType(Enum):
    INSTITUTIONAL_AUTHORITY = auto()  # Formal authority roles and positions
    ECONOMIC_CONTROL = auto()         # Control over financial resources and flows
    INFORMATION_ACCESS = auto()       # Access to and control of information
    NETWORK_POSITION = auto()         # Strategic position within networks
    CULTURAL_LEGITIMACY = auto()      # Cultural authority and legitimacy sources
```

### 3. ToolSkillTechnologyType Enum

Represents Hayden's tool-skill-technology complex:

```python
class ToolSkillTechnologyType(Enum):
    PHYSICAL_TOOL = auto()            # Material instruments and devices
    COGNITIVE_SKILL = auto()          # Mental capabilities and knowledge
    TECHNOLOGY_SYSTEM = auto()        # Integrated technological arrangements
    TECHNIQUE = auto()                # Specific methods and procedures
    METHODOLOGY = auto()              # Systematic approaches and frameworks
    CRAFT_KNOWLEDGE = auto()          # Embodied practical knowledge
    DIGITAL_CAPABILITY = auto()       # Digital tools and skills
    ANALYTICAL_METHOD = auto()        # Formal analytical techniques
    PROBLEM_SOLVING_APPROACH = auto() # General problem-solving strategies
    INNOVATION_CAPACITY = auto()      # Capability to create new solutions
```

### 4. PathDependencyType Enum

Classification of institutional path dependency strength:

```python
class PathDependencyType(Enum):
    WEAK = auto()      # Easy to change, low switching costs
    MODERATE = auto()  # Some resistance, moderate switching costs
    STRONG = auto()    # High resistance, significant switching costs
    LOCKED_IN = auto() # Extremely difficult to change
```

### 5. InstitutionalChangeType Enum

Patterns of institutional change and evolution:

```python
class InstitutionalChangeType(Enum):
    INCREMENTAL = auto()      # Gradual, small-scale adjustments
    TRANSFORMATIONAL = auto() # Significant structural changes
    REVOLUTIONARY = auto()    # Rapid, fundamental system overhaul
    EVOLUTIONARY = auto()     # Organic adaptation over time
    ADAPTIVE = auto()         # Responsive changes to environmental pressures
    CRISIS_DRIVEN = auto()    # Changes triggered by system crises
    INNOVATION_LED = auto()   # Changes driven by innovation
    REFORM_BASED = auto()     # Planned, policy-driven changes
    EMERGENT = auto()         # Bottom-up, spontaneous changes
    CYCLICAL = auto()         # Recurring patterns of change and stability
```

## Usage Examples

### Analyzing Ceremonial vs. Instrumental Patterns

```python
from core.sfm_enums import RelationshipKind

# Identify highly ceremonial relationships in a system
ceremonial_relationships = [
    rel for rel in RelationshipKind 
    if rel.ceremonial_tendency > 0.7
]

# Identify highly instrumental relationships
instrumental_relationships = [
    rel for rel in RelationshipKind 
    if rel.ceremonial_tendency < 0.3
]

# Calculate average ceremonial tendency for a set of relationships
relationships = [RelationshipKind.GOVERNS, RelationshipKind.PRODUCES, RelationshipKind.EDUCATES]
avg_ceremonial = sum(rel.ceremonial_tendency for rel in relationships) / len(relationships)
```

### Power Analysis

```python
from core.sfm_enums import PowerResourceType

# Analyze power resource distribution
power_resources = {
    'actor_1': [PowerResourceType.INSTITUTIONAL_AUTHORITY, PowerResourceType.ECONOMIC_CONTROL],
    'actor_2': [PowerResourceType.INFORMATION_ACCESS, PowerResourceType.NETWORK_POSITION],
    'actor_3': [PowerResourceType.CULTURAL_LEGITIMACY]
}
```

### Tool-Skill-Technology Analysis

```python
from core.sfm_enums import ToolSkillTechnologyType

# Categorize system capabilities
system_capabilities = {
    'manufacturing': [ToolSkillTechnologyType.PHYSICAL_TOOL, ToolSkillTechnologyType.TECHNIQUE],
    'research': [ToolSkillTechnologyType.ANALYTICAL_METHOD, ToolSkillTechnologyType.COGNITIVE_SKILL],
    'innovation': [ToolSkillTechnologyType.INNOVATION_CAPACITY, ToolSkillTechnologyType.METHODOLOGY]
}
```

## Theoretical Alignment

This implementation aligns with Hayden's SFM framework by:

1. **Distinguishing ceremonial from instrumental behaviors** - The ceremonial_tendency property enables quantitative analysis of institutional vs. problem-solving orientations.

2. **Capturing power dynamics** - PowerResourceType provides categories for analyzing different forms of institutional power and control.

3. **Representing integrated technology systems** - ToolSkillTechnologyType reflects Hayden's concept of technology as integrated tool-skill-knowledge complexes.

4. **Modeling path dependency** - PathDependencyType enables analysis of institutional lock-in and resistance to change.

5. **Categorizing change patterns** - InstitutionalChangeType provides vocabulary for different modes of institutional evolution.

## Testing and Validation

The implementation has been validated through:

- **Unit tests** for all new enums and properties
- **Integration tests** to ensure compatibility with existing functionality
- **Range validation** for ceremonial_tendency values (0.0-1.0)
- **Logical consistency** tests for ceremonial vs. instrumental categorization
- **Completeness checks** for all required enum values

## Future Extensions

This foundation enables future enhancements such as:

- **Quantitative SFM analysis** using ceremonial tendency scores
- **Power network analysis** using PowerResourceType classifications
- **Technology system modeling** with ToolSkillTechnologyType components
- **Institutional evolution tracking** using change type patterns
- **Path dependency strength analysis** for system resilience assessment