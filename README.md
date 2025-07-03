# Social Fabric Matrix Graph Service

An advanced Python framework implementing F. Gregory Hayden's Social Fabric Matrix (SFM) methodology for modeling, analyzing, and querying complex socio-economic systems through graph-based data structures and sophisticated analysis tools.

## Overview

The Social Fabric Matrix Graph Service is a comprehensive software implementation of the Social Fabric Matrix framework, designed to model and analyze complex interdependencies within socio-economic systems. This framework enables researchers, policy analysts, and decision-makers to:

- **Model Complex Systems**: Represent actors, institutions, resources, processes, flows, and their relationships in a unified, type-safe graph structure
- **Analyze Policy Impacts**: Trace the effects of policy changes through interconnected networks using advanced graph algorithms
- **Forecast System Changes**: Use network analysis and predictive modeling to anticipate outcomes of interventions
- **Query Complex Relationships**: Perform sophisticated analytical queries on system topology with a powerful query engine
- **Validate System Integrity**: Ensure data consistency through comprehensive enum validation and type safety
- **Visualize Networks**: Generate interactive visualizations for system exploration and presentation

Built with modern software engineering practices, this framework provides a robust, extensible architecture suitable for both research prototyping and production-scale policy analysis applications.

## Key Features

### 📊 **Comprehensive Data Model**
- **Actors**: Government agencies, corporations, organizations, individuals with sector-based classification
- **Institutions**: Three-layer institutional framework (formal rules, organizations, informal norms) following Hayden's methodology
- **Resources**: Natural resources, produced goods, financial capital, knowledge with comprehensive type validation
- **Processes**: Transformation activities that convert inputs to outputs with flow tracking
- **Flows**: Quantified linkages between system components with directional nature tracking
- **Policies**: Formal interventions with authority attribution and measurable impacts
- **Indicators**: Performance metrics with current values and trend tracking
- **Relationships**: Strongly-typed connections with weights, validation rules, and dimensional metadata
- **Technology Systems**: Innovation tracking with Technology Readiness Level (TRL) assessment
- **Value Systems**: Cultural and institutional value frameworks with legitimacy source tracking

### 🔍 **Advanced Query Engine**
- **Network Analysis**: Centrality measures, path finding, community detection, structural analysis
- **Policy Impact Analysis**: Multi-hop impact tracing, scenario comparison, target identification
- **Flow Analysis**: Resource flow tracking, bottleneck identification, efficiency calculations
- **Structural Analysis**: Bridge identification, vulnerability assessment, system resilience evaluation
- **Temporal Analysis**: Time-series tracking, trend analysis, change detection
- **Validation Analysis**: System integrity checking, relationship validation, enum compliance

### 🗄️ **Flexible Storage and API Layer**
- **Abstract Repository Pattern**: Extensible to multiple storage backends (NetworkX, Neo4j-ready)
- **Type-Safe Operations**: Strongly-typed repositories for different entity types with validation
- **CRUD Operations**: Full create, read, update, delete functionality with transaction support
- **RESTful API**: FastAPI-based service layer for web applications and external integrations
- **Graph Persistence**: Save/load complete graph structures with relationship preservation

### 🛠️ **Enhanced Validation and Type Safety**
- **Comprehensive Enum Validation**: Cross-enum dependency checking and contextual validation
- **Relationship Validation**: Entity-type specific relationship rules with helpful error messages
- **Policy Instrument Validation**: Ensures appropriate policy tools for given contexts
- **Flow Validation**: Validates flow nature and type combinations for system integrity
- **Institution Layer Validation**: Enforces Hayden's three-layer institutional framework

### 📈 **Real-World Applications**
- **Commodity Market Analysis**: Forecast price changes based on policy and market conditions
- **Policy Impact Assessment**: Analyze ripple effects of regulatory changes through system networks
- **Supply Chain Resilience**: Identify vulnerabilities, dependencies, and critical pathways
- **Economic Development Planning**: Model regional development scenarios and policy outcomes
- **Institutional Analysis**: Study formal and informal institutional interactions and changes

## Installation

### Requirements
- Python 3.8+
- NetworkX 3.0+
- FastAPI (for API services)
- Neo4j (optional, for graph database backend)
- Additional dependencies listed in requirements.txt

