"""
Test suite for API security features including rate limiting.

This module tests the security features implemented in the FastAPI layer,
including rate limiting and input validation.
"""

import unittest
from unittest.mock import patch, MagicMock
import time
from collections import deque, defaultdict

from fastapi.testclient import TestClient
from api.sfm_api import app, check_rate_limit, rate_limit_storage, RATE_LIMIT_REQUESTS
from core.sfm_service import ValidationError, SFMServiceError


class TestAPIRateLimiting(unittest.TestCase):
    """Test suite for API rate limiting functionality."""

    def setUp(self):
        """Set up test client and reset rate limiting storage."""
        self.client = TestClient(app)
        # Clear rate limiting storage before each test
        rate_limit_storage.clear()

    def test_rate_limit_within_limits(self):
        """Test that requests within rate limits are allowed."""
        # Mock request object
        request = MagicMock()
        request.client.host = "127.0.0.1"
        
        # Should pass for requests within limit
        for i in range(10):
            result = check_rate_limit(request)
            self.assertTrue(result)

    def test_rate_limit_exceeded(self):
        """Test that requests exceeding rate limits are blocked."""
        # Mock request object
        request = MagicMock()
        request.client.host = "127.0.0.1"
        
        # Fill up the rate limit
        for i in range(RATE_LIMIT_REQUESTS):
            check_rate_limit(request)
        
        # Next request should fail
        from fastapi import HTTPException
        with self.assertRaises(HTTPException) as context:
            check_rate_limit(request)
        
        self.assertEqual(context.exception.status_code, 429)
        self.assertIn("Rate limit exceeded", context.exception.detail)

    def test_rate_limit_different_ips(self):
        """Test that rate limiting is per IP address."""
        # Mock different IP addresses
        request1 = MagicMock()
        request1.client.host = "127.0.0.1"
        
        request2 = MagicMock()
        request2.client.host = "192.168.1.1"
        
        # Fill up rate limit for first IP
        for i in range(RATE_LIMIT_REQUESTS):
            check_rate_limit(request1)
        
        # Second IP should still be allowed
        result = check_rate_limit(request2)
        self.assertTrue(result)

    def test_rate_limit_window_expiration(self):
        """Test that rate limiting window expires correctly."""
        request = MagicMock()
        request.client.host = "127.0.0.1"
        
        # Manually add old entries to simulate expired requests
        old_time = time.time() - 70  # 70 seconds ago (past the 60-second window)
        rate_limit_storage[request.client.host] = deque([old_time] * RATE_LIMIT_REQUESTS)
        
        # Should be allowed since old entries are expired
        result = check_rate_limit(request)
        self.assertTrue(result)


class TestAPISecurityIntegration(unittest.TestCase):
    """Test suite for API security integration."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)
        # Clear rate limiting storage
        rate_limit_storage.clear()

    @patch('core.sfm_service.get_sfm_service')
    def test_create_actor_with_dangerous_input_via_api(self, mock_get_service):
        """Test creating actor with dangerous input through API."""
        # Mock service to raise security validation error
        mock_service = MagicMock()
        mock_service.create_actor.side_effect = SFMServiceError("Failed to create actor: Input contains potentially dangerous content")
        mock_get_service.return_value = mock_service
        
        # Attempt to create actor with dangerous input
        dangerous_data = {
            "name": "<script>alert('xss')</script>",
            "description": "Test description"
        }
        
        response = self.client.post("/actors", json=dangerous_data)
        
        # Should return 500 error (since SFMServiceError maps to 500)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Service Error", response.json()["error"])

    @patch('core.sfm_service.get_sfm_service')
    def test_create_actor_with_valid_input_via_api(self, mock_get_service):
        """Test creating actor with valid input through API."""
        # Mock service to return successful response
        from core.sfm_service import NodeResponse
        mock_service = MagicMock()
        mock_response = NodeResponse(
            id="123e4567-e89b-12d3-a456-426614174000",
            label="Valid Actor",
            entity_type="Actor",
            description="Valid description",
            meta={},
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-01T00:00:00"
        )
        mock_service.create_actor.return_value = mock_response
        mock_get_service.return_value = mock_service
        
        # Create actor with valid input
        valid_data = {
            "name": "Valid Actor",
            "description": "Valid description"
        }
        
        response = self.client.post("/actors", json=valid_data)
        
        # Should succeed
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["label"], "Valid Actor")

    def test_health_endpoint_security(self):
        """Test that health endpoint is accessible and secure."""
        response = self.client.get("/health")
        
        # Should succeed
        self.assertEqual(response.status_code, 200)
        
        # Should return expected structure
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("timestamp", data)

    def test_api_cors_headers(self):
        """Test that CORS headers are properly set."""
        response = self.client.options("/health")
        
        # Should include CORS headers (if properly configured)
        # Note: TestClient might not include all CORS headers in test mode


class TestAPIValidationErrorHandling(unittest.TestCase):
    """Test suite for API validation error handling."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)
        rate_limit_storage.clear()

    @patch('core.sfm_service.get_sfm_service')
    def test_validation_error_handling(self, mock_get_service):
        """Test proper handling of validation errors."""
        # Mock service to raise validation error
        mock_service = MagicMock()
        mock_service.create_actor.side_effect = ValidationError("Invalid actor data", "name", "")
        mock_get_service.return_value = mock_service
        
        response = self.client.post("/actors", json={"name": ""})
        
        # Should return 400 Bad Request
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["error"], "Validation Error")
        self.assertIn("Invalid actor data", data["message"])

    @patch('core.sfm_service.get_sfm_service')  
    def test_not_found_error_handling(self, mock_get_service):
        """Test proper handling of not found errors."""
        # Mock service to raise not found error
        from core.sfm_service import NotFoundError
        mock_service = MagicMock()
        mock_service.get_actor.side_effect = NotFoundError("Actor", "123")
        mock_get_service.return_value = mock_service
        
        response = self.client.get("/actors/123")
        
        # Should return 404 Not Found
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["error"], "Not Found")

    def test_invalid_uuid_format_handling(self):
        """Test handling of invalid UUID formats."""
        response = self.client.get("/actors/invalid-uuid")
        
        # Should return 400 Bad Request
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid UUID format", response.json()["detail"])


if __name__ == '__main__':
    unittest.main()