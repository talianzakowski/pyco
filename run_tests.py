#!/usr/bin/env python3
"""
Minimal test runner for GitHub Actions debugging
"""
import sys
import os

# Add src to path first thing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

print("=== Minimal Test Runner ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Added to path: {os.path.join(os.path.dirname(__file__), 'src')}")

# List test files
print("\n=== Test Files ===")
test_files = []
for root, dirs, files in os.walk('tests'):
    for file in files:
        if file.startswith('test_') and file.endswith('.py'):
            full_path = os.path.join(root, file)
            test_files.append(full_path)
            print(f"Found: {full_path}")

if not test_files:
    print("❌ No test files found!")
    sys.exit(1)

# Try to import test modules
print("\n=== Import Test ===")
import importlib.util

for test_file in test_files:
    try:
        spec = importlib.util.spec_from_file_location("test_module", test_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✅ {test_file} imported successfully")
    except Exception as e:
        print(f"❌ {test_file} import failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

# Now try unittest discovery
print("\n=== Test Discovery ===")
import unittest

loader = unittest.TestLoader()
try:
    suite = loader.discover('tests', pattern='test_*.py')
    test_count = suite.countTestCases()
    print(f"✅ Test discovery successful: {test_count} tests found")
    
    if test_count > 0:
        print("\n=== Running Tests ===")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print("✅ All tests passed!")
            sys.exit(0)
        else:
            print(f"❌ Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
            sys.exit(1)
    else:
        print("❌ No tests discovered")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Test discovery failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)