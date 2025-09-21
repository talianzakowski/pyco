#!/usr/bin/env python2
"""
String utilities with Python 2 patterns
"""

import string
import types
from functools import reduce

def format_message(template, *args, **kwargs):
    """Format message using old string formatting"""
    print(("Formatting template:", template))

    # Old % formatting
    if args:
        result = template % args
    else:
        result = template % kwargs

    print(("Formatted result:", result))
    return result

def check_string_type(value):
    """Check string types using old Python 2 methods"""
    if type(value) == bytes:
        print("Found regular string")
        return "str"
    elif type(value) == str:
        print("Found unicode string")
        return "unicode"
    else:
        print("Not a string type")
        return "other"

def process_text_file(filename):
    """Process text file with old file handling"""
    try:
        file_obj = file(filename, 'r')
        content = file_obj.read()
        file_obj.close()

        # Process lines
        lines = content.splitlines()
        for line_num in range(len(lines)):
            line = lines[line_num]
            if line.strip():
                print(("Line %d: %s" % (line_num + 1, line[:50])))

        return len(lines)
    except IOError as e:
        print(("Error reading file:", e))
        return 0

def compare_strings(str1, str2):
    """Compare strings using old comparison methods"""
    print("Comparing strings:")
    print(("  String 1: %r" % str1))
    print(("  String 2: %r" % str2))

    # Old comparison
    if cmp(str1, str2) == 0:
        print("Strings are equal")
        return True
    elif cmp(str1, str2) < 0:
        print("String 1 is less than String 2")
        return False
    else:
        print("String 1 is greater than String 2")
        return False

def filter_strings(string_list):
    """Filter strings using old filter/map patterns"""
    print(("Original list:", string_list))

    # Old filter usage
    non_empty = [_f for _f in string_list if _f]
    print(("Non-empty strings:", non_empty))

    # Old map usage
    lengths = list(map(len, non_empty))
    print(("String lengths:", lengths))

    # Old reduce usage
    try:
        total_length = reduce(lambda x, y: x + y, lengths, 0)
        print(("Total length:", total_length))
    except NameError:
        # reduce might not be available
        total_length = sum(lengths)
        print(("Total length (using sum):", total_length))

    return non_empty

if __name__ == "__main__":
    # Test the functions
    print("=== String Helper Tests ===")

    # Test formatting
    msg = format_message("Hello %s, you have %d messages", "Alice", 5)

    # Test string types
    regular_str = "Hello"
    unicode_str = "Hello Unicode"
    check_string_type(regular_str)
    check_string_type(unicode_str)

    # Test string comparison
    compare_strings("apple", "banana")
    compare_strings("test", "test")

    # Test filtering
    test_strings = ["hello", "", "world", None, "python"]
    filtered = filter_strings(test_strings)
    print(("Filtered result:", filtered))