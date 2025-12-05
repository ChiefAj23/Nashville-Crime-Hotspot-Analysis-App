"""
Test Runner - Run all test cases
TDD: Execute all tests to verify implementation
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_all_tests():
    """Run all test suites"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test modules
    test_modules = [
        'test_route_planning',
        'test_time_analysis',
        'test_emergency_contacts',
        'test_nearby_places',
        'test_historical_trends',
        'test_weather_integration',
        'test_user_preferences'
    ]

    for module_name in test_modules:
        try:
            module = __import__(f'tests.{module_name}', fromlist=[module_name])
            tests = loader.loadTestsFromModule(module)
            suite.addTests(tests)
            print(f"✅ Loaded tests from {module_name}")
        except ImportError as e:
            print(f"⚠️  Could not load {module_name}: {e}")

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.testsRun - len(result.failures) - len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}")

    if result.errors:
        print("\n❌ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}")

    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

