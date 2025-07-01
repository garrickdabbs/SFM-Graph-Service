# SFM Enum Error Handling and Validation Guide

This document describes the error handling and validation utilities added to the SFM (Social Fabric Matrix) enum module to ensure data consistency and provide helpful feedback when incompatible enum combinations are used.

## Overview

The SFM enum validation system provides:

1. **Custom exception hierarchy** for enum-related errors
2. **Context-aware validation** for enum combinations
3. **Comprehensive error messages** with suggestions
4. **Validation decorators** for model methods
5. **Automatic validation** in model constructors

## Exception Hierarchy

### SFMEnumError
Base exception for all SFM enum-related errors.

```python
from core.sfm_enums import SFMEnumError
```

### IncompatibleEnumError
Raised when incompatible enum values are used together.

```python
from core.sfm_enums import IncompatibleEnumError
```

### InvalidEnumOperationError
Raised when an invalid operation is attempted on enum values.

```python
from core.sfm_enums import InvalidEnumOperationError
```

## EnumValidator Class

The `EnumValidator` class provides static methods for validating enum combinations:

### Relationship Context Validation

Validates that relationship types make sense between different node types:

```python
from core.sfm_enums import EnumValidator, RelationshipKind

# Valid combination
EnumValidator.validate_relationship_context(
    RelationshipKind.GOVERNS, 'Actor', 'Institution'
)  # ✓ Passes

# Invalid combination
try:
    EnumValidator.validate_relationship_context(
        RelationshipKind.GOVERNS, 'Actor', 'Resource'
    )
except IncompatibleEnumError as e:
    print(f"Error: {e}")
    # Error: GOVERNS relationship requires Actor->Actor, Actor->Institution, 
    # or Institution relationships. Got Actor->Resource. 
    # Suggestions: For Actor sources, valid targets are: Actor, Institution, Policy
```

### Flow Combination Validation

Validates that flow nature and type combinations make sense:

```python
from core.sfm_enums import FlowNature, FlowType

# Valid combination
EnumValidator.validate_flow_combination(
    FlowNature.FINANCIAL, FlowType.FINANCIAL
)  # ✓ Passes

# Invalid combination
try:
    EnumValidator.validate_flow_combination(
        FlowNature.FINANCIAL, FlowType.MATERIAL
    )
except IncompatibleEnumError as e:
    print(f"Error: {e}")
    # Error: Flow nature FINANCIAL is incompatible with flow type MATERIAL. 
    # Consider using compatible combinations like FINANCIAL with FINANCIAL type...
```

### Institution Layer Validation

Validates that institution layers are appropriate for institution types:

```python
from core.sfm_enums import InstitutionLayer

# Valid combination
EnumValidator.validate_institution_layer_context(
    InstitutionLayer.FORMAL_RULE, 'Institution'
)  # ✓ Passes

# Potentially problematic combination
try:
    EnumValidator.validate_institution_layer_context(
        InstitutionLayer.FORMAL_RULE, 'BeliefSystem'
    )
except IncompatibleEnumError as e:
    print(f"Warning: {e}")
    # Warning: FORMAL_RULE layer is typically not appropriate for BeliefSystem. 
    # Consider using CULTURAL_VALUE or KNOWLEDGE_SYSTEM layers...
```

## Automatic Model Validation

### Flow Validation

Flow objects automatically validate their nature and type combination:

```python
from core.sfm_models import Flow
from core.sfm_enums import FlowNature, FlowType

# Valid flow
flow = Flow(
    label="Valid Financial Flow",
    nature=FlowNature.FINANCIAL,
    flow_type=FlowType.FINANCIAL
)  # ✓ Creates successfully

# Invalid flow
try:
    flow = Flow(
        label="Invalid Flow",
        nature=FlowNature.FINANCIAL,
        flow_type=FlowType.MATERIAL
    )
except IncompatibleEnumError as e:
    print(f"Flow creation failed: {e}")
```

### SFMGraph Relationship Validation

The SFMGraph automatically validates relationships when they are added:

```python
from core.sfm_models import SFMGraph, Actor, Resource, Relationship
from core.sfm_enums import RelationshipKind

graph = SFMGraph(name="Test Graph")
actor = Actor(label="Test Actor")
resource = Resource(label="Test Resource", rtype=ResourceType.NATURAL)

graph.add_node(actor)
graph.add_node(resource)

# Invalid relationship
try:
    relationship = Relationship(
        source_id=actor.id,
        target_id=resource.id,
        kind=RelationshipKind.GOVERNS
    )
    graph.add_relationship(relationship)
except IncompatibleEnumError as e:
    print(f"Relationship rejected: {e}")
    # Relationship rejected: GOVERNS relationship requires Actor->Actor, 
    # Actor->Institution, or Institution relationships. Got Actor->Resource...
```