### Setup
```bash
# Clone the repository
git clone https://github.com/SFM-Graph-Service/alpha.git
cd alpha

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Verification
```bash
# Run the test suite to verify installation
python -m unittest discover tests -v

# Test with example
python examples/us_grain_export_example.py
```

## Quick Start

### Basic Usage
```python
from core.sfm_models import SFMGraph, Actor, Institution, Relationship
from core.sfm_enums import RelationshipKind, InstitutionLayer
from db.sfm_dao import SFMRepositoryFactory
from core.sfm_query import SFMQueryFactory

# Create a repository with NetworkX backend
repo = SFMRepositoryFactory.create_repository("networkx")

# Create entities with proper typing
usda = Actor(label="USDA", sector="Government")
farmers = Actor(label="Farmers Association", sector="Agriculture") 
market = Institution(label="Commodity Market", layer=InstitutionLayer.FORMAL)

# Add to repository
repo.create_node(usda)
repo.create_node(farmers)
repo.create_node(market)

# Create relationships with validation
regulation = Relationship(
    source_id=usda.id,
    target_id=farmers.id,
    kind=RelationshipKind.REGULATES,
    weight=0.8,
    description="USDA regulatory oversight of farming practices"
)
repo.create_relationship(regulation)

# Load into SFM graph for analysis
sfm_graph = repo.load_graph()

# Create query engine for analysis
query_engine = SFMQueryFactory.create_query_engine(sfm_graph, "networkx")

# Perform network analysis
central_actors = query_engine.get_most_central_nodes(Actor, "betweenness", 5)
policy_impact = query_engine.analyze_policy_impact(usda.id, impact_radius=3)

print(f"Most central actors: {central_actors}")
print(f"Policy impact: {policy_impact}")
```

### Using the Service Layer
```python
from core.sfm_service import SFMService, SFMServiceConfig

# Initialize service with configuration
config = SFMServiceConfig(
    storage_backend="networkx",
    enable_validation=True,
    auto_save=True
)
service = SFMService(config)

# Use high-level service operations
actor_id = service.create_actor("USDA", "Government")
institution_id = service.create_institution("Market", InstitutionLayer.FORMAL)

# Create relationships through service
service.create_relationship(
    actor_id, institution_id, 
    RelationshipKind.PARTICIPATES_IN, 
    weight=0.9
)

# Get analysis results
analysis = service.get_network_analysis()
health = service.get_service_health()
```

### Advanced Example: Grain Market Analysis
```python
from examples.us_grain_export_example import create_us_grain_market_graph
from core.sfm_models import SFMGraph
from core.sfm_enums import ResourceType
from db.sfm_dao import SFMRepositoryFactory

# Create repository and graph container
repo = SFMRepositoryFactory.create_repository("networkx")
sfm_graph = SFMGraph(
    name="US Grain Market Analysis",
    description="Comprehensive model for grain price forecasting and policy analysis"
)

# Build complex graph with entities and relationships
us_grain_graph = create_us_grain_market_graph(repo, sfm_graph)

# Create query engine for sophisticated analysis
query_engine = SFMQueryFactory.create_query_engine(us_grain_graph, "networkx")

# Perform comprehensive system analysis
vulnerabilities = query_engine.system_vulnerability_analysis()
grain_flows = query_engine.trace_resource_flows(ResourceType.PRODUCED)
network_density = query_engine.calculate_network_density()

# Analyze policy impacts across the system
for policy_id, policy in us_grain_graph.policies.items():
    impact = query_engine.analyze_policy_impact(policy_id, impact_radius=3)
    affected_nodes = impact.get('total_affected_nodes', 0)
    print(f"{policy.label}: affects {affected_nodes} nodes in the system")

# Identify critical system components
bridges = query_engine.find_bridges()
central_nodes = query_engine.get_most_central_nodes(limit=5)

print(f"System vulnerability points: {vulnerabilities}")
print(f"Network density: {network_density:.3f}")
print(f"Critical bridges: {bridges}")
```

### RESTful API Usage
```python
import httpx

# Start the API server (in separate terminal)
# uvicorn api.sfm_api:app --reload

# Use the REST API
async with httpx.AsyncClient() as client:
    # Create entities via API
    actor_response = await client.post(
        "http://localhost:8000/actors",
        json={"label": "USDA", "sector": "Government"}
    )
    
    # Get analysis results
    analysis_response = await client.get("http://localhost:8000/analysis/network")
    
    # Retrieve graph data
    graph_response = await client.get("http://localhost:8000/graph")
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

