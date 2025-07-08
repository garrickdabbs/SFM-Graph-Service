# Security Validation Enhancements

This document describes the enhanced security validation features added to the SFM framework.

## Overview

The security validation system has been enhanced with three key improvements:

1. **Advanced Input Sanitization** - Using the `bleach` library for robust HTML cleaning
2. **Rate Limiting** - Configurable rate limiting for validation operations
3. **Enhanced Logging** - Comprehensive logging for all security validation failures

## Features

### Advanced Input Sanitization

The sanitization system now uses the `bleach` library in addition to HTML escaping:

```python
from core.security_validators import sanitize_string

# Basic sanitization
clean_text = sanitize_string("Hello <b>World</b>")
# Result: "Hello &lt;b&gt;World&lt;/b&gt;"

# Dangerous content is blocked
try:
    sanitize_string("<script>alert('xss')</script>")
except SecurityValidationError as e:
    print(f"Blocked: {e.message}")
```

### Rate Limiting

Validation operations can be rate-limited to prevent abuse:

```python
from core.security_validators import (
    enable_validation_rate_limiting,
    set_validation_caller_context,
    get_validation_rate_limit_status
)

# Enable rate limiting (50 requests per minute by default)
enable_validation_rate_limiting()

# Set caller context for tracking
set_validation_caller_context("client_ip_123")

# Check rate limit status
status = get_validation_rate_limit_status()
print(f"Requests: {status['current_requests']}/{status['limit']}")
```

### Enhanced Logging

All security validation failures are now logged with detailed context:

```python
import logging

# Configure logging to see security events
logging.basicConfig(level=logging.INFO)

try:
    sanitize_string("dangerous input")
except SecurityValidationError as e:
    # Error is automatically logged with:
    # - Timestamp
    # - Field that failed
    # - Truncated value
    # - Additional context
    print(f"Context: {e.context}")
    print(f"Timestamp: {e.timestamp}")
```

## Configuration

### Rate Limiting Settings

```python
from core.security_validators import (
    VALIDATION_RATE_LIMIT,      # 50 requests per minute
    VALIDATION_RATE_WINDOW,     # 60 seconds
)

# Disable rate limiting (useful for testing)
disable_validation_rate_limiting()

# Enable rate limiting
enable_validation_rate_limiting()

# Clear rate limiting storage
clear_validation_rate_limit_storage()
```

### Sanitization Settings

The bleach configuration allows specific HTML tags and attributes:

```python
ALLOWED_TAGS = ['b', 'i', 'em', 'strong', 'u', 'br', 'p']
ALLOWED_ATTRIBUTES = {}
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']
```

## API Integration

For API endpoints, set the caller context based on request IP:

```python
from fastapi import Request
from core.security_validators import set_validation_caller_context

@app.post("/api/endpoint")
async def endpoint(request: Request, data: dict):
    # Set caller context for rate limiting
    set_validation_caller_context(request.client.host)
    
    # Validation operations will now be rate-limited per IP
    validated_data = validate_and_sanitize_node_data(data)
    return validated_data
```

## Error Handling

The enhanced `SecurityValidationError` provides rich context:

```python
try:
    validate_metadata(large_metadata)
except SecurityValidationError as e:
    error_info = {
        "message": e.message,
        "field": e.field,
        "value": e.value,
        "context": e.context,
        "timestamp": e.timestamp
    }
    # Log or handle the structured error information
```

## Testing

For testing environments, disable rate limiting to avoid interference:

```python
# In test setup
from core.security_validators import disable_validation_rate_limiting
disable_validation_rate_limiting()

# Run tests normally
def test_validation():
    result = sanitize_string("test input")
    assert result == "test input"
```

## Backwards Compatibility

All existing functionality is preserved. The enhancements are additive:

- Existing validation functions work unchanged
- Rate limiting is optional and can be disabled
- Enhanced logging provides additional information without breaking existing error handling
- New dependencies are additive (bleach library)

## Security Considerations

1. **Rate Limiting**: Prevents abuse of validation endpoints
2. **Advanced Sanitization**: More robust protection against XSS attacks
3. **Comprehensive Logging**: Better monitoring and incident response
4. **Input Validation**: Stricter validation of user-facing fields

## Migration Guide

No migration is required for existing code. To take advantage of new features:

1. **For Rate Limiting**: Call `enable_validation_rate_limiting()` and set caller context
2. **For Enhanced Logging**: Configure logging level to INFO or DEBUG
3. **For API Integration**: Set caller context in request handlers

The system is designed for gradual adoption of enhanced features while maintaining full backwards compatibility.