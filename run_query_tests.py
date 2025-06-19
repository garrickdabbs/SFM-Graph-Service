"""
Test runner for SFM Query Engine tests.
This script runs all the tests for the SFM query functionality.
"""

import sys
import os
import unittest

# Add the project root to Python path so we can import modules
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def run_sfm_query_tests():
    """Run all SFM query engine tests."""
    # Import test modules
    from tests.sfm_query_test import (
        TestSFMQueryEngineAbstract,
        TestDataClasses,
        TestNetworkXSFMQueryEngineUnit,
        TestSFMQueryFactory,
        TestNetworkXSFMQueryEngineIntegration,
        TestEdgeCases,
        TestPerformance
    )
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestSFMQueryEngineAbstract,
        TestDataClasses,
        TestNetworkXSFMQueryEngineUnit,
        TestSFMQueryFactory,
        TestNetworkXSFMQueryEngineIntegration,
        TestEdgeCases,
        TestPerformance
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success/failure
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Running SFM Query Engine Tests...")
    print("=" * 50)
    
    success = run_sfm_query_tests()
    
    if success:
        print("\n" + "=" * 50)
        print("All tests passed! ✅")
        sys.exit(0)
    else:
        print("\n" + "=" * 50)
        print("Some tests failed! ❌")
        sys.exit(1)