## Advanced Examples

The framework includes sophisticated examples that demonstrate the full analytical power of the Social Fabric Matrix methodology for complex real-world systems. These examples showcase advanced features including temporal dynamics, cognitive frameworks, multi-stakeholder analysis, and comprehensive policy evaluation.

### 1. Smart City Urban Planning (`smart_city_urban_planning_example.py`)

**Scenario**: Comprehensive smart city initiative involving multiple stakeholders, technology systems, and policy instruments working together to achieve sustainable urban development goals.

**Advanced Features Demonstrated**:
- **42 nodes across 6 entity types**: 7 actors, 3 institutions, 7 resources, 3 policies, 4 flows, 6 indicators, 3 technology systems, 3 policy instruments
- **Temporal dynamics**: Policy rollout, crisis response, and technology adoption patterns
- **Technology readiness levels**: IoT sensors (TRL 8), AI traffic systems (TRL 7), green building tech (TRL 9)
- **Cognitive frameworks**: Government efficiency, community quality of life, and innovation frameworks
- **Multi-dimensional analysis**: Network centrality, vulnerability assessment, stakeholder power distribution

**Key Stakeholders**: City Government, Urban Planning Department, Tech Companies, Community Groups, Environmental NGOs, Research Universities

**Policy Analysis**: Smart city master plan implementation, green building standards enforcement, data privacy regulations

```bash
python examples/smart_city_urban_planning_example.py
```

**Sample Output**:
```
🎯 Most Central Actors (Betweenness Centrality):
  • Smart Infrastructure Corp: 0.011
  • Neighborhood Associations: 0.001

🔬 Technology Maturity Analysis:
  • IoT Environmental Sensor Network: TRL 8 (0.77 compatibility)
  • AI Traffic Management System: TRL 7 (0.82 compatibility)
  • Smart Green Building Technology: TRL 9 (0.82 compatibility)

⏰ Temporal Change Analysis:
  • Smart City Investment Flow: EXPONENTIAL dynamics
  • Research to Practice Knowledge Transfer: LOGISTIC dynamics
```

### 2. Global Supply Chain Resilience (`global_supply_chain_resilience_example.py`)

**Scenario**: Global supply chain ecosystem with multiple tiers, regions, and stakeholders working together to maintain operational resilience in the face of global disruptions.

**Advanced Features Demonstrated**:
- **68 nodes across 9 entity types**: 10 actors, 5 institutions, 10 resources, 4 policies, 6 flows, 11 indicators, 4 technology systems, 4 policy instruments, 3 processes, 2 feedback loops
- **Crisis and recovery dynamics**: Exponential disruption patterns, logistic recovery models
- **Multi-tier analysis**: OEMs, Tier 1/2 suppliers, raw material providers, logistics networks
- **Technology integration**: Blockchain platforms, AI forecasting, IoT tracking, digital twins
- **Comprehensive resilience metrics**: 8 value categories including performance, economic, technological, social, environmental, institutional, resilience, and diversity

**Key Stakeholders**: Automotive OEMs, Electronics Manufacturers, Global Suppliers, Logistics Providers, Financial Services, Trade Organizations

**Policy Analysis**: Supply chain transparency mandates, diversification incentives, resilience standards, digital trade facilitation

```bash
python examples/global_supply_chain_resilience_example.py
```

**Sample Output**:
```
🎯 Most Central Supply Chain Actors:
  • Global Automotive OEM: 0.007
  • Tier 1 Component Supplier (Asia): 0.005
  • Semiconductor Foundry: 0.003

🚧 Supply Chain Bottleneck Identification:
  • Material flow bottlenecks: 6 identified
  • Information flow bottlenecks: 6 identified
  • Financial flow bottlenecks: 6 identified

⏰ Crisis and Recovery Dynamics:
  • Critical Component Flow: EXPONENTIAL dynamics
  • Raw Material Supply Flow: LOGISTIC dynamics
  • Cross-Border Payment Flows: EXPONENTIAL dynamics
```

### 3. Healthcare System Policy Analysis (`healthcare_system_policy_example.py`)

**Scenario**: Healthcare system policy evaluation involving patients, providers, payers, regulators, and technology systems working together to improve health outcomes through coordinated policy interventions.

