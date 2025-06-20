# Core Module Documentation

This directory contains the fundamental data structures and analysis tools for the Social Fabric Matrix (SFM) framework.

## Files Overview

### `sfm_models.py`
Defines the core data classes for representing SFM entities and their relationships. These classes form the building blocks of any SFM analysis.

### `enums.py`
Contains enumeration definitions that provide controlled vocabularies for categorizing entities and relationships. These ensure consistent data classification across different analyses.

### `sfm_query.py`
Provides the query engine abstraction and NetworkX implementation for analyzing SFM graphs. This enables complex network analysis and policy impact assessment.

### `sfm_service.py`
Provides a unified facade service that simplifies interaction with the SFM framework. This is the recommended entry point for most users, offering high-level operations without requiring direct manipulation of repositories or query engines.

## Core Data Model

The SFM framework models socio-economic systems as networks of interconnected entities. Here are the main components:

### Node Types (Entities)

```
Node (Base Class)
├── Actor           # Decision-making entities (agencies, firms, individuals)
├── Institution     # Rules and organizations
│   └── Policy      # Specific interventions
├── Resource        # Stocks and assets
├── Process         # Transformation activities
├── Flow            # Quantified transfers
├── Indicator       # Performance measures
└── Other specialized types...
```

### Dimensional Entities

```
TimeSlice    # Temporal context (e.g., "Q1-2025")
SpatialUnit  # Geographic boundaries (e.g., "US-WA-SEATTLE")
Scenario     # Policy alternatives (e.g., "Carbon Tax 2026")
```

### Relationships

Relationships connect entities with typed, weighted connections:

```
Relationship
├── source_id: UUID
├── target_id: UUID
├── kind: RelationshipKind
├── weight: float
└── dimensional context (time, space, scenario)
```

## Example SFM Matrix Structure

Here's a simplified representation of how entities relate in a grain market analysis:

```
           USDA  Farmers  Traders  Grain  Subsidy
USDA        -      0.8      -       -      0.9
Farmers     -       -      0.6     0.7     -
Traders     -       -       -      0.5     -
Grain       -       -       -       -      -
Subsidy    0.5     0.8      -       -      -
```

Where values represent relationship weights (e.g., influence strength, flow volume).

## Basic Usage Example

```python
from core.sfm_models import SFMGraph, Actor, Resource, Relationship
from core.enums import RelationshipKind, ResourceType

# Create entities
government = Actor(label="Government", sector="Public")
grain = Resource(label="Wheat", rtype=ResourceType.PRODUCED)

# Create relationship
regulation = Relationship(
    source_id=government.id,
    target_id=grain.id,
    kind=RelationshipKind.REGULATES,
    weight=0.7
)

# Build graph
graph = SFMGraph(name="Simple Market Model")
graph.add_node(government)
graph.add_node(grain)
graph.add_relationship(regulation)
```

## Quick Start with SFM Service

The `SFMService` class provides the easiest way to work with SFM graphs:

```python
from core.sfm_service import SFMService

# Create service instance
service = SFMService()

# Create entities
usda = service.create_actor(
    name="USDA", 
    description="US Department of Agriculture",
    sector="government"
)

farm_bill = service.create_policy(
    name="Farm Bill 2023",
    description="Agricultural support legislation",
    authority="US Congress"
)

wheat = service.create_resource(
    name="Winter Wheat",
    description="Primary grain crop",
    rtype=ResourceType.BIOLOGICAL,
    unit="bushels"
)

# Create relationships
service.connect(usda.id, farm_bill.id, "IMPLEMENTS")
service.connect(farm_bill.id, wheat.id, "REGULATES")

# Analyze the network
stats = service.get_statistics()
central_actors = service.find_most_influential_actors()
path = service.find_shortest_path(usda.id, wheat.id)

print(f"Graph has {stats['total_nodes']} nodes and {stats['total_relationships']} relationships")
```

## Entity Relationship Diagram

```
    Actor ────────────────┐
      │                   │
      │ governs           │ affects
      ▼                   ▼
  Institution ──────► Resource
      │                   ▲
      │ implements        │ uses
      ▼                   │
    Policy ──────────► Process
      │                   │
      │ creates           │ produces
      ▼                   ▼
    Flow ◄─────────────► Indicator
```

## Relationship Types (Key Examples)

From `enums.py`, relationships are categorized by function:

- **Governance**: GOVERNS, REGULATES, AUTHORIZES
- **Economic**: FUNDS, PAYS, TRADES, PRODUCES
- **Information**: INFORMS, ANALYZES, COMMUNICATES
- **Process**: TRANSFORMS, EXTRACTS, OPERATES

## Query Engine Capabilities

The `sfm_query.py` module provides analysis functions:

### Network Analysis
- Node centrality calculations
- Shortest path finding
- Community detection

### Policy Analysis
- Impact radius assessment
- Target identification
- Scenario comparison

### Flow Analysis
- Resource flow tracing
- Bottleneck identification
- Efficiency calculations

## Simple Matrix Creation Process

1. **Define Entities**: Create actors, institutions, resources, etc.
2. **Establish Relationships**: Connect entities with typed relationships
3. **Build Graph**: Use `SFMGraph` to organize the network
4. **Generate Matrix**: Filter relationships by type and aggregate weights
5. **Analyze**: Use query engine for network analysis
