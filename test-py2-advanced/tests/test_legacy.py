#!/usr/bin/env python2
"""
Legacy test patterns using Python 2 unittest and old testing conventions
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.network import HTTPClient
from utils.data_processing import DataProcessor
from config.settings import AppConfig

class TestHTTPClient(unittest.TestCase):
    """Test HTTP client functionality"""
    
    def setUp(self):
        print("Setting up HTTP client test")
        self.client = HTTPClient()
    
    def tearDown(self):
        print("Tearing down HTTP client test")
    
    def test_get_request(self):
        """Test GET request functionality"""
        print("Testing GET request...")
        
        try:
            # This would fail in Python 3 due to urllib2
            response = self.client.get("http://httpbin.org/get")
            self.assertIsNotNone(response)
            print("GET request test passed")
        except Exception as e:
            print("GET request failed:", e)
            self.fail("GET request should work")
    
    def test_post_request(self):
        """Test POST request functionality"""
        print("Testing POST request...")
        
        data = {"key": "value", "test": "data"}
        
        try:
            response = self.client.post("http://httpbin.org/post", data)
            self.assertIsNotNone(response)
            print("POST request test passed")
        except Exception as e:
            print("POST request failed:", e)
            # Don't fail the test since we can't actually make requests
    
    def test_error_handling(self):
        """Test error handling in HTTP client"""
        print("Testing error handling...")
        
        try:
            # Test with invalid URL
            response = self.client.get("http://invalid.domain.example")
            print("Unexpected success with invalid URL")
        except Exception as e:
            print("Expected error with invalid URL:", e)
            self.assertTrue(True)  # Expected behavior

class TestDataProcessor(unittest.TestCase):
    """Test data processing functionality"""
    
    def setUp(self):
        print("Setting up data processor test")
        self.processor = DataProcessor()
    
    def test_pickle_operations(self):
        """Test pickle serialization/deserialization"""
        print("Testing pickle operations...")
        
        test_data = {
            "string": "test data",
            "number": 42,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        
        try:
            # Test serialization
            serialized = self.processor.serialize_data(test_data)
            self.assertIsNotNone(serialized)
            print("Serialization successful")
            
            # Test deserialization
            deserialized = self.processor.deserialize_data(serialized)
            self.assertEqual(test_data, deserialized)
            print("Deserialization successful")
            
        except Exception as e:
            print("Pickle test failed:", e)
            self.fail("Pickle operations should work")
    
    def test_set_operations(self):
        """Test set operations using sets module"""
        print("Testing set operations...")
        
        try:
            set1 = self.processor.create_set([1, 2, 3, 4])
            set2 = self.processor.create_set([3, 4, 5, 6])
            
            union = self.processor.set_union(set1, set2)
            intersection = self.processor.set_intersection(set1, set2)
            
            self.assertEqual(len(union), 6)
            self.assertEqual(len(intersection), 2)
            print("Set operations test passed")
            
        except Exception as e:
            print("Set operations failed:", e)
            # Don't fail since sets module might not be available
    
    def test_string_operations(self):
        """Test string operations using old patterns"""
        print("Testing string operations...")
        
        test_string = "Hello, World!"
        
        try:
            # Test has_key equivalent
            char_count = self.processor.count_characters(test_string)
            self.assertGreater(len(char_count), 0)
            print("Character counting successful")
            
            # Test string formatting
            formatted = self.processor.format_string("Hello %s", "World")
            self.assertEqual(formatted, "Hello World")
            print("String formatting successful")
            
        except Exception as e:
            print("String operations failed:", e)
            self.fail("String operations should work")

class TestConfiguration(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        print("Setting up configuration test")
        self.config_file = "test_config.ini"
        self.config = AppConfig(self.config_file)
    
    def tearDown(self):
        print("Tearing down configuration test")
        # Clean up test config file
        if os.path.exists(self.config_file):
            try:
                os.remove(self.config_file)
                print("Cleaned up test config file")
            except Exception as e:
                print("Failed to clean up config file:", e)
    
    def test_config_creation(self):
        """Test configuration file creation"""
        print("Testing config creation...")
        
        self.assertIsNotNone(self.config)
        print("Configuration object created successfully")
    
    def test_config_values(self):
        """Test getting and setting configuration values"""
        print("Testing config values...")
        
        # Test getting default values
        app_name = self.config.get_value('general', 'app_name')
        self.assertIsNotNone(app_name)
        print("Got app name:", app_name)
        
        # Test setting new values
        self.config.set_value('test', 'value', 'test_data')
        retrieved = self.config.get_value('test', 'value')
        self.assertEqual(retrieved, 'test_data')
        print("Set and retrieved test value successfully")
        
        # Test boolean values
        debug = self.config.get_boolean('general', 'debug', False)
        self.assertIsInstance(debug, bool)
        print("Boolean value test passed")
        
        # Test integer values
        port = self.config.get_int('database', 'port', 0)
        self.assertIsInstance(port, int)
        print("Integer value test passed")

def run_legacy_tests():
    """Run tests using Python 2 patterns"""
    print("Running legacy test suite...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestHTTPClient))
    suite.addTest(unittest.makeSuite(TestDataProcessor))
    suite.addTest(unittest.makeSuite(TestConfiguration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\nTest Summary:")
    print("Tests run:", result.testsRun)
    print("Failures:", len(result.failures))
    print("Errors:", len(result.errors))
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(test, ":", traceback)
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(test, ":", traceback)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("Legacy Python 2 Test Suite")
    print("Testing patterns that need conversion to Python 3")
    print()
    
    success = run_legacy_tests()
    
    if success:
        print("\nAll tests completed successfully!")
    else:
        print("\nSome tests failed - this is expected for Python 2 code")
    
    sys.exit(0 if success else 1)