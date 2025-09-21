#!/usr/bin/env python2
"""
Test cases using Python 2 patterns
"""

import unittest
import sys
import os
from functools import reduce

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.string_helper import format_message, check_string_type

class TestLegacyCode(unittest.TestCase):
    """Test cases for legacy Python 2 code"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_strings = [
            "regular string",
            "unicode string",
            "",
            "special chars: café"
        ]

    def test_string_formatting(self):
        """Test old-style string formatting"""
        template = "Hello %s, count: %d"
        result = format_message(template, "World", 42)
        expected = "Hello World, count: 42"
        self.assertEqual(result, expected)

        print("String formatting test passed")

    def test_unicode_handling(self):
        """Test unicode string handling"""
        regular = "test"
        unicode_str = "test"

        type1 = check_string_type(regular)
        type2 = check_string_type(unicode_str)

        self.assertEqual(type1, "str")
        self.assertEqual(type2, "unicode")

        print("Unicode handling test passed")

    def test_exception_handling(self):
        """Test old-style exception handling"""
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            print(("Caught exception:", e))
            self.assertTrue(True)
        else:
            self.fail("Expected ZeroDivisionError")

    def test_dictionary_methods(self):
        """Test old dictionary methods"""
        test_dict = {'a': 1, 'b': 2, 'c': 3}

        # Test old iteration methods
        keys = list(test_dict.keys())
        values = list(test_dict.values())
        items = list(test_dict.items())

        self.assertEqual(len(keys), 3)
        self.assertEqual(len(values), 3)
        self.assertEqual(len(items), 3)

        # Test iteritems
        count = 0
        for key, value in list(test_dict.items()):
            print(("Item: %s = %s" % (key, value)))
            count += 1

        self.assertEqual(count, 3)

    def test_range_functions(self):
        """Test xrange vs range"""
        # Test xrange
        result = []
        for i in range(5):
            result.append(i)

        expected = [0, 1, 2, 3, 4]
        self.assertEqual(result, expected)

        print("Range function test passed")

    def test_comparison_function(self):
        """Test old cmp function"""
        try:
            result1 = cmp("apple", "banana")
            result2 = cmp("test", "test")
            result3 = cmp("zebra", "apple")

            self.assertEqual(result1, -1)
            self.assertEqual(result2, 0)
            self.assertEqual(result3, 1)

            print("Comparison function test passed")
        except NameError:
            print("cmp function not available")
            self.skipTest("cmp function not available")

    def test_filter_map_reduce(self):
        """Test old filter, map, reduce patterns"""
        numbers = [1, 2, 3, 4, 5]

        # Test filter
        evens = [x for x in numbers if x % 2 == 0]
        self.assertEqual(list(evens), [2, 4])

        # Test map
        squares = [x * x for x in numbers]
        self.assertEqual(list(squares), [1, 4, 9, 16, 25])

        # Test reduce (if available)
        try:
            total = reduce(lambda x, y: x + y, numbers)
            self.assertEqual(total, 15)
            print("Filter/map/reduce test passed")
        except NameError:
            print("reduce function not available")

    def test_old_division(self):
        """Test old division behavior"""
        # Integer division in Python 2
        result1 = 5 / 2
        result2 = 5.0 / 2

        # In Python 2, 5/2 = 2 (integer division)
        # In Python 3, 5/2 = 2.5 (true division)
        print(("Division results: %s, %s" % (result1, result2)))

        # This test may behave differently in Python 2 vs 3
        self.assertTrue(isinstance(result2, float))

def run_tests():
    """Run all tests"""
    print("Running legacy code tests...")
    print(("=" * 50))

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLegacyCode)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(("=" * 50))
    print(("Tests run: %d" % result.testsRun))
    print(("Failures: %d" % len(result.failures)))
    print(("Errors: %d" % len(result.errors)))

    return result

if __name__ == "__main__":
    run_tests()