**Advanced Features Demonstrated**:
- **69 nodes across 8 entity types**: 10 actors, 5 institutions, 10 resources, 4 policies, 6 flows, 12 indicators, 4 technology systems, 4 policy instruments, 3 processes
- **Cognitive frameworks**: Evidence-based medicine, health economics, patient-centered care, prevention frameworks
- **Value systems**: Medical ethics, population health values, patient rights and autonomy
- **Behavioral patterns**: Technology adoption, clinical guideline adherence, preventive care seeking, collaborative coordination
- **Multi-dimensional outcomes**: Health, equity, economic, technological, and social indicators

**Key Stakeholders**: Primary Care Physicians, Hospital Systems, Health Insurance Companies, Public Health Agencies, Patient Advocacy Groups, Health Tech Companies, Research Institutions

**Policy Analysis**: Universal coverage expansion, quality payment programs, interoperability mandates, prevention investments

```bash
python examples/healthcare_system_policy_example.py
```

**Sample Output**:
```
⚡ Healthcare Stakeholder Power Distribution:
  • Regional Hospital Systems: 0.91 average power
  • Health Research Institutions: 0.89 average power
  • Health Insurance Companies: 0.88 average power

🔬 Healthcare Technology Integration Assessment:
  • Electronic Health Records System: TRL 9 (0.74 compatibility)
  • AI-Powered Diagnostic Support: TRL 7 (0.68 compatibility)
  • Comprehensive Telehealth Platform: TRL 8 (0.79 compatibility)

📊 Health Outcome Indicators by Category:
  Health Indicators:
    • Clinical Quality Outcomes: 72.0 → 85.0
    • Patient Safety Incidents: 12.5 → 6.0
    • Preventable Hospitalizations: 45.0 → 25.0
```

### Example Comparison and Use Cases

| Example | Domain | Nodes | Focus | Key Features |
|---------|--------|-------|-------|--------------|
| **Smart City** | Urban Planning | 42 | Technology Integration & Governance | Temporal dynamics, IoT systems, multi-stakeholder coordination |
| **Supply Chain** | Global Commerce | 68 | Resilience & Crisis Response | Multi-tier networks, disruption modeling, bottleneck analysis |
| **Healthcare** | Policy Analysis | 69 | Outcomes & Quality Improvement | Cognitive frameworks, value systems, behavioral patterns |

### Running Advanced Examples

All examples include comprehensive analysis output and can be run independently:

```bash
# Smart city planning with technology integration
python examples/smart_city_urban_planning_example.py

# Global supply chain resilience analysis
python examples/global_supply_chain_resilience_example.py

# Healthcare system policy evaluation
python examples/healthcare_system_policy_example.py
```

### Customizing Examples

Each example can be easily modified to explore different scenarios:

```python
# Modify stakeholder power distributions
actor.power_resources = {
    "technological": 0.95,
    "financial": 0.8,
    "regulatory": 0.6
}

# Adjust temporal dynamics parameters
temporal_dynamics = TemporalDynamics(
    start_time=baseline_period,
    function_type=TemporalFunctionType.LOGISTIC,
    parameters={"growth_rate": 0.4, "capacity": 100.0}
)

# Change policy effectiveness measures
policy_instrument.effectiveness_measure = 0.85

# Modify technology readiness levels
tech_system.maturity = TechnologyReadinessLevel.PROTOTYPE_DEMONSTRATION
```

These examples serve as comprehensive templates for building domain-specific SFM models and demonstrate the framework's capability to handle complex, multi-stakeholder systems with sophisticated analytical requirements.

## Architecture

### Core Components

