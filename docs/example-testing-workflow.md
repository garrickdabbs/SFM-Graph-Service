# Example Testing Workflow Documentation

## Overview

The **Test Examples** workflow is an ad-hoc GitHub Actions workflow designed to validate the functionality of all examples provided in the Social Fabric Matrix Graph Service repository. This workflow ensures that examples are working correctly and provides comprehensive testing across different scenarios and edge cases.

## Features

- ✅ **Manual Triggering**: Can be run on-demand using workflow_dispatch
- ✅ **Configurable Timeout**: Adjustable timeout for each example execution
- ✅ **Selective Testing**: Option to run all examples or just basic ones
- ✅ **Comprehensive Validation**: Validates both execution success and output content
- ✅ **Edge Case Testing**: Tests error scenarios and memory constraints
- ✅ **Detailed Reporting**: Generates comprehensive test reports with artifacts
- ✅ **Error Logging**: Captures detailed logs for debugging failed tests

## Workflow Inputs

| Parameter | Description | Default | Required |
|-----------|-------------|---------|----------|
| `timeout_minutes` | Timeout in minutes for each example | `5` | No |
| `run_all_examples` | Run all examples (if false, only run basic ones) | `true` | No |

## Tested Examples

### Always Tested (Basic Examples)
1. **US Grain Export Example** (`us_grain_export_example.py`)
   - Basic SFM graph creation and analysis
   - Actor centrality analysis
   - Policy impact assessment

2. **US Grain Market Forecast Example** (`us_grain_market_forecast.py`)
   - Market forecasting functionality
   - Time-series integration with SFM analysis

### Advanced Examples (when `run_all_examples` = true)
3. **Smart City Urban Planning Example** (`smart_city_urban_planning_example.py`)
   - Complex multi-stakeholder relationships
   - Technology systems with maturity assessment
   - Temporal dynamics modeling

4. **Healthcare System Policy Example** (`healthcare_system_policy_example.py`)
   - Multi-stakeholder healthcare ecosystem modeling
   - Cognitive frameworks in healthcare decision-making
   - Value systems and ethical considerations

5. **Global Supply Chain Resilience Example** (`global_supply_chain_resilience_example.py`)
   - Multi-regional supply chain networks
   - Risk assessment and vulnerability analysis
   - Dynamic flow analysis with bottleneck identification

## How to Trigger the Workflow

### Method 1: GitHub Web Interface
1. Navigate to the repository on GitHub
2. Go to the **Actions** tab
3. Select **Test Examples** from the workflow list
4. Click **Run workflow**
5. Configure the input parameters:
   - **Timeout in minutes**: Set how long each example should run (default: 5)
   - **Run all examples**: Choose whether to test all examples or just basic ones
6. Click **Run workflow** to start the test

### Method 2: GitHub CLI
```bash
# Run with default settings
gh workflow run test-examples.yml

# Run with custom timeout and only basic examples
gh workflow run test-examples.yml \
  -f timeout_minutes=3 \
  -f run_all_examples=false

# Run all examples with extended timeout
gh workflow run test-examples.yml \
  -f timeout_minutes=10 \
  -f run_all_examples=true
```

### Method 3: GitHub API
```bash
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/SFM-Graph-Service/alpha/actions/workflows/test-examples.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "timeout_minutes": "5",
      "run_all_examples": "true"
    }
  }'
```

## Understanding the Results

### Success Indicators
- ✅ **Green checkmarks** indicate successful example execution
- **Output validation** ensures examples produce expected results
- **Complete execution** within timeout limits

### Failure Indicators
- ❌ **Red X marks** indicate failed example execution
- **Exit codes** show the type of failure
- **Detailed logs** in artifacts provide debugging information

### Output Validation
The workflow validates that examples produce expected outputs including:
- Graph creation messages
- Analysis section headers
- Expected data patterns
- Proper cleanup messages

## Edge Case Testing

The workflow includes comprehensive edge case testing:

### 1. Invalid Python Path
Tests behavior when `PYTHONPATH` is corrupted or invalid.

### 2. Missing Dependencies
Simulates missing core modules to test import error handling.

### 3. Memory Constraints
Creates large graphs to test memory usage and constraints.

### 4. Timeout Scenarios
Uses configurable timeouts to prevent hanging examples.

## Artifacts and Reports

After each run, the workflow generates several artifacts:

### Test Results (`example-test-results`)
- Individual output files for each example
- Edge case test results
- Error logs and debugging information

### Test Summary (`example-test-summary`)
- Markdown summary of all test results
- Configuration details
- File size information
- Quick status overview

## Troubleshooting

### Common Issues

#### Example Timeout
**Problem**: Example exceeds the timeout limit
**Solution**: Increase the `timeout_minutes` parameter or optimize the example code

#### Import Errors
**Problem**: Module import failures
**Solution**: Check that all dependencies are properly installed and sys.path is correctly configured

#### Memory Issues
**Problem**: Out of memory errors during execution
**Solution**: Reduce graph size or increase runner resources

#### Missing Output Patterns
**Problem**: Output validation fails despite successful execution
**Solution**: Check that examples produce expected output messages

### Debugging Steps

1. **Check the workflow logs** in the GitHub Actions interface
2. **Download artifacts** to examine detailed output files
3. **Review the test summary** for quick issue identification
4. **Run examples locally** to reproduce issues
5. **Check dependencies** and environment setup

## Example Configurations

### Quick Validation (Fast)
```yaml
timeout_minutes: "2"
run_all_examples: "false"
```
- Tests only basic examples
- Short timeout for quick feedback
- Good for rapid iteration

### Comprehensive Testing (Thorough)
```yaml
timeout_minutes: "10"
run_all_examples: "true"
```
- Tests all examples
- Extended timeout for complex examples
- Recommended for release validation

### Development Testing (Balanced)
```yaml
timeout_minutes: "5"
run_all_examples: "true"
```
- Tests all examples with reasonable timeout
- Good balance of coverage and speed
- Default configuration

## Integration with Existing Workflows

This workflow complements the existing CI/CD pipeline:

- **CI Workflow**: Tests core functionality and unit tests
- **Code Quality**: Validates code style and complexity
- **Performance**: Tests system performance and benchmarks
- **Security**: Validates security aspects
- **Documentation**: Checks documentation completeness
- **Test Examples**: Validates example functionality ← **This workflow**

## Maintenance

### Adding New Examples
1. Add the example file to the `examples/` directory
2. Ensure proper sys.path setup in the example
3. Add a new test step in the workflow
4. Update output validation patterns
5. Update this documentation

### Modifying Validation
1. Update output validation patterns in the workflow
2. Test validation changes locally
3. Update expected patterns in documentation

### Performance Optimization
1. Monitor execution times in workflow logs
2. Optimize slow examples if needed
3. Adjust timeout parameters as necessary
4. Consider parallel execution for independent examples

## Best Practices

### For Example Authors
- Include proper sys.path setup at the beginning
- Add clear output messages for validation
- Include cleanup code to prevent resource leaks
- Test examples locally before committing
- Document expected runtime and resource usage

### For Workflow Users
- Use appropriate timeout values for your needs
- Enable all examples for comprehensive testing before releases
- Check artifacts when issues occur
- Report persistent failures to the development team
- Use shorter timeouts for iterative development

## Security Considerations

- The workflow runs in a sandboxed environment
- Examples should not access external resources without proper error handling
- Sensitive data should not be included in example outputs
- Network access is limited in the GitHub Actions environment