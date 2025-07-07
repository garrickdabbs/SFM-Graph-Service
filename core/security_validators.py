"""
Security validation utilities for SFM input sanitization and validation.

This module provides functions to sanitize and validate user inputs to prevent
security vulnerabilities like XSS attacks, injection attacks, and other
malicious input-based exploits.

Security measures implemented:
- HTML/script tag sanitization
- Length limits for string inputs
- Metadata validation and sanitization
- URL validation
- Input type validation
"""

import re
import html
import logging
from typing import Any, Dict, Optional, List, cast
from urllib.parse import urlparse

# Configure logging
logger = logging.getLogger(__name__)

# Public API
__all__ = [
    'SecurityValidationError',
    'sanitize_string',
    'sanitize_description',
    'validate_metadata',
    'validate_url',
    'validate_node_label',
    'validate_node_description',
    'validate_and_sanitize_node_data',
    'MAX_STRING_LENGTH',
    'MAX_DESCRIPTION_LENGTH',
]

# Security configuration constants
MAX_STRING_LENGTH = 1000
MAX_DESCRIPTION_LENGTH = 2000
MAX_METADATA_KEYS = 50
MAX_METADATA_VALUE_LENGTH = 500
MAX_METADATA_DEPTH = 3

# Dangerous patterns to detect and sanitize
DANGEROUS_PATTERNS = [
    r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>',  # Script tags
    r'javascript:',  # JavaScript URLs
    r'vbscript:',    # VBScript URLs
    r'on\w+\s*=',    # Event handlers (onclick, onload, etc.)
    r'eval\s*\(',    # eval() calls
    r'expression\s*\(',  # CSS expressions
]

# Compile regex patterns for better performance
DANGEROUS_REGEX = re.compile('|'.join(DANGEROUS_PATTERNS), re.IGNORECASE)


class SecurityValidationError(Exception):
    """Raised when input fails security validation."""

    def __init__(self, message: str, field: Optional[str] = None,
                 value: Optional[Any] = None) -> None:
        self.message = message
        self.field = field
        self.value = value
        super().__init__(message)


def sanitize_string(value: str, max_length: int = MAX_STRING_LENGTH) -> str:
    """
    Sanitize a string input by removing dangerous content and limiting length.

    Args:
        value: The string to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized string

    Raises:
        SecurityValidationError: If string is too long or contains dangerous patterns
    """
    # Ensure the input is treated as a string
    value = str(value)

    # Check length
    if len(value) > max_length:
        raise SecurityValidationError(
            f"String too long: {len(value)} > {max_length}",
            field="length",
            value=value[:50] + "..." if len(value) > 50 else value
        )

    # HTML escape to prevent XSS
    sanitized = html.escape(value, quote=True)

    # Check for dangerous patterns
    if DANGEROUS_REGEX.search(value):
        logger.warning("Dangerous pattern detected in input: %s", value[:100])
        raise SecurityValidationError(
            "Input contains potentially dangerous content",
            field="content",
            value=value[:50] + "..." if len(value) > 50 else value
        )

    return sanitized


def sanitize_description(value: str) -> str:
    """
    Sanitize a description field with longer length allowance.

    Args:
        value: The description to sanitize

    Returns:
        Sanitized description
    """
    return sanitize_string(value, MAX_DESCRIPTION_LENGTH)


def validate_metadata(metadata: Dict[str, Any],
                      max_depth: int = MAX_METADATA_DEPTH) -> Dict[str, Any]:
    """
    Validate and sanitize metadata dictionary.

    Args:
        metadata: Dictionary to validate
        max_depth: Maximum nesting depth allowed

    Returns:
        Sanitized metadata dictionary

    Raises:
        SecurityValidationError: If metadata fails validation
    """
    if len(metadata) > MAX_METADATA_KEYS:
        raise SecurityValidationError(
            f"Too many metadata keys: {len(metadata)} > {MAX_METADATA_KEYS}",
            field="keys",
            value=len(metadata)
        )

    return _sanitize_dict(metadata, max_depth)