```
SFM-Graph-Service/
├── core/                           # Core framework components
│   ├── sfm_models.py              # Data model classes (Node, Actor, Institution, etc.)
│   ├── sfm_query.py               # Query engine abstractions and NetworkX implementation
│   ├── sfm_enums.py               # Comprehensive enumeration definitions
│   ├── sfm_service.py             # High-level service facade for simplified usage
│   └── sfm_persistence.py         # Graph persistence and serialization utilities
├── db/                            # Data access layer
│   └── sfm_dao.py                 # Repository pattern implementation (CRUD operations)
├── api/                           # RESTful web service layer
│   └── sfm_api.py                 # FastAPI-based REST endpoints
├── examples/                      # Working examples and demonstrations
│   ├── us_grain_export_example.py # Comprehensive grain market model
│   └── us_grain_market_forecast.py # Market forecasting example
├── tests/                         # Comprehensive test suite
│   ├── test_sfm_models.py         # Unit tests for data models
│   ├── test_sfm_dao.py            # Unit tests for data access layer
│   ├── test_sfm_query.py          # Unit tests for query engine
│   ├── test_sfm_service.py        # Unit tests for service layer
│   ├── test_enum_validation.py    # Tests for enum validation system
│   └── test_sfm_api.py            # API endpoint tests
├── docs/                          # Documentation and design materials
│   ├── sfm-overview.md            # Theoretical framework overview
│   ├── SFMSuiteDesignProposal.md  # Comprehensive design documentation
│   ├── enum_validation_guide.md   # Validation system documentation
│   └── hayden_sfm_alignment.md    # SFM methodology alignment notes
├── pyproject.toml                 # Modern Python project configuration
├── requirements.txt               # Production dependencies
└── setup.py                      # Package installation configuration
```

### Design Principles

1. **Separation of Concerns**: Clear boundaries between data models, storage, query operations, and service layers
2. **Extensibility**: Abstract interfaces allow new storage backends, analysis methods, and service integrations
3. **Type Safety**: Strong typing with comprehensive validation ensures data integrity and developer experience
4. **Performance**: Optimized for both small prototypes and large-scale production analysis
5. **Hayden Compliance**: Faithful implementation of SFM theoretical framework with methodological rigor
6. **API-First Design**: RESTful service layer enables web applications and external system integration
7. **Validation-Driven**: Comprehensive enum validation ensures system integrity and prevents modeling errors

## Data Model

### Entity Hierarchy
The framework models Hayden's core SFM components with enhanced typing and validation:

- **Core Node Types**: Base classes for all system entities
  - `Actor`: Decision-making entities (agencies, firms, individuals) with sector classification
  - `Institution`: Rule systems at three levels (formal, organizational, informal) following Hayden's framework
  - `Resource`: Stocks and assets (natural, produced, financial, knowledge) with comprehensive type validation
  - `Process`: Transformation activities with input/output flow tracking
  - `Flow`: Quantified system linkages with directional nature (input/output/bidirectional)
  - `Policy`: Specific institutional interventions with authority attribution and instrument typing
  - `Indicator`: Measurable system performance metrics with current values and trend tracking

- **Advanced Entity Types**: Extended framework capabilities
  - `TechnologySystem`: Innovation and technology tracking with TRL (Technology Readiness Level) assessment
  - `ValueSystem`: Cultural and institutional value frameworks with legitimacy source tracking
  - `FeedbackLoop`: System feedback mechanisms with polarity and type classification
  - `SystemProperty`: Emergent system characteristics and properties

- **Relationship Types**: Semantic connections between entities with validation rules
  - Governance relationships (REGULATES, AUTHORIZES, ENFORCES, GOVERNS)
  - Economic relationships (FUNDS, TRADES, PRODUCES, OWNS, EMPLOYS)
  - Information relationships (INFORMS, INFLUENCES, COMMUNICATES)
  - Process relationships (TRANSFORMS, EXTRACTS, DISTRIBUTES, PARTICIPATES_IN)
  - Institutional relationships (LEGITIMIZES, CONSTRAINS, ENABLES)

### Dimensional Entities
- **TimeSlice**: Temporal context for analysis periods (fiscal years, quarters)
- **SpatialUnit**: Geographic boundaries and scales for regional analysis
- **Scenario**: Policy counterfactuals and alternative futures for comparative analysis
- **AnalyticalContext**: Framework for organizing different analytical perspectives

### Validation and Type Safety
The framework includes comprehensive validation systems:
- **Cross-Enum Validation**: Ensures compatibility between related enum values
- **Relationship Validation**: Validates source-target entity type combinations for relationships
- **Policy Instrument Validation**: Ensures appropriate policy tools for given institutional contexts
- **Flow Validation**: Validates flow nature and type combinations for system integrity
- **Institution Layer Validation**: Enforces Hayden's three-layer institutional framework consistency

## Analysis Capabilities

