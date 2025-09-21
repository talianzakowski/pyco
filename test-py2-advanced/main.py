#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Advanced Python 2 Test Project - Main Application
This file contains various Python 2 patterns for comprehensive testing
"""

import sys
import os
from StringIO import StringIO
import ConfigParser
import urllib2
import urlparse
import cPickle as pickle
import thread
import Queue

# Python 2 import patterns
from UserDict import UserDict
from UserList import UserList

def demonstrate_print_variations():
    """Test various print statement patterns"""
    print "=" * 50
    print "PRINT STATEMENT VARIATIONS"
    print "=" * 50
    
    # Basic print statements
    print "Simple message"
    print "Multiple", "arguments", "here"
    print "Number:", 42, "and string:", "hello"
    
    # Print with trailing comma (no newline)
    print "This line continues...",
    print "...on the same line"
    
    # Print to stderr
    print >> sys.stderr, "Error message to stderr"
    
    # Print to file-like object
    output = StringIO()
    print >> output, "Message to StringIO"
    print "StringIO content:", output.getvalue().strip()
    
    # Empty print
    print
    print "After empty line"

def test_string_operations():
    """Test Python 2 string operations"""
    print "STRING OPERATIONS"
    print "-" * 30
    
    # Unicode literals
    regular_str = "Regular ASCII string"
    unicode_str = u"Unicode string with café and naïve"
    raw_str = r"Raw string with \n and \t"
    
    print "Regular:", type(regular_str), repr(regular_str)
    print "Unicode:", type(unicode_str), repr(unicode_str)
    print "Raw:", type(raw_str), repr(raw_str)
    
    # String formatting
    old_format = "Hello %s, you have %d messages" % ("Alice", 5)
    print "Old format:", old_format
    
    # String methods that changed
    test_str = "Hello World"
    print "Has key-like usage:", test_str.find("World") != -1

def test_iteration_patterns():
    """Test Python 2 iteration patterns"""
    print "ITERATION PATTERNS"
    print "-" * 30
    
    # xrange vs range
    print "Using xrange:",
    for i in xrange(5):
        print i,
    print
    
    # Dictionary iteration methods
    test_dict = {"a": 1, "b": 2, "c": 3}
    
    print "Dict.keys():", test_dict.keys()
    print "Dict.values():", test_dict.values()
    print "Dict.items():", test_dict.items()
    
    print "Using iterkeys():",
    for key in test_dict.iterkeys():
        print key,
    print
    
    print "Using itervalues():",
    for value in test_dict.itervalues():
        print value,
    print
    
    print "Using iteritems():"
    for key, value in test_dict.iteritems():
        print "  %s: %s" % (key, value)

def test_exception_handling():
    """Test Python 2 exception patterns"""
    print "EXCEPTION HANDLING"
    print "-" * 30
    
    # Old exception syntax
    try:
        result = 10 / 0
    except ZeroDivisionError, e:
        print "Caught ZeroDivisionError:", e
    
    try:
        raise ValueError, "Custom error message"
    except ValueError, error:
        print "Caught ValueError:", error
    
    # Multiple exception types
    try:
        import non_existent_module
    except (ImportError, AttributeError), e:
        print "Import failed:", e
    
    # Exception with tuple
    try:
        raise TypeError, ("Type error", "with tuple")
    except TypeError, (msg, extra):
        print "TypeError with tuple:", msg, extra

def test_builtin_functions():
    """Test Python 2 builtin functions that changed"""
    print "BUILTIN FUNCTIONS"
    print "-" * 30
    
    # raw_input vs input
    print "Would use raw_input() for user input"
    # user_input = raw_input("Enter something: ")
    
    # apply function
    def multiply(a, b, c):
        return a * b * c
    
    result = apply(multiply, (2, 3, 4))
    print "apply() result:", result
    
    # execfile
    # execfile("some_script.py")  # Would execute file
    
    # cmp function
    print "cmp(5, 3):", cmp(5, 3)
    print "cmp(3, 5):", cmp(3, 5)
    print "cmp(5, 5):", cmp(5, 5)
    
    # filter, map, reduce returning lists
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    evens = filter(lambda x: x % 2 == 0, numbers)
    print "filter() result type:", type(evens)
    print "Even numbers:", evens
    
    squares = map(lambda x: x * x, numbers[:5])
    print "map() result type:", type(squares)
    print "Squares:", squares
    
    from operator import add
    total = reduce(add, numbers[:5])
    print "reduce() result:", total

def test_integer_division():
    """Test Python 2 integer division behavior"""
    print "INTEGER DIVISION"
    print "-" * 30
    
    print "5 / 2 =", 5 / 2  # Should be 2 in Python 2
    print "5.0 / 2 =", 5.0 / 2  # Should be 2.5
    print "5 // 2 =", 5 // 2  # Floor division
    print "-5 / 2 =", -5 / 2  # Should be -3 in Python 2
    print "-5.0 / 2 =", -5.0 / 2  # Should be -2.5

def test_type_checking():
    """Test Python 2 type checking patterns"""
    print "TYPE CHECKING"
    print "-" * 30
    
    import types
    
    test_string = "hello"
    test_unicode = u"hello"
    test_int = 42
    test_long = 42L
    
    # Old type checking
    if type(test_string) == types.StringType:
        print "Found StringType"
    
    if type(test_unicode) == types.UnicodeType:
        print "Found UnicodeType"
    
    if type(test_int) == types.IntType:
        print "Found IntType"
    
    if type(test_long) == types.LongType:
        print "Found LongType"
    
    # isinstance with old types
    print "isinstance checks:"
    print "  string:", isinstance(test_string, basestring)
    print "  unicode:", isinstance(test_unicode, basestring)

def main():
    """Main function with Python 2 patterns"""
    print "ADVANCED PYTHON 2 TEST PROJECT"
    print "=" * 60
    print "Testing comprehensive Python 2 to 3 conversion patterns"
    print "=" * 60
    print
    
    try:
        demonstrate_print_variations()
        print
        
        test_string_operations()
        print
        
        test_iteration_patterns()
        print
        
        test_exception_handling()
        print
        
        test_builtin_functions()
        print
        
        test_integer_division()
        print
        
        test_type_checking()
        print
        
        print "=" * 60
        print "ALL TESTS COMPLETED SUCCESSFULLY"
        print "This project exercises many Python 2 to 3 conversion scenarios"
        print "=" * 60
        
    except Exception, e:
        print >> sys.stderr, "Error occurred:", e
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)