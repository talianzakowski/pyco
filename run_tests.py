#!/usr/bin/env python3
"""
Simple test runner for GitHub Actions
"""
import sys
import os
import unittest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

def main():
    """Run all tests"""
    print("=== Test Runner Debug ===")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # Test imports
    try:
        from converter.engine import Python2to3Converter
        print("✅ converter.engine import successful")
    except Exception as e:
        print(f"❌ converter.engine import failed: {e}")
        return 1
        
    try:
        from tester.validator import ConvertedCodeValidator
        print("✅ tester.validator import successful")
    except Exception as e:
        print(f"❌ tester.validator import failed: {e}")
        return 1
    
    print("\n=== Running Tests ===")
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Count tests
    test_count = suite.countTestCases()
    print(f"Found {test_count} tests")
    
    if test_count == 0:
        print("❌ No tests found!")
        return 1
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return appropriate exit code
    if result.wasSuccessful():
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
        return 1

if __name__ == "__main__":
    sys.exit(main())