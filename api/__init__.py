"""
API package for SFM Graph Service.

This package contains modules related to the API layer of the service,
including route definitions and dependency injection for FastAPI.
"""

# Optionally, expose main API components for easier imports:
from .sfm_api import app, get_sfm_service_dependency
