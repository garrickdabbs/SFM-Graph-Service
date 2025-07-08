#!/usr/bin/env python3
"""
Demonstration of enhanced security validation features.

This script shows the new security enhancements in action:
1. Advanced sanitization with bleach
2. Rate limiting for validation operations
3. Enhanced logging for security validation failures
"""

import logging
import time
from core.security_validators import (
    sanitize_string,
    validate_metadata,
    validate_url,
    validate_node_label,
    SecurityValidationError,
    set_validation_caller_context,
    get_validation_rate_limit_status,
    enable_validation_rate_limiting,
    disable_validation_rate_limiting,
    clear_validation_rate_limit_storage,
)

# Configure logging to see the enhanced logging features
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def demonstrate_enhanced_sanitization():
    """Demonstrate advanced sanitization features."""
    print("\n=== Enhanced Sanitization Demo ===")
    
    # Test cases
    test_strings = [
        "Normal text",
        "Text with <b>bold</b> tags",
        "<script>alert('xss')</script>",
        "Text with 'quotes' and \"double quotes\"",
        "Mixed <script>alert('xss')</script> and <b>bold</b> content",
    ]
    
    for text in test_strings:
        try:
            result = sanitize_string(text)
            print(f"✓ '{text}' -> '{result}'")
        except SecurityValidationError as e:
            print(f"✗ '{text}' -> BLOCKED: {e.message}")
            print(f"  Context: {e.context}")

def demonstrate_rate_limiting():
    """Demonstrate rate limiting for validation operations."""
    print("\n=== Rate Limiting Demo ===")
    
    # Enable rate limiting
    enable_validation_rate_limiting()
    clear_validation_rate_limit_storage()
    
    # Set caller context
    set_validation_caller_context("demo_client_123")
    
    print("Making validation requests...")
    
    # Make several requests to show rate limiting in action
    for i in range(7):
        try:
            result = sanitize_string(f"test string {i}")
            print(f"✓ Request {i+1}: '{result}'")
        except SecurityValidationError as e:
            print(f"✗ Request {i+1}: RATE LIMITED: {e.message}")
        
        # Show rate limit status
        status = get_validation_rate_limit_status()
        print(f"  Rate limit status: {status['current_requests']}/{status['limit']} requests")
    
    # Disable rate limiting for cleanup
    disable_validation_rate_limiting()

def demonstrate_enhanced_logging():
    """Demonstrate enhanced logging for security validation failures."""
    print("\n=== Enhanced Logging Demo ===")
    
    # Create a custom logger to capture security events
    security_logger = logging.getLogger('core.security_validators')
    security_logger.setLevel(logging.DEBUG)
    
    # Test cases that will trigger logging
    test_cases = [
        ("", "Empty string"),
        ("a" * 1001, "String too long"),
        ("<script>alert('xss')</script>", "Dangerous content"),
        ("javascript:alert('xss')", "URL validation"),
    ]
    
    for test_input, description in test_cases:
        print(f"\nTesting: {description}")
        try:
            if "URL" in description:
                from core.security_validators import validate_url
                validate_url(test_input)
            else:
                sanitize_string(test_input)
        except SecurityValidationError as e:
            print(f"Exception caught: {e.message}")
            print(f"Field: {e.field}")
            print(f"Context: {e.context}")
            print(f"Timestamp: {e.timestamp}")

def demonstrate_metadata_validation():
    """Demonstrate enhanced metadata validation."""
    print("\n=== Metadata Validation Demo ===")
    
    # Test various metadata scenarios
    test_metadata = [
        ({"safe_key": "safe_value"}, "Safe metadata"),
        ({"key": "<script>alert('xss')</script>"}, "Dangerous metadata value"),
        ({"level1": {"level2": {"level3": {"level4": "too deep"}}}}, "Too deep nesting"),
        ({f"key_{i}": f"value_{i}" for i in range(52)}, "Too many keys"),
    ]
    
    for metadata, description in test_metadata:
        print(f"\nTesting: {description}")
        try:
            result = validate_metadata(metadata)
            print(f"✓ Validation passed: {len(result)} keys")
        except SecurityValidationError as e:
            print(f"✗ Validation failed: {e.message}")
            print(f"  Field: {e.field}")
            print(f"  Context: {e.context}")

def demonstrate_node_validation():
    """Demonstrate comprehensive node data validation."""
    print("\n=== Node Data Validation Demo ===")
    
    from core.security_validators import validate_and_sanitize_node_data
    
    # Test node data scenarios
    test_nodes = [
        ({"name": "Safe Node", "description": "Safe description"}, "Safe node"),
        ({"name": "<script>alert('xss')</script>", "description": "Test"}, "Dangerous node name"),
        ({"name": "Test", "description": "a" * 2001}, "Description too long"),
        ({"name": "Test", "meta": {"key": "value"}}, "Node with metadata"),
    ]
    
    for node_data, description in test_nodes:
        print(f"\nTesting: {description}")
        try:
            result = validate_and_sanitize_node_data(node_data)
            print(f"✓ Validation passed: {result}")
        except SecurityValidationError as e:
            print(f"✗ Validation failed: {e.message}")
            print(f"  Field: {e.field}")
            print(f"  Context: {e.context}")

if __name__ == "__main__":
    print("Enhanced Security Validation Features Demo")
    print("=" * 50)
    
    # Disable rate limiting initially for demos
    disable_validation_rate_limiting()
    
    try:
        demonstrate_enhanced_sanitization()
        demonstrate_enhanced_logging()
        demonstrate_metadata_validation()
        demonstrate_node_validation()
        demonstrate_rate_limiting()
    except Exception as e:
        print(f"\nDemo error: {e}")
    finally:
        # Clean up
        disable_validation_rate_limiting()
        clear_validation_rate_limit_storage()
    
    print("\n" + "=" * 50)
    print("Demo completed!")