### Network Metrics and Structural Analysis
- **Centrality Analysis**: Identify key system nodes using betweenness, closeness, degree, and eigenvector centrality
- **Path Analysis**: Find shortest paths, alternative routes, and reachability between entities
- **Community Detection**: Discover system clusters, subsystems, and organizational boundaries
- **Structural Analysis**: Locate bridges, bottlenecks, vulnerabilities, and critical pathways
- **Network Density**: Calculate connectivity levels and system integration measures
- **Bridge Analysis**: Identify critical connector nodes whose removal would fragment the network

### Policy Analysis and Impact Assessment
- **Multi-hop Impact Propagation**: Trace policy effects through network paths with configurable radius
- **Scenario Modeling**: Compare baseline vs. intervention outcomes across multiple dimensions
- **Target Identification**: Find entities directly and indirectly affected by policy changes
- **Effectiveness Measurement**: Quantify policy reach, influence strength, and system penetration
- **Ripple Effect Analysis**: Track cascading effects through institutional and economic networks
- **Cross-System Impact**: Analyze how changes in one subsystem affect other subsystems

### Flow Analysis and Resource Tracking
- **Resource Tracing**: Follow materials, money, and information flows through system pathways
- **Bottleneck Detection**: Identify system constraints, chokepoints, and capacity limitations
- **Efficiency Calculation**: Measure flow effectiveness, losses, and optimization opportunities
- **Dependency Mapping**: Understand supply chain relationships and critical dependencies
- **Flow Volume Analysis**: Quantify resource movement and identify high-volume pathways
- **Flow Direction Analysis**: Track directional patterns and bidirectional relationships

### System Integrity and Validation Analysis
- **Relationship Validation**: Verify that entity relationships follow defined rules and constraints
- **Enum Compliance**: Check that all entities use valid enumeration values and combinations
- **System Consistency**: Validate overall system coherence and identify potential modeling errors
- **Completeness Analysis**: Identify missing relationships or entities that may be needed
- **Data Quality Assessment**: Evaluate the quality and completeness of system data

## Testing

The framework includes comprehensive test coverage with 491 passing tests:

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test modules
python -m unittest tests.test_sfm_models -v
python -m unittest tests.test_sfm_dao -v
python -m unittest tests.test_sfm_query -v
python -m unittest tests.test_sfm_service -v
python -m unittest tests.test_enum_validation -v

# Run API tests
python -m unittest tests.test_sfm_api -v
```

### Test Categories
- **Unit Tests**: Individual component functionality (models, enums, repositories)
- **Integration Tests**: Component interaction verification (service layer, API endpoints)
- **Validation Tests**: Comprehensive enum validation and type safety verification
- **Performance Tests**: Scalability and efficiency validation for large graphs
- **Edge Case Tests**: Error handling, boundary conditions, and robustness testing
- **SFM Alignment Tests**: Validation of Hayden's methodology implementation
- **API Tests**: RESTful service endpoint functionality and response validation

### Test Coverage Areas
- **Data Models**: Entity creation, validation, and relationship management
- **Repository Layer**: CRUD operations, graph persistence, and query functionality
- **Query Engine**: Network analysis, policy impact assessment, and flow tracking
- **Service Layer**: High-level operations, configuration management, and health monitoring
- **Enum Validation**: Cross-enum dependencies, relationship rules, and contextual validation
- **API Layer**: HTTP endpoints, request/response handling, and error management

## Examples and Demonstrations

### US Grain Market Analysis
The [`examples/us_grain_export_example.py`](examples/us_grain_export_example.py) provides a comprehensive demonstration of framework capabilities:

**Model Components:**
- **Actors**: USDA (government), Farmers (agriculture), Traders (private sector)
- **Institutions**: US Government, Trade Organizations with proper layer classification
- **Resources**: Grain (produced goods), Land (natural resources) with type validation
- **Policies**: Grain subsidies, Export tariffs with authority attribution
- **Flows**: Export flows, Financial flows with directional nature tracking
- **Indicators**: Grain prices, Production levels with quantitative values

**Analysis Capabilities Demonstrated:**
- Actor centrality analysis and influence measurement
- Policy impact assessment with multi-hop propagation
- Resource flow tracing and bottleneck identification
- Network density calculation and structural analysis
- Bridge identification for system resilience assessment

**Running the Example:**
```bash
# Execute the complete grain market analysis
python examples/us_grain_export_example.py

