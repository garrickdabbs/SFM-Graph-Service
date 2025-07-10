# Complex Policy Analysis Examples for SFM-Graph-Service

This directory contains two comprehensive examples demonstrating advanced features of the SFM-Graph-Service for policy analysis using real-world historical scenarios.

## Examples Overview

### 1. Tax Cuts and Jobs Act (TCJA) 2017 Analysis
**File:** `tcja_2017_analysis.py`

**Description:** Comprehensive analysis of the Tax Cuts and Jobs Act of 2017 and its financial impact on middle-class families.

**Key Features:**
- **Scope:** Federal tax policy implementation and state-level interactions
- **Nodes:** 1,200+ actors, institutions, policies, and indicators
- **Relationships:** 3,500+ connections modeling policy impacts
- **Time Period:** 2017-2025
- **Geographic Coverage:** Federal and all 50 states

**Major Components:**
- Federal tax agencies (IRS, Treasury, OTP, JCT)
- Congressional leadership and committees
- State revenue departments and governors
- Middle-class taxpayer demographics (by income and family type)
- TCJA policy provisions and instruments
- Economic indicators and financial flows
- Institutional framework for tax policy

### 2. Affordable Care Act (ACA) Healthcare Analysis
**File:** `aca_healthcare_analysis.py`

**Description:** Comprehensive analysis of the Affordable Care Act and its impact on healthcare outcomes and access.

**Key Features:**
- **Scope:** Healthcare system transformation and coverage expansion
- **Nodes:** 1,400+ actors, institutions, policies, and indicators
- **Relationships:** 4,200+ connections modeling healthcare interactions
- **Time Period:** 2010-2023
- **Geographic Coverage:** Federal and 20 major states

**Major Components:**
- Federal healthcare agencies (CMS, HHS, CDC, HRSA)
- State healthcare systems and Medicaid programs
- Healthcare providers and insurance networks
- Patient populations and demographics
- ACA policy provisions and instruments
- Health outcome indicators and flows
- Healthcare institutional framework

## Technical Features Demonstrated

### 1. Graph Persistence and Serialization
Both examples demonstrate:
- **Multiple Format Support:** JSON, Pickle, and Compressed JSON
- **Metadata Preservation:** Complete graph structure with relationships
- **Performance Metrics:** Save/load times and file sizes
- **Data Integrity:** Validation and consistency checks

```python
# Example usage
persistence_manager = SFMPersistenceManager(data_dir)
persistence_manager.save_graph(graph, filepath, StorageFormat.JSON, include_metadata=True)
loaded_graph = persistence_manager.load_graph(filepath, StorageFormat.JSON)
```

### 2. Advanced Caching and Performance Optimization
- **Cache Policies:** LRU and TTL caching strategies
- **Query Optimization:** Cached network analysis results
- **Performance Monitoring:** Real-time metrics collection
- **Memory Management:** Graph memory usage tracking

```python
# Example caching configuration
cache_manager.set_policy("query_results", CachePolicy.LRU, max_size=1000)
cache_manager.set_policy("network_metrics", CachePolicy.TTL, ttl_seconds=3600)
```

### 3. Security Validation and Input Sanitization
- **Input Validation:** All data inputs are validated and sanitized
- **Security Checks:** Authority and jurisdiction validation
- **Data Integrity:** Relationship validation rules
- **Safe Operations:** Protected graph modifications

```python
# Example security validation
validated_data = security_validator.validate_and_sanitize(input_data)
```

### 4. Performance Monitoring and Metrics Collection
- **Operation Timing:** Detailed performance metrics for all operations
- **Memory Usage:** Graph memory consumption tracking
- **Cache Statistics:** Hit rates and performance improvements
- **Resource Utilization:** System resource monitoring

```python
# Example performance monitoring
metrics_collector.start_monitoring()
# ... operations ...
metrics = metrics_collector.get_metrics()
```

### 5. High-Level Service Layer Features
- **Service Facade:** Unified interface for graph operations
- **Repository Pattern:** Abstracted data access layer
- **Query Engine:** Advanced network analysis capabilities
- **API Integration:** FastAPI-compatible data models

```python
# Example service usage
service = SFMService()
actor = service.create_actor(name="IRS", sector="government")
policy = service.create_policy(name="TCJA")
service.connect(actor.id, policy.id, "IMPLEMENTS")
```

### 6. Complex Analytics and Queries
Both examples include sophisticated analysis capabilities:

#### Network Analysis
- **Centrality Measures:** Betweenness, closeness, eigenvector centrality
- **Community Detection:** Identification of policy implementation clusters
- **Path Analysis:** Policy impact propagation paths
- **Structural Analysis:** Network topology and resilience

#### Policy Impact Analysis
- **Multi-hop Impact Tracing:** Following policy effects through the network
- **Scenario Comparison:** Before/after policy implementation
- **Target Identification:** Key actors and institutions affected
- **Outcome Measurement:** Quantitative impact assessment

#### Flow Analysis
- **Financial Flow Tracking:** Money flows between actors
- **Resource Allocation:** Distribution of policy resources
- **Bottleneck Identification:** Constraints in policy implementation
- **Efficiency Calculations:** Cost-effectiveness metrics

#### Temporal Analysis
- **Time Series Tracking:** Policy outcomes over time
- **Trend Analysis:** Long-term policy effects
- **Change Detection:** Significant shifts in indicators
- **Seasonal Patterns:** Cyclical policy impacts

## Data Sources and Modeling

### TCJA Analysis Data Sources
- **Congressional Records:** Voting patterns and committee assignments
- **IRS Statistics:** Tax filing data and demographic breakdowns
- **Treasury Reports:** Revenue estimates and policy analysis
- **Federal Reserve Data:** Economic indicators and impact measures
- **State Revenue Data:** State-level tax policy interactions

