"""
Test Runner - Run all tests with detailed output
TDD: Execute all tests to verify implementation
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_tests():
    """Run all test suites with detailed output"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Test modules
    test_modules = [
        'test_route_planning',
        'test_time_analysis',
        'test_emergency_contacts',
        'test_nearby_places',
        'test_historical_trends',
        'test_weather_integration',
        'test_user_preferences'
    ]

    print("="*60)
    print("🧪 TEST-DRIVEN DEVELOPMENT - TEST SUITE")
    print("="*60)
    print()

    loaded_count = 0
    for module_name in test_modules:
        try:
            module = __import__(f'tests.{module_name}', fromlist=[module_name])
            tests = loader.loadTestsFromModule(module)
            suite.addTests(tests)
            loaded_count += 1
            print(f"✅ Loaded: {module_name}")
        except ImportError as e:
            print(f"⚠️  Could not load {module_name}: {e}")
        except Exception as e:
            print(f"❌ Error loading {module_name}: {e}")

    print(f"\n📦 Loaded {loaded_count} test modules")
    print("="*60)
    print()

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Success: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print(f"⏭️  Skipped: {len(result.skipped)}")

    if result.failures:
        print("\n" + "="*60)
        print("❌ FAILURES:")
        print("="*60)
        for test, traceback in result.failures:
            print(f"\n🔴 {test}")
            print(traceback[:500] + "..." if len(traceback) > 500 else traceback)

    if result.errors:
        print("\n" + "="*60)
        print("⚠️  ERRORS:")
        print("="*60)
        for test, traceback in result.errors:
            print(f"\n🔴 {test}")
            print(traceback[:500] + "..." if len(traceback) > 500 else traceback)

    if result.wasSuccessful():
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ SOME TESTS FAILED - Review errors above")
        print("="*60)

    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