# Expected output includes:
# - Graph creation statistics (entities and relationships)
# - Network analysis results (centrality, density, vulnerabilities)
# - Policy impact assessments
# - Resource flow analysis
# - Structural component identification
```

### Market Forecasting Example
The [`examples/us_grain_market_forecast.py`](examples/us_grain_market_forecast.py) demonstrates:
- Time-series integration with SFM analysis
- Scenario comparison for policy alternatives
- Predictive modeling using network structure
- Integration with external data sources

### API Service Demonstration
Start the RESTful API service for web integration:
```bash
# Start the FastAPI server
uvicorn api.sfm_api:app --reload --host 0.0.0.0 --port 8000

# Access interactive documentation
open http://localhost:8000/docs
```

**Available API Endpoints:**
- `POST /actors`: Create new actor entities
- `POST /institutions`: Create new institutions with layer validation
- `POST /relationships`: Create validated relationships between entities
- `GET /analysis/network`: Retrieve network analysis results
- `GET /analysis/policy/{policy_id}`: Get policy impact analysis
- `GET /graph`: Export complete graph structure
- `GET /health`: Service health and status information

## Documentation

### Core Documentation
- **[SFM Overview](docs/sfm-overview.md)**: Theoretical foundation and Hayden's methodology
- **[Design Proposal](docs/SFMSuiteDesignProposal.md)**: Comprehensive architectural design and extensibility roadmap
- **[Manifest](docs/sfmManifest.md)**: Advanced service capabilities and modular architecture
- **[Hayden SFM Alignment](docs/hayden_sfm_alignment.md)**: Methodological compliance and theoretical accuracy
- **[Enum Validation Guide](docs/enum_validation_guide.md)**: Comprehensive guide to validation system usage

### Module Documentation
- **[Core Module](core/README.md)**: Data models, query engine, and service layer documentation
- **[Database Module](db/README.md)**: Repository patterns, type-safe operations, and storage backends

### API Documentation
When running the API service, interactive documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Theoretical Foundation

This implementation is based on F. Gregory Hayden's Social Fabric Matrix methodology, which provides:

- **Systems Perspective**: Understanding complex interdependencies and emergent properties
- **Institutional Analysis**: Three-layer institutional framework (formal rules, organizations, informal norms)
- **Policy Integration**: Connecting formal policies to informal practices and cultural values
- **Quantitative Assessment**: Measuring relationship strengths, impacts, and system dynamics
- **Dynamic Modeling**: Capturing system evolution, change processes, and path dependencies

### SFM Core Concepts Implemented

1. **Matrix Structure**: Entities as nodes, relationships as weighted edges with semantic meaning
2. **Hierarchical Institution Types**: Formal rules, organizational structures, informal cultural norms
3. **Flow Quantification**: Measurable transfers between system components with directional tracking
4. **Dimensional Analysis**: Temporal slicing, spatial boundaries, and scenario comparison
5. **Policy Evaluation**: Systematic assessment of intervention effects with impact propagation
6. **Validation Framework**: Ensuring theoretical consistency and methodological rigor

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

We welcome contributions to the Social Fabric Matrix Graph Service! This project follows open-source best practices and encourages community involvement.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/SFM-Graph-Service/alpha.git
cd alpha

# Install in development mode with all dependencies
pip install -r requirements.txt
pip install -e .

# Run tests to verify setup
python -m unittest discover tests -v

# Run example to verify functionality
python examples/us_grain_export_example.py
```

### Development Guidelines

**Code Quality Standards:**
- Follow existing code structure and naming conventions
- Add comprehensive tests for new functionality (maintain 100% test coverage)
- Update documentation for API changes and new features
- Ensure compatibility with existing examples and use cases
- Use type hints and docstrings for all public methods
- Follow PEP 8 style guidelines with pylint validation

**Testing Requirements:**
- Write unit tests for individual components
- Include integration tests for component interactions
- Add validation tests for new enum types or relationship rules
- Test edge cases and error conditions
- Verify API endpoints with request/response testing

**Documentation Standards:**
- Update relevant README sections for new features
- Add docstrings following Google style conventions
- Include usage examples in docstrings
- Update API documentation for new endpoints
- Maintain theoretical alignment documentation for SFM methodology changes

### Contribution Areas

**High-Priority Contributions Needed:**
- Additional storage backends (Neo4j, PostgreSQL, MongoDB)
- Enhanced visualization capabilities with interactive web components
- Machine learning integration for predictive modeling
- Performance optimizations for large-scale graph analysis
- Industry-specific SFM templates and example models

