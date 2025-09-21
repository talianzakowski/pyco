#!/usr/bin/env python2
"""
README file for comprehensive Python 2 test project
"""

# Python 2 Test Project

This is a comprehensive test project designed to exercise Python 2 to 3 conversion tools.
It contains various Python 2 patterns and constructs that need to be converted for Python 3 compatibility.

## Python 2 Patterns Included

### Print Statements
- Basic print statements without parentheses
- Print statements with multiple arguments
- Print statements with file output redirection
- Print statements with formatting

### Exception Handling
- Old-style exception syntax: `except Exception, e:`
- Bare except clauses
- Exception raising without parentheses

### Import Statements
- Renamed modules: `cPickle`, `cStringIO`, `ConfigParser`
- Removed modules: `sets`, `md5`, `sha`
- urllib2 and httplib usage
- Old-style relative imports

### String Operations
- String formatting with % operator
- Unicode string handling
- has_key() method usage on dictionaries

### Data Types and Operations
- xrange() instead of range()
- dict.iteritems(), dict.iterkeys(), dict.itervalues()
- sets.Set() usage
- Long integer literals with 'L' suffix

### Standard Library Changes
- Threading module differences
- Queue vs queue module
- ConfigParser vs configparser
- pickle vs cPickle

## Files Structure

```
test-py2-advanced/
├── main.py                 # Main application with diverse Python 2 patterns
├── utils/
│   ├── network.py         # Network operations using urllib2, httplib
│   └── data_processing.py # Data processing with cPickle, sets module
├── config/
│   └── settings.py        # Configuration using ConfigParser
└── tests/
    └── test_legacy.py     # Unit tests with Python 2 patterns
```

## Expected Conversions

When converted to Python 3, these patterns should be transformed:

1. **Print statements** → Print functions
   ```python
   # Python 2
   print "Hello World"
   print >> sys.stderr, "Error message"
   
   # Python 3
   print("Hello World")
   print("Error message", file=sys.stderr)
   ```

2. **Exception handling** → New syntax
   ```python
   # Python 2
   except Exception, e:
   
   # Python 3
   except Exception as e:
   ```

3. **Imports** → Updated module names
   ```python
   # Python 2
   import cPickle
   import ConfigParser
   import urllib2
   
   # Python 3
   import pickle
   import configparser
   import urllib.request
   ```

4. **Dictionary methods** → Iterator methods removed
   ```python
   # Python 2
   for key, value in dict.iteritems():
   
   # Python 3
   for key, value in dict.items():
   ```

5. **Range function** → xrange removed
   ```python
   # Python 2
   for i in xrange(10):
   
   # Python 3
   for i in range(10):
   ```

## Testing the Converter

To test the Python 2 to 3 converter on this project:

1. Ensure the converter tool is working
2. Point it to this `test-py2-advanced` directory
3. Run the conversion process
4. Check that all Python 2 patterns are properly converted
5. Verify the converted code is syntactically correct Python 3

## Expected Results

After conversion, all files should:
- Use Python 3 print function syntax
- Use modern exception handling syntax
- Import correct Python 3 module names
- Use Python 3 compatible string and data operations
- Pass Python 3 syntax validation

This test project provides comprehensive coverage of Python 2 to 3 conversion scenarios.