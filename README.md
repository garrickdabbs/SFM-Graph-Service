# Social Fabric Matrix Graph Service

An experimental Python framework for implementing F. Gregory Hayden's Social Fabric Matrix (SFM) methodology, providing tools for modeling, analyzing, and querying complex socio-economic systems through graph-based data structures.

## Overview

The Social Fabric Matrix Graph Service is an experimental software implementation of the Social Fabric Matrix framework, designed to model and analyze complex interdependencies within socio-economic systems. This framework aspires to enable researchers, policy analysts, and decision-makers to:

- **Model Complex Systems**: Represent actors, institutions, resources, processes, and their relationships in a unified graph structure
- **Analyze Policy Impacts**: Trace the effects of policy changes through interconnected networks
- **Forecast System Changes**: Use network analysis to predict outcomes of interventions
- **Query Complex Relationships**: Perform sophisticated analytical queries on system topology

What started as a graduate school project prototype has evolved into a experimental framework that attempts to implement Hayden's SFM methodology using modern software engineering practices and extensible architecture.

## Key Features

### 📊 **Experimental Data Model**
- **Actors**: Government agencies, corporations, organizations, individuals
- **Institutions**: Formal rules, organizations, informal norms (following Hayden's three-layer institutional framework)
- **Resources**: Natural resources, produced goods, financial capital, knowledge
- **Processes**: Transformation activities that convert inputs to outputs
- **Flows**: Quantified linkages between system components
- **Policies**: Formal interventions with measurable impacts
- **Relationships**: Typed connections with weights and dimensional metadata

### 🔍 **Advanced Query Engine**
- **Network Analysis**: Centrality measures, path finding, community detection
- **Policy Impact Analysis**: Trace policy effects through relationship networks
- **Flow Analysis**: Track resource flows and identify bottlenecks
- **Structural Analysis**: Identify key nodes, bridges, and vulnerable components
- **Scenario Comparison**: Compare different policy or market scenarios

### 🗄️ **Flexible Storage Layer**
- **Abstract Repository Pattern**: Extensible to multiple storage backends
- **Default NetworkX Implementation**: In-memory graph storage for rapid prototyping
- **Type-Safe Operations**: Strongly-typed repositories for different entity types
- **CRUD Operations**: Full create, read, update, delete functionality

### 📈 **Real-World Applications**
- **Commodity Market Analysis**: Forecast price changes based on policy and market conditions
- **Policy Impact Assessment**: Analyze ripple effects of regulatory changes
- **Supply Chain Resilience**: Identify vulnerabilities and dependencies
- **Economic Development Planning**: Model regional development scenarios

## Installation

### Requirements
- Python 3.8+
- NetworkX
- NumPy (for advanced calculations)

### Setup
```bash
# Clone the repository
git clone https://github.com/your-repo/SFM-Graph-Service.git
cd SFM-Graph-Service

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Quick Start

### Basic Usage
```python
from core.sfm_models import SFMGraph, Actor, Institution, Relationship
from core.enums import RelationshipKind
from db.sfm_dao import SFMRepositoryFactory
from core.sfm_query import SFMQueryFactory

# Create a repository
repo = SFMRepositoryFactory.create_repository("networkx")

# Create entities
usda = Actor(label="USDA", sector="Government")
farmers = Actor(label="Farmers Association", sector="Agriculture") 
market = Institution(label="Commodity Market")

# Add to repository
repo.create_node(usda)
repo.create_node(farmers)
repo.create_node(market)

# Create relationships
regulation = Relationship(
    source_id=usda.id,
    target_id=farmers.id,
    kind=RelationshipKind.REGULATES,
    weight=0.8
)
repo.create_relationship(regulation)

# Load into SFM graph
sfm_graph = repo.load_graph()

# Create query engine for analysis
query_engine = SFMQueryFactory.create_query_engine(sfm_graph, "networkx")

# Analyze network
central_actors = query_engine.get_most_central_nodes(Actor, "betweenness", 5)
policy_impact = query_engine.analyze_policy_impact(usda.id, impact_radius=3)
```

### Advanced Example: Grain Market Analysis
```python
from examples.us_grain_export_example import create_us_grain_market_graph

# Create experimental grain market model
repo = SFMRepositoryFactory.create_repository("networkx")
sfm_graph = SFMGraph(
    name="US Grain Market Analysis",
    description="experimental model for grain price forecasting"
)

# Build complex graph with entities and relationships
us_grain_graph = create_us_grain_market_graph(repo, sfm_graph)

# Perform sophisticated analysis
query_engine = SFMQueryFactory.create_query_engine(us_grain_graph, "networkx")

# Find system vulnerabilities
vulnerabilities = query_engine.system_vulnerability_analysis()

# Trace resource flows
grain_flows = query_engine.trace_resource_flows(ResourceType.PRODUCED)

# Analyze policy impacts
for policy_id, policy in us_grain_graph.policies.items():
    impact = query_engine.analyze_policy_impact(policy_id, impact_radius=2)
    print(f"{policy.label}: affects {impact.get('total_affected_nodes', 0)} nodes")
```

### Running the Examples
```bash
# From workspace root
python examples/us_grain_export_example.py

# Or using module syntax
python -m examples.us_grain_export_example

# For running from subfolders, examples include path resolution
python examples/us_grain_export_example.py  # Works from any directory
```

## Architecture

### Core Components

```
SFM-Graph-Service/
├── core/
│   ├── sfm_models.py      # Data model classes (Node, Actor, Institution, etc.)
│   ├── sfm_query.py       # Query engine abstractions and NetworkX implementation
│   └── enums.py           # Enumeration definitions (RelationshipKind, ResourceType, etc.)
├── db/
│   └── sfm_dao.py         # Data access layer (Repository pattern, CRUD operations)
├── examples/
│   ├── us_grain_export_example.py  # Experimental grain market model
│   └── us_grain_market_forecast.py # Market forecasting example
├── tests/
│   ├── sfm_models_test.py      # Unit tests for data models
│   ├── sfm_dao_test.py         # Unit tests for data access layer
│   └── sfm_query_test.py       # Unit tests for query engine
├── docs/
│   ├── sfm-overview.md         # Theoretical framework overview
│   └── README_SFM_GRAPH.md     # Technical documentation
└── run_query_tests.py          # Test runner for query engine
```

### Design Principles

1. **Separation of Concerns**: Clear boundaries between data models, storage, and analysis
2. **Extensibility**: Abstract interfaces allow new storage backends and analysis methods
3. **Type Safety**: Strong typing ensures data integrity and developer experience
4. **Performance**: Optimized for both small prototypes and large-scale analysis
5. **Hayden Compliance**: Faithful implementation of SFM theoretical framework

## Data Model

### Entity Hierarchy
The framework models Hayden's core SFM components:

- **Node Types**: Base classes for all system entities
  - `Actor`: Decision-making entities (agencies, firms, individuals)
  - `Institution`: Rule systems at three levels (formal, organizational, informal)
  - `Resource`: Stocks and assets (natural, produced, financial, knowledge)
  - `Process`: Transformation activities
  - `Flow`: Quantified system linkages
  - `Policy`: Specific institutional interventions
  - `Indicator`: Measurable system performance metrics

- **Relationship Types**: Semantic connections between entities
  - Governance relationships (REGULATES, AUTHORIZES, ENFORCES)
  - Economic relationships (FUNDS, TRADES, PRODUCES)
  - Information relationships (INFORMS, INFLUENCES, COMMUNICATES)
  - Process relationships (TRANSFORMS, EXTRACTS, DISTRIBUTES)

### Dimensional Entities
- **TimeSlice**: Temporal context for analysis periods
- **SpatialUnit**: Geographic boundaries and scales
- **Scenario**: Policy counterfactuals and alternative futures

## Analysis Capabilities

### Network Metrics
- **Centrality Analysis**: Identify key system nodes using betweenness, closeness, degree, and eigenvector centrality
- **Path Analysis**: Find shortest paths and alternative routes between entities
- **Community Detection**: Discover system clusters and subsystems
- **Structural Analysis**: Locate bridges, bottlenecks, and vulnerabilities

### Policy Analysis
- **Impact Propagation**: Trace policy effects through network paths
- **Scenario Modeling**: Compare baseline vs. intervention outcomes
- **Target Identification**: Find entities affected by policy changes
- **Effectiveness Measurement**: Quantify policy reach and influence

### Flow Analysis
- **Resource Tracing**: Follow materials, money, and information flows
- **Bottleneck Detection**: Identify system constraints and chokepoints
- **Efficiency Calculation**: Measure flow effectiveness and losses
- **Dependency Mapping**: Understand supply chain relationships

## Testing

The framework includes test coverage:

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test modules
python -m unittest tests.sfm_models_test -v
python -m unittest tests.sfm_dao_test -v
python -m unittest tests.sfm_query_test -v

# Run query engine specific tests
python run_query_tests.py
```

### Test Categories
- **Unit Tests**: Individual component functionality
- **Integration Tests**: Component interaction verification
- **Performance Tests**: Scalability and efficiency validation
- **Edge Case Tests**: Error handling and boundary conditions

## Examples

### US Grain Market Forecast
The [`examples/us_grain_export_example.py`](examples/us_grain_export_example.py) demonstrates:
- Experimental model of US grain commodity markets
- Policy impact analysis for agricultural regulations
- Global market condition modeling
- Advanced query operations for system analysis

**Key Features:**
- Multiple actor types (USDA, farmers, traders)
- Institution modeling (government, trade organizations)
- Resource flows (grain, land, financial)
- Policy interventions (subsidies, tariffs)
- Analytical queries (centrality, impact analysis, flow tracing)

## Theoretical Foundation

This implementation is based on F. Gregory Hayden's Social Fabric Matrix methodology, which provides:

- **Systems Perspective**: Understanding complex interdependencies
- **Institutional Analysis**: Three-layer institutional framework
- **Policy Integration**: Connecting formal policies to informal practices
- **Quantitative Assessment**: Measuring relationship strengths and impacts
- **Dynamic Modeling**: Capturing system evolution over time

### SFM Core Concepts Implemented

1. **Matrix Structure**: Entities as rows/columns, relationships as cell values
2. **Hierarchical Institution Types**: Formal rules, organizations, informal norms
3. **Flow Quantification**: Measurable transfers between system components
4. **Dimensional Analysis**: Temporal, spatial, and scenario slicing
5. **Policy Evaluation**: Systematic assessment of intervention effects

## Development

### Adding New Storage Backends

1. Implement the `SFMRepository` abstract class
2. Add factory method to `SFMRepositoryFactory`
3. Create corresponding tests
4. Update documentation

Example for Neo4j backend:
```python
class Neo4jSFMRepository(SFMRepository):
    def __init__(self, connection_string):
        # Implementation details
        pass
    
    def create_node(self, node: Node) -> Node:
        # Neo4j-specific implementation
        pass
```

### Adding New Analysis Methods

1. Extend the `SFMQueryEngine` abstract class
2. Implement in `NetworkXSFMQueryEngine`
3. Add comprehensive tests
4. Document usage patterns

## Contributing

### Development Setup
```bash
# Install in development mode
pip install -e .

# Run tests before committing
python -m unittest discover tests -v
```

### Guidelines
- Follow existing code structure and naming conventions
- Add tests for new functionality
- Update documentation for API changes
- Ensure compatibility with existing examples

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE](LICENSE) file for details.

## Roadmap

### Near Term
- [ ] Neo4j storage backend implementation
- [ ] Enhanced visualization capabilities
- [ ] Additional analysis algorithms
- [ ] Performance optimizations

### Medium Term
- [ ] Machine learning integration for predictive modeling
- [ ] Real-time data integration capabilities
- [ ] Web-based interface for graph construction
- [ ] Advanced scenario modeling tools

### Long Term
- [ ] Cloud deployment options
- [ ] Industry-specific templates
- [ ] Integration with existing policy analysis tools
- [ ] Academic research collaboration features

---

*The Social Fabric Matrix Graph Service provides a robust foundation for understanding and analyzing complex socio-economic systems through the lens of F. Gregory Hayden's methodological framework.*