## Validation Rules

### Relationship Context Rules

The following relationship validation rules are enforced:

#### GOVERNS Relationship
- **Valid combinations**: Actor→Actor, Actor→Institution, Actor→Policy, Institution→Institution, Institution→Actor, Policy→Actor
- **Invalid**: Actor→Resource, Resource→Actor, Process→Resource, etc.
- **Rationale**: Governance requires authority-capable entities

#### EMPLOYS Relationship
- **Valid combinations**: Actor→Actor only
- **Invalid**: Institution→Actor, Actor→Resource, etc.
- **Rationale**: Employment is a direct Actor-to-Actor relationship

#### OWNS Relationship
- **Valid combinations**: Actor→Resource, Institution→Resource, Actor→TechnologySystem, Institution→TechnologySystem
- **Invalid**: Resource→Actor, Process→Resource, etc.
- **Rationale**: Ownership requires entities capable of ownership and ownable resources

#### USES Relationship
- **Valid combinations**: Actor→Resource, Process→Resource, Actor→TechnologySystem, Process→TechnologySystem, Actor→Institution, Process→Institution
- **Invalid**: Resource→Actor, etc.
- **Rationale**: Usage requires a user and a usable entity

#### PRODUCES Relationship
- **Valid combinations**: Actor→Resource, Process→Resource, TechnologySystem→Resource, Actor→Flow, Process→Flow, TechnologySystem→Flow
- **Invalid**: Resource→Actor, etc.
- **Rationale**: Production requires a producer and a producible output

### Flow Combination Rules

The following flow nature and type combinations are considered incompatible:

- FINANCIAL nature with MATERIAL type
- MATERIAL nature with FINANCIAL type  
- ENERGY nature with INFORMATION type
- INFORMATION nature with ENERGY type

### Institution Layer Rules

- FORMAL_RULE layers are flagged as potentially inappropriate for BeliefSystem and ValueSystem entities
- Suggestions are provided for more appropriate layers (CULTURAL_VALUE, KNOWLEDGE_SYSTEM)

## Validation Decorator

Use the `@validate_enum_operation` decorator to add validation to custom functions:

```python
from core.sfm_enums import validate_enum_operation

@validate_enum_operation("custom_relationship_creation")
def create_custom_relationship(kind, source, target):
    # Your custom logic here
    if kind == RelationshipKind.CUSTOM:
        raise ValueError("Custom logic error")
    return Relationship(source_id=source.id, target_id=target.id, kind=kind)

# Usage
try:
    rel = create_custom_relationship(RelationshipKind.CUSTOM, actor1, actor2)
except InvalidEnumOperationError as e:
    print(f"Operation failed: {e}")
    # Operation failed: Invalid custom_relationship_creation operation: Custom logic error
```

## Error Message Features

All validation errors provide:

1. **Clear problem description**: What went wrong
2. **Context information**: The specific combination that failed
3. **Helpful suggestions**: Valid alternatives or next steps
4. **Relevant examples**: When applicable

## Best Practices

1. **Always handle IncompatibleEnumError** when creating relationships or flows programmatically
2. **Use try-catch blocks** around model creation when enum combinations might be invalid
3. **Pay attention to error suggestions** - they provide guidance for valid alternatives
4. **Validate early** - catch invalid combinations as close to the source as possible
5. **Test edge cases** - verify that your code handles validation errors gracefully

## Testing

The validation system includes comprehensive tests in `tests/test_enum_validation.py`. Run them with:

```bash
python -m unittest tests.test_enum_validation -v
```

## Future Extensions

The validation system is designed to be extensible. To add new validation rules:

1. Add the rule to `EnumValidator.RELATIONSHIP_RULES` or create a new validation method
2. Update the error messages and suggestions
3. Add corresponding tests
4. Update this documentation

## Integration with Existing Code

The validation system is designed to be minimally intrusive:

- Existing code continues to work unchanged
- Validation only activates when creating new relationships or flows
- Error messages are informative and actionable
- Performance impact is minimal

This ensures backward compatibility while providing better data quality for new SFM models.