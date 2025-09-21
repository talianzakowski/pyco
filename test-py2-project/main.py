#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Main application demonstrating Python 2 patterns that need conversion
"""

import sys
import os
from io import StringIO
import configparser
from functools import reduce

# Add local modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

from data_processor import DataProcessor
from string_helper import format_message, filter_strings
from settings import AppConfig

def demonstrate_python2_features():
    """Demonstrate various Python 2 features that need conversion"""

    print("=" * 60)
    print("PYTHON 2 LEGACY CODE DEMONSTRATION")
    print("=" * 60)

    # 1. Print statements
    print("1. Testing print statements")
    print("Hello", "World")
    print("Number:", 42)
    print()

    # 2. Raw input
    print("2. Testing raw input (commented out for automation)")
    # user_name = raw_input("What's your name? ")
    # print "Hello,", user_name
    print()

    # 3. Unicode strings
    print("3. Testing unicode strings")
    regular_string = "Regular string"
    unicode_string = "Unicode string: café"
    print("Regular:", repr(regular_string))
    print("Unicode:", repr(unicode_string))
    print()

    # 4. String formatting
    print("4. Testing old string formatting")
    template = "User %s has %d points"
    formatted = template % ("Alice", 150)
    print(formatted)
    print()

    # 5. xrange vs range
    print("5. Testing xrange")
    print("Numbers using xrange:", end=' ')
    for i in range(5):
        print(i, end=' ')
    print()
    print()

    # 6. Dictionary iteration
    print("6. Testing dictionary iteration")
    sample_dict = {'name': 'John', 'age': 30, 'city': 'Boston'}
    print("Dictionary contents:")
    for key, value in sample_dict.items():
        print("  %s: %s" % (key, value))
    print()

    # 7. Exception handling
    print("7. Testing exception handling")
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print("Caught exception:", e)
    print()

    # 8. File handling
    print("8. Testing file operations")
    test_content = "Line 1\nLine 2\nLine 3"
    test_file = StringIO(test_content)
    for line_num, line in enumerate(test_file):
        print("Line %d: %s" % (line_num + 1, line.strip()))
    test_file.close()
    print()

    # 9. Type checking
    print("9. Testing type checking")
    import types
    test_var = "test string"
    if type(test_var) == bytes:
        print("Found string type")
    print()

    # 10. Comparison function
    print("10. Testing comparison")
    try:
        comparison = cmp("apple", "banana")
        print("Comparison result:", comparison)
    except NameError:
        print("cmp function not available")
    print()

    # 11. Filter, map, reduce
    print("11. Testing filter/map operations")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    evens = [x for x in numbers if x % 2 == 0]
    print("Even numbers:", evens)

    squares = [x * x for x in numbers[:5]]
    print("Squares:", squares)

    try:
        total = reduce(lambda x, y: x + y, numbers[:5])
        print("Sum using reduce:", total)
    except NameError:
        print("reduce function not available")
    print()

    # 12. Integer division
    print("12. Testing division")
    print("5 / 2 =", 5 / 2)  # Integer division in Python 2
    print("5.0 / 2 =", 5.0 / 2)
    print()

def test_custom_modules():
    """Test our custom modules"""
    print("=" * 60)
    print("TESTING CUSTOM MODULES")
    print("=" * 60)

    # Test configuration
    print("Testing configuration module...")
    config = AppConfig()
    config.set_setting('app_name', 'Legacy App')
    print("App name:", config.get_setting('app_name'))
    print()

    # Test string helper
    print("Testing string helper...")
    message = format_message("Hello %s, version %d.%d", "User", 2, 7)
    print("Formatted message:", message)

    test_strings = ["hello", "", "world", "python"]
    filtered = filter_strings(test_strings)
    print("Filtered strings:", filtered)
    print()

    print("Custom module tests completed")

def main():
    """Main function"""
    print("Starting Python 2 legacy application...")
    print("Python version:", sys.version)
    print()

    try:
        demonstrate_python2_features()
        test_custom_modules()

        print("=" * 60)
        print("APPLICATION COMPLETED SUCCESSFULLY")
        print("This code contains many Python 2 patterns that need conversion!")
        print("=" * 60)

    except Exception as e:
        print("Application error:", e)
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)