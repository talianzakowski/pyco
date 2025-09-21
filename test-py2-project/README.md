# Python 2 Legacy Test Project

This is a sample Python 2 project created for testing Python 2 to 3 conversion tools.

## Python 2 Features Included

This project contains various Python 2 patterns that need conversion:

### 1. Print Statements
- `print "text"` → `print("text")`
- `print "item1", "item2"` → `print("item1", "item2")`

### 2. Import Changes
- `import ConfigParser` → `import configparser`
- `from StringIO import StringIO` → `from io import StringIO`
- `import urllib2` → `import urllib.request`
- `from urlparse import *` → `from urllib.parse import *`

### 3. String Handling
- `unicode()` strings → regular strings
- `str.has_key()` → `key in dict`
- Old string formatting patterns

### 4. Exception Handling
- `except Exception, e:` → `except Exception as e:`

### 5. Iterator Changes
- `dict.iteritems()` → `dict.items()`
- `dict.iterkeys()` → `dict.keys()`
- `dict.itervalues()` → `dict.values()`

### 6. Range Functions
- `xrange()` → `range()`

### 7. Built-in Function Changes
- `raw_input()` → `input()`
- `cmp()` function removal
- `file()` → `open()`

### 8. Division Behavior
- Integer division changes: `5/2` behavior

### 9. Type Checking
- `types.StringType` → `str`
- `types.UnicodeType` → `str`

### 10. Functional Programming
- `filter()`, `map()` return iterators in Python 3
- `reduce()` moved to `functools.reduce()`

## Project Structure

```
test-py2-project/
├── main.py                 # Main application demonstrating Python 2 patterns
├── scripts/
│   └── data_processor.py   # Data processing with legacy imports
├── utils/
│   └── string_helper.py    # String utilities with old patterns
├── config/
│   └── settings.py         # Configuration with renamed imports
├── tests/
│   └── test_legacy.py      # Test cases using Python 2 patterns
└── README.md               # This file
```

## Usage

### Running in Python 2 (Original)
```bash
python2 main.py
```

### Testing the Converter
Use this project as input for the Python 2 to 3 converter tool.

### Expected Conversion Changes
After conversion, the code should:
- Use print functions instead of statements
- Have updated import statements
- Use Python 3 compatible string handling
- Use modern exception syntax
- Replace deprecated functions and methods

## Notes

This project is specifically designed to test conversion tools and contains intentional Python 2 patterns that would cause syntax errors or deprecated warnings in Python 3.