### ACA Analysis Data Sources
- **CMS Data:** Medicare and Medicaid enrollment and outcomes
- **Healthcare.gov:** Marketplace enrollment and premium data
- **CDC Statistics:** Health outcomes and utilization data
- **HRSA Reports:** Healthcare provider and access data
- **National Health Interview Survey:** Population health metrics

### Modeling Approach
Both examples use the Social Fabric Matrix framework to model:

1. **Actors:** Government agencies, legislators, taxpayers/patients, providers
2. **Institutions:** Formal rules, organizations, and informal norms
3. **Policies:** Legislation, regulations, and implementation mechanisms
4. **Resources:** Financial, human, and informational resources
5. **Processes:** Policy implementation and service delivery processes
6. **Flows:** Financial, informational, and service flows
7. **Indicators:** Outcome measures and performance metrics

## Usage Instructions

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Examples

#### TCJA Analysis
```bash
python examples/tcja_2017_analysis.py
```

#### ACA Analysis
```bash
python examples/aca_healthcare_analysis.py
```

### Expected Output
Each example generates:
- **Console Output:** Progress updates and analysis summary
- **Data Files:** Persisted graph data in multiple formats
- **Results JSON:** Comprehensive analysis results
- **Performance Report:** Detailed performance metrics

### Output Files
- `tcja_analysis_data/` or `aca_analysis_data/` - Analysis data directory
- `*_analysis.json` - Graph data in JSON format
- `*_analysis.pickle` - Graph data in Pickle format
- `*_analysis.json.gz` - Compressed graph data
- `*_analysis_results.json` - Complete analysis results

## Performance Characteristics

### TCJA Analysis
- **Graph Size:** ~1,200 nodes, ~3,500 edges
- **Generation Time:** ~8-12 seconds
- **Memory Usage:** ~85-120 MB
- **Analysis Time:** ~15-25 seconds
- **Persistence:** ~2-4 seconds per format

### ACA Analysis
- **Graph Size:** ~1,400 nodes, ~4,200 edges
- **Generation Time:** ~10-15 seconds
- **Memory Usage:** ~110-150 MB
- **Analysis Time:** ~20-30 seconds
- **Persistence:** ~3-5 seconds per format

## Key Insights and Findings

### TCJA Analysis Insights
- **Multi-level Governance:** Complex interactions between federal and state tax systems
- **Demographic Variations:** Different impacts across income brackets and family types
- **Policy Instrument Effects:** Varied effectiveness of different TCJA provisions
- **Implementation Challenges:** Coordination requirements across jurisdictions

### ACA Analysis Insights
- **Healthcare System Complexity:** Intricate relationships between multiple stakeholders
- **Geographic Variations:** State-level differences in implementation and outcomes
- **Coverage Improvements:** Measurable increases in healthcare access and coverage
- **Network Effects:** Cascading impacts throughout the healthcare system

## Technical Implementation Notes

### Code Quality
- **Type Safety:** Comprehensive type hints throughout
- **PEP8 Compliance:** Consistent coding style and formatting
- **Documentation:** Extensive docstrings and comments
- **Error Handling:** Robust exception handling and logging

### Scalability Considerations
- **Memory Management:** Efficient graph representation and caching
- **Performance Optimization:** Cached queries and optimized algorithms
- **Modular Design:** Extensible architecture for additional analysis
- **Data Validation:** Comprehensive input validation and sanitization

### Security Features
- **Input Sanitization:** All user inputs are validated and sanitized
- **Authority Validation:** Relationship authority checks
- **Data Integrity:** Comprehensive validation rules
- **Safe Operations:** Protected graph modifications

## Extension Points

### Adding New Analysis
1. **Create New Actors:** Add additional government agencies or stakeholders
2. **Extend Policies:** Include related policies or subsequent legislation
3. **Add Indicators:** Include additional outcome measures
4. **Enhance Relationships:** Model additional interaction types

### Customization Options
1. **Geographic Scope:** Extend to additional states or localities
2. **Time Period:** Extend analysis to cover longer time periods
3. **Stakeholder Groups:** Include additional affected populations
4. **Analysis Types:** Add new query types and analytical methods

## Troubleshooting

### Common Issues
1. **Memory Usage:** Large graphs may require memory management tuning
2. **Performance:** Complex queries may benefit from additional caching
3. **Data Loading:** Large datasets may require optimized loading strategies
4. **Visualization:** Complex graphs may need specialized visualization tools

### Optimization Tips
1. **Batch Operations:** Group similar operations for better performance
2. **Caching Strategy:** Tune cache policies for your specific use case
3. **Memory Limits:** Set appropriate memory limits for your environment
4. **Parallel Processing:** Consider parallel processing for large-scale analysis

## Future Enhancements

### Potential Improvements
1. **Real-time Data Integration:** Connect to live data sources
2. **Machine Learning:** Add predictive analytics capabilities
3. **Visualization:** Enhanced interactive visualization tools
4. **API Endpoints:** RESTful API for remote analysis access

### Research Applications
1. **Policy Simulation:** What-if analysis for policy proposals
2. **Comparative Analysis:** Cross-policy and cross-jurisdiction comparisons
3. **Impact Prediction:** Forecasting policy outcomes
4. **Stakeholder Engagement:** Interactive policy analysis tools

## Support and Documentation

For additional support:
- **Repository Issues:** Submit issues on GitHub
- **Documentation:** Refer to the main README and API documentation
- **Code Examples:** Additional examples in the tests directory
- **Community:** Join the SFM-Graph-Service community discussions