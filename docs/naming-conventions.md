# SFM Enums Naming Conventions

This document establishes naming standards for all enumerations in the Social Fabric Matrix (SFM) framework to ensure consistency, clarity, and maintainability.

## General Principles

### 1. Descriptive and Unambiguous
- Enum values should clearly describe their meaning
- Avoid abbreviations unless they are widely understood
- Use full words over contractions

### 2. Consistent Capitalization
- All enum values use `SCREAMING_SNAKE_CASE`
- Words separated by underscores
- No mixed case or camelCase

### 3. Singular Forms
- Use singular nouns consistently: `FORMAL_RULE` not `FORMAL_RULES`
- Exception: When the concept is inherently plural (e.g., `ENFORCEMENT_MECHANISMS`)

## Relationship Naming Standards

### Verb Tense Consistency
- Use **present active voice** for actions: `GOVERNS`, `FUNDS`, `REGULATES`
- Avoid passive voice: `GOVERNED_BY`, `FUNDED_BY` (use active alternatives)
- Use consistent tense across related relationships

### Preposition Usage Patterns

#### Symmetric Relationships (mutual/bidirectional)
Use `_WITH` for relationships that are inherently mutual:
```python
COLLABORATES_WITH = auto()  # Actor A collaborates with Actor B (mutual)
COMPETES_WITH = auto()      # Actor A competes with Actor B (mutual)
COORDINATES_WITH = auto()   # Actor A coordinates with Actor B (mutual)
EXCHANGES_WITH = auto()     # Actor A exchanges with Actor B (mutual)
```

#### Directional Relationships (source to target)
Use `_TO` for relationships that flow toward a target:
```python
SELLS_TO = auto()          # Actor A sells to Actor B (A→B)
TRANSITIONS_TO = auto()    # Actor A transitions to state B (A→B)
ACCOUNTABLE_TO = auto()    # Actor A is accountable to Actor B (A→B)
DELEGATES_TO = auto()      # Actor A delegates to Actor B (A→B)
```

#### Source Relationships (origin from source)
Use `_FROM` for relationships that indicate origin or source:
```python
BUYS_FROM = auto()         # Actor A buys from Actor B (A←B)
EMERGES_FROM = auto()      # Actor A emerges from Actor B (A←B)
BENEFITS_FROM = auto()     # Actor A benefits from Actor B (A←B)
LEARNS_FROM = auto()       # Actor A learns from Actor B (A←B)
```

#### Simple Actions (no preposition needed)
Use no preposition for direct action verbs:
```python
GOVERNS = auto()           # Actor A governs Actor B
FUNDS = auto()             # Actor A funds Actor B
REGULATES = auto()         # Actor A regulates Actor B
PRODUCES = auto()          # Actor A produces Resource B
```

### Relationship Direction Guidelines

1. **Active Voice Preferred**: Use the perspective of the source entity
   - `GOVERNS` (government governs institution)
   - `SUPPLIES` (supplier supplies manufacturer)

2. **Consistent Perspective**: Maintain source-to-target perspective
   - Good: `TEACHES` (teacher teaches student)
   - Avoid: `TAUGHT_BY` (student taught by teacher)

3. **Bidirectional Relationships**: Use `_WITH` to indicate mutual action
   - `COLLABORATES_WITH` (both parties collaborate)
   - `NEGOTIATES_WITH` (both parties negotiate)

## Institution Layer Naming

### Singular Forms Required
```python
# Correct
FORMAL_RULE = auto()       # Constitutional and legal frameworks
ORGANIZATION = auto()      # Structured collective entities
INFORMAL_NORM = auto()     # Cultural practices and expectations

# Incorrect
FORMAL_RULES = auto()      # Avoid plural
ORGANIZATIONS = auto()     # Avoid plural
INFORMAL_NORMS = auto()    # Avoid plural
```

### Descriptive Specificity
- Use specific terms: `POLICY_INSTRUMENT` not `POLICY`
- Include context when helpful: `MARKET_MECHANISM` not `MECHANISM`
- Avoid overly generic terms: `HYBRID_INSTITUTION` not `HYBRID`

## Value Category Naming

### Conceptual Clarity
- Use established economic/social terms when possible
- Avoid overlapping concepts:
  - Use `EFFICIENCY` OR `PERFORMANCE`, not both
  - Use `COMMUNICATION` OR `INFORMATIONAL`, not both

### Scope Indication
- Distinguish between similar concepts with scope qualifiers:
  - `SOCIAL_CAPITAL` vs `FINANCIAL_CAPITAL`
  - `CULTURAL_VALUE` vs `ECONOMIC_VALUE`

## Resource Type Naming

### Hierarchical Consistency
- Use consistent patterns for related types:
  - `NATURAL`, `PRODUCED`, `HUMAN` (capability types)
  - `FINANCIAL`, `INTELLECTUAL`, `SOCIAL_CAPITAL` (capital types)

### Material vs Abstract Distinction
- Clear separation between physical and abstract resources
- Use qualifiers when needed: `BUILT` vs `DIGITAL`

## Validation Rules

### Automated Checks
1. **No Passive Voice**: Flag `_BY` endings for review
2. **Preposition Consistency**: Verify `_WITH/_TO/_FROM` usage follows patterns
3. **Singular Forms**: Flag plural endings (`_S`, `_ES`) for review
4. **Reserved Terms**: Prevent use of ambiguous terms

### Manual Review Required
- New enum values must be reviewed for naming consistency
- Changes to existing values require deprecation planning
- Cross-enum relationships should be validated

## Migration and Deprecation

### Adding New Values
1. Follow naming conventions strictly
2. Add comprehensive documentation
3. Include usage examples
4. Update validation rules if needed

### Changing Existing Values
1. Add new value with correct naming
2. Mark old value as deprecated with warning
3. Update all code references gradually
4. Remove deprecated value in next major version

### Deprecation Warning Format
```python
@deprecated_enum_value("Use NEW_VALUE instead")
OLD_VALUE = auto()  # Deprecated: Use NEW_VALUE

NEW_VALUE = auto()  # Replacement for OLD_VALUE
```

## Examples

### Good Naming Examples
```python
# Clear, consistent, active voice
GOVERNS = auto()           # Government authority relationship
FUNDS = auto()             # Financial provision relationship
COLLABORATES_WITH = auto() # Mutual cooperation relationship
EMERGES_FROM = auto()      # Origin/source relationship

# Consistent institution layers
FORMAL_RULE = auto()       # Singular, specific
POLICY_INSTRUMENT = auto() # Singular, descriptive
MARKET_MECHANISM = auto()  # Singular, qualified
```

### Naming to Avoid
```python
# Passive voice
GOVERNED_BY = auto()       # Use GOVERNS instead
FUNDED_BY = auto()         # Use FUNDS instead

# Inconsistent plurals
FORMAL_RULES = auto()      # Use FORMAL_RULE instead
POLICY_INSTRUMENTS = auto() # Use POLICY_INSTRUMENT instead

# Inconsistent prepositions
COLLABORATES_TO = auto()   # Use COLLABORATES_WITH instead
BENEFITS_WITH = auto()     # Use BENEFITS_FROM instead
```

## Tool Support

### Linting Rules
- Custom pylint rules to enforce naming patterns
- Pre-commit hooks to validate new enum values
- Automated tests for naming convention compliance

### Documentation Generation
- Automatic cross-references between related enums
- Consistency reports for maintenance
- Usage pattern analysis

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Status**: Active