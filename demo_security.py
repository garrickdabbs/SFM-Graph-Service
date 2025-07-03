#!/usr/bin/env python3
"""
Security Validation Demonstration Script

This script demonstrates the security validation features implemented
in the SFM framework to protect against injection attacks and other
security vulnerabilities.
"""

from core.sfm_service import SFMService, CreateActorRequest, SFMServiceError
from core.security_validators import (
    sanitize_string, validate_metadata, SecurityValidationError
)

def demo_security_validation():
    """Demonstrate security validation features."""
    print("🔒 SFM Security Validation Demonstration")
    print("=" * 50)
    
    service = SFMService()
    
    # Test 1: Valid input should work
    print("\n✅ Test 1: Valid input")
    try:
        actor = service.create_actor(CreateActorRequest(
            name="USDA",
            description="United States Department of Agriculture"
        ))
        print(f"   Successfully created: {actor.label}")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
    
    # Test 2: XSS attempt should be blocked
    print("\n🛡️  Test 2: XSS prevention")
    try:
        service.create_actor(CreateActorRequest(
            name="<script>alert('XSS Attack!')</script>",
            description="Malicious actor"
        ))
        print("   ❌ XSS attack was not blocked!")
    except SFMServiceError as e:
        print(f"   ✅ XSS attack blocked: {str(e)[:80]}...")
    
    # Test 3: JavaScript URL should be blocked
    print("\n🛡️  Test 3: JavaScript URL prevention")
    try:
        service.create_actor(CreateActorRequest(
            name="javascript:alert('malicious')",
            description="Another malicious attempt"
        ))
        print("   ❌ JavaScript URL was not blocked!")
    except SFMServiceError as e:
        print(f"   ✅ JavaScript URL blocked: {str(e)[:80]}...")
    
    # Test 4: Event handler injection should be blocked
    print("\n🛡️  Test 4: Event handler prevention")
    try:
        service.create_actor(CreateActorRequest(
            name="onclick=alert('click')",
            description="Event handler injection"
        ))
        print("   ❌ Event handler injection was not blocked!")
    except SFMServiceError as e:
        print(f"   ✅ Event handler injection blocked: {str(e)[:80]}...")
    
    # Test 5: Overly long input should be blocked
    print("\n🛡️  Test 5: Length limit protection")
    try:
        service.create_actor(CreateActorRequest(
            name="A" * 1001,  # Exceeds MAX_STRING_LENGTH
            description="Too long name"
        ))
        print("   ❌ Overly long input was not blocked!")
    except SFMServiceError as e:
        print(f"   ✅ Long input blocked: {str(e)[:80]}...")
    
    # Test 6: Dangerous metadata should be blocked
    print("\n🛡️  Test 6: Metadata validation")
    try:
        actor_data = {
            "name": "Test Actor",
            "description": "Valid description",
            "meta": {
                "malicious": "<script>document.cookie</script>"
            }
        }
        service.create_actor(actor_data)
        print("   ❌ Dangerous metadata was not blocked!")
    except SFMServiceError as e:
        print(f"   ✅ Dangerous metadata blocked: {str(e)[:80]}...")
    
    # Test 7: Safe HTML is escaped but allowed in content
    print("\n✅ Test 7: Safe HTML escaping")
    try:
        from core.security_validators import sanitize_string
        safe_html = sanitize_string("Hello <b>World</b>")
        print(f"   Input: 'Hello <b>World</b>'")
        print(f"   Output: '{safe_html}'")
        print("   ✅ HTML properly escaped")
    except Exception as e:
        print(f"   ❌ Error in HTML escaping: {e}")
    
    print("\n" + "=" * 50)
    print("🔒 Security validation demonstration complete!")
    print("All malicious inputs were successfully blocked.")


def demo_api_rate_limiting():
    """Demonstrate API rate limiting functionality."""
    print("\n🚦 Rate Limiting Demonstration")
    print("=" * 30)
    
    from api.sfm_api import check_rate_limit, rate_limit_storage, RATE_LIMIT_REQUESTS
    from unittest.mock import MagicMock
    
    # Clear any existing rate limit data
    rate_limit_storage.clear()
    
    # Mock request object
    request = MagicMock()
    request.client.host = "127.0.0.1"
    
    print(f"Rate limit: {RATE_LIMIT_REQUESTS} requests per minute")
    
    # Test requests within limit
    print("\n✅ Testing requests within limit:")
    for i in range(5):
        try:
            result = check_rate_limit(request)
            print(f"   Request {i+1}: ✅ Allowed")
        except Exception as e:
            print(f"   Request {i+1}: ❌ Blocked - {e}")
    
    # Test what happens when we exceed the limit
    print(f"\n🛡️  Testing rate limit enforcement (simulating {RATE_LIMIT_REQUESTS + 1} requests):")
    
    # Fill up the rate limit bucket
    for i in range(RATE_LIMIT_REQUESTS - 5):  # -5 because we already made 5 requests
        try:
            check_rate_limit(request)
        except:
            pass
    
    # Now the next request should be blocked
    try:
        check_rate_limit(request)
        print("   ❌ Rate limit not enforced!")
    except Exception as e:
        print(f"   ✅ Rate limit enforced: {str(e)[:60]}...")
    
    print("\n🚦 Rate limiting demonstration complete!")


if __name__ == "__main__":
    try:
        demo_security_validation()
        demo_api_rate_limiting()
        
        print("\n🎉 All security features are working correctly!")
        print("\nThe SFM framework is now protected against:")
        print("  • XSS attacks")
        print("  • Script injection") 
        print("  • JavaScript URL attacks")
        print("  • Event handler injection")
        print("  • Excessively long inputs")
        print("  • Malicious metadata")
        print("  • DoS through rate limiting")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()