**Medium-Priority Enhancements:**
- Real-time data integration capabilities
- Advanced scenario modeling tools
- Export capabilities to common formats (GraphML, GEXF, CSV)
- Enhanced policy simulation features
- Integration with external policy analysis tools

**New Example Domains for Contribution:**
- Environmental policy and climate change adaptation
- Financial system stability and regulatory analysis
- Educational system reform and outcome improvement
- Energy transition and renewable technology adoption
- International trade and diplomatic relationship modeling
- Social media and information flow analysis

### Adding New Storage Backends

1. Implement the `SFMRepository` abstract class in `db/sfm_dao.py`
2. Add factory method to `SFMRepositoryFactory`
3. Create comprehensive test suite
4. Update documentation and examples

Example for Neo4j backend:
```python
class Neo4jSFMRepository(SFMRepository):
    def __init__(self, connection_string: str):
        """Initialize Neo4j connection."""
        self.driver = GraphDatabase.driver(connection_string)
    
    def create_node(self, node: Node) -> Node:
        """Create node in Neo4j database."""
        # Implementation with Cypher queries
        pass
```

### Adding New Analysis Methods

1. Extend the `SFMQueryEngine` abstract class in `core/sfm_query.py`
2. Implement in `NetworkXSFMQueryEngine` class
3. Add comprehensive tests in `tests/test_sfm_query.py`
4. Document usage patterns and theoretical justification

### Pull Request Process

1. **Fork and Branch**: Create a feature branch from main
2. **Develop**: Implement changes with tests and documentation
3. **Test**: Ensure all tests pass (`python -m unittest discover tests -v`)
4. **Lint**: Run pylint and fix any style issues
5. **Document**: Update README and relevant documentation
6. **Submit**: Create pull request with clear description of changes

### Community Guidelines

- **Be Respectful**: Maintain professional and inclusive communication
- **Academic Rigor**: Ensure theoretical alignment with Hayden's SFM methodology
- **Open Collaboration**: Share knowledge and help other contributors
- **Quality Focus**: Prioritize code quality and system reliability over speed

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

## Roadmap

### Current Release (v1.0.0)
- [x] Comprehensive SFM data model with type safety
- [x] NetworkX-based graph storage and analysis
- [x] Advanced query engine with network analysis capabilities
- [x] RESTful API service layer with FastAPI
- [x] Comprehensive enum validation system
- [x] Service layer facade for simplified usage
- [x] Extensive test suite (491 passing tests)
- [x] Working examples and demonstrations

### Near Term (v1.1.0 - Q2 2024)
- [ ] Neo4j storage backend implementation for large-scale analysis
- [ ] Enhanced visualization capabilities with PyVis and D3.js integration
- [ ] Performance optimizations for graphs with 10,000+ nodes
- [ ] Export capabilities (GraphML, GEXF, CSV formats)
- [ ] Advanced policy simulation with scenario branching
- [ ] Interactive Jupyter notebook tutorials

### Medium Term (v1.2.0 - Q4 2024)
- [ ] Machine learning integration for predictive modeling and pattern recognition
- [ ] Real-time data integration capabilities with external APIs
- [ ] Web-based interface for graph construction and visualization
- [ ] Advanced scenario modeling tools with counterfactual analysis
- [ ] Industry-specific SFM templates (agriculture, healthcare, energy)
- [ ] Time-series analysis integration for temporal dynamics

### Long Term (v2.0.0 - 2025)
- [ ] Cloud deployment options (AWS, Azure, GCP) with containerization
- [ ] Multi-user collaboration features with role-based access
- [ ] Integration with existing policy analysis tools (R, STATA, specialized software)
- [ ] Academic research collaboration features and publication support
- [ ] Advanced AI-driven insights and automated policy recommendation
- [ ] Multi-language support for international applications

### Research and Development
- [ ] Dynamic graph evolution modeling with temporal pathways
- [ ] Uncertainty quantification and sensitivity analysis
- [ ] Multi-scale analysis capabilities (micro, meso, macro levels)
- [ ] Network resilience and robustness optimization
- [ ] Cross-system interaction modeling for complex policy domains

---

*The Social Fabric Matrix Graph Service provides a robust foundation for understanding and analyzing complex socio-economic systems through the lens of F. Gregory Hayden's methodological framework.*