def _sanitize_dict(data: Dict[Any, Any], depth: int) -> Dict[str, Any]:
    """
    Recursively sanitize dictionary values.

    Args:
        data: Dictionary to sanitize
        depth: Current nesting depth

    Returns:
        Sanitized dictionary
    """
    if depth <= 0:
        raise SecurityValidationError("Metadata nesting too deep", field="depth", value=depth)

    sanitized: Dict[str, Any] = {}
    for key, value in data.items():
        # Sanitize key
        key_str: str = str(key)
        sanitized_key = sanitize_string(key_str, MAX_METADATA_VALUE_LENGTH)

        # Sanitize value based on type
        if isinstance(value, str):
            sanitized[sanitized_key] = sanitize_string(value, MAX_METADATA_VALUE_LENGTH)
        elif isinstance(value, dict):
            sanitized[sanitized_key] = _sanitize_dict(cast(Dict[Any, Any], value), depth - 1)
        elif isinstance(value, list):
            sanitized[sanitized_key] = _sanitize_list(cast(List[Any], value), depth - 1)
        elif isinstance(value, (int, float, bool)):
            sanitized[sanitized_key] = value
        elif value is None:
            sanitized[sanitized_key] = None
        else:
            # Convert unknown types to sanitized strings
            sanitized[sanitized_key] = sanitize_string(str(value), MAX_METADATA_VALUE_LENGTH)

    return sanitized


def _sanitize_list(data: List[Any], depth: int) -> List[Any]:
    """
    Recursively sanitize list values.

    Args:
        data: List to sanitize
        depth: Current nesting depth

    Returns:
        Sanitized list
    """
    if depth <= 0:
        raise SecurityValidationError("Metadata nesting too deep", field="depth", value=depth)

    sanitized: List[Any] = []
    for item in data:
        if isinstance(item, str):
            sanitized.append(sanitize_string(item, MAX_METADATA_VALUE_LENGTH))
        elif isinstance(item, dict):
            sanitized.append(_sanitize_dict(cast(Dict[Any, Any], item), depth - 1))
        elif isinstance(item, list):
            sanitized.append(_sanitize_list(cast(List[Any], item), depth - 1))
        elif isinstance(item, (int, float, bool)):
            sanitized.append(item)
        elif item is None:
            sanitized.append(None)
        else:
            sanitized.append(sanitize_string(str(item), MAX_METADATA_VALUE_LENGTH))

    return sanitized


def validate_url(url: str) -> bool:
    """
    Validate that a URL is safe and properly formatted.

    Args:
        url: URL to validate

    Returns:
        True if URL is valid and safe

    Raises:
        SecurityValidationError: If URL is invalid or unsafe
    """
    if not url:
        raise SecurityValidationError("URL must be a non-empty string", field="type", value=url)

    # Check for dangerous URL schemes
    if url.lower().startswith(('javascript:', 'vbscript:', 'data:')):
        raise SecurityValidationError("Dangerous URL scheme detected", field="scheme", value=url)

    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise SecurityValidationError("Invalid URL format", field="format", value=url)
    except Exception as e:
        raise SecurityValidationError(f"URL parsing failed: {str(e)}", field="parsing",
                                      value=url) from e

    return True


def validate_node_label(label: str) -> str:
    """
    Validate and sanitize a node label.

    Args:
        label: Label to validate

    Returns:
        Sanitized label
    """
    if not label:
        raise SecurityValidationError("Label must be a non-empty string", field="label",
                                      value=label)

    return sanitize_string(label.strip())


def validate_node_description(description: Optional[str]) -> Optional[str]:
    """
    Validate and sanitize a node description.

    Args:
        description: Description to validate

    Returns:
        Sanitized description or None
    """
    if description is None:
        return None

    description = str(description)

    return sanitize_description(description.strip())


def validate_and_sanitize_node_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Comprehensive validation and sanitization of node data.

    Args:
        data: Dictionary containing node data

    Returns:
        Sanitized node data dictionary
    """
    sanitized: Dict[str, Any] = {}

    # Validate required fields
    if "name" in data:
        sanitized["name"] = validate_node_label(data["name"])

    if "label" in data:
        sanitized["label"] = validate_node_label(data["label"])

    if "description" in data:
        sanitized["description"] = validate_node_description(data["description"])

    # Validate metadata
    if "meta" in data and data["meta"]:
        sanitized["meta"] = validate_metadata(data["meta"])
    elif "meta" in data:
        sanitized["meta"] = {}

    # Copy other fields with basic validation
    for key, value in data.items():
        if key not in ["name", "label", "description", "meta"]:
            if isinstance(value, str):
                sanitized[key] = sanitize_string(value)
            else:
                sanitized[key] = value

    return sanitized
