# Repository Structure

This document provides an overview of the Python 2 to 3 Converter repository structure.

## 📁 Root Directory

```
cc-py2to3/
├── .github/
│   └── workflows/
│       └── test.yml                 # GitHub Actions CI/CD
├── src/
│   ├── converter/
│   │   ├── __init__.py
│   │   └── engine.py               # Core conversion logic (2to3 + fissix)
│   ├── gui/
│   │   ├── __init__.py
│   │   └── main_window.py          # GUI application with fissix option
│   ├── reporter/
│   │   ├── __init__.py
│   │   └── logger.py               # HTML/JSON reporting with VS Code links
│   └── tester/
│       ├── __init__.py
│       └── validator.py            # Post-conversion validation
├── tests/
│   ├── __init__.py
│   ├── test_converter.py           # Unit tests for converter
│   └── test_validator.py           # Unit tests for validator
├── test-py2-project/               # Basic Python 2 sample project
│   ├── main.py
│   ├── README.md
│   ├── config/
│   │   └── settings.py
│   ├── scripts/
│   │   └── data_processor.py
│   ├── tests/
│   │   └── test_legacy.py
│   └── utils/
│       └── string_helper.py
├── test-py2-advanced/              # Comprehensive Python 2 sample project
│   ├── main.py                     # Extensive Python 2 patterns
│   ├── README.md
│   ├── test_cmp_sorting.py         # Specific fissix test cases
│   ├── config/
│   │   └── settings.py             # ConfigParser patterns
│   ├── tests/
│   │   └── test_legacy.py          # Python 2 unittest patterns
│   └── utils/
│       ├── network.py              # urllib2, httplib patterns
│       └── data_processing.py      # cPickle, sets module patterns
├── logs/                           # Generated at runtime
│   ├── conversion_*.log            # Text logs
│   ├── report_*.json              # JSON reports
│   └── report_*.html              # HTML reports with VS Code links
├── main.py                         # Application entry point
├── requirements.txt                # Python dependencies
├── setup.py                       # Package installation script
├── .gitignore                     # Git ignore rules
├── LICENSE                        # MIT license
├── README.md                      # Main documentation
├── CHANGELOG.md                   # Version history
└── REPOSITORY_STRUCTURE.md       # This file
```

## 🔧 Key Components

### Core Conversion Engine (`src/converter/engine.py`)
- **Python2to3Converter**: Main conversion class
- **Two-stage process**: 2to3 + fissix enhancement
- **ConversionResult**: Result tracking and validation
- **Error handling**: Graceful fallback and detailed reporting

### GUI Application (`src/gui/main_window.py`)
- **MainWindow**: Tkinter-based interface
- **Progress tracking**: Real-time conversion updates
- **Option controls**: Backup and fissix enhancement toggles
- **Results display**: Integrated log viewing

### Reporting System (`src/reporter/logger.py`)
- **ConversionReporter**: Multi-format logging
- **VS Code integration**: Clickable file links in HTML reports
- **Error parsing**: Line number extraction and formatting
- **Progress tracking**: Conversion statistics and summaries

### Sample Projects
- **test-py2-project/**: 5 Python files with basic Python 2 patterns
- **test-py2-advanced/**: 6 Python files with comprehensive Python 2 patterns
- **Ready-to-convert**: Authentic Python 2 syntax for testing

## 🧪 Testing Infrastructure

### Unit Tests (`tests/`)
- **test_converter.py**: Core conversion logic tests
- **test_validator.py**: Post-conversion validation tests
- **GitHub Actions**: Automated testing across Python versions and platforms

### Sample Validation
- **Comprehensive patterns**: Print statements, imports, exceptions, sorting
- **fissix demonstration**: `cmp` parameter conversion test cases
- **Error simulation**: Invalid syntax and edge cases

## 📦 Distribution

### Package Files
- **setup.py**: PyPI distribution configuration
- **requirements.txt**: Runtime dependencies
- **LICENSE**: MIT license for open source distribution
- **.gitignore**: Git exclusion rules for clean repository

### Documentation
- **README.md**: Complete user guide with badges and examples
- **CHANGELOG.md**: Version history and feature additions
- **Repository structure**: This file for developers

## 🚀 Usage Patterns

### Development Setup
1. Clone repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `pytest tests/`
5. Launch GUI: `python main.py`

### Conversion Workflow
1. Select Python 2 project directory
2. Configure backup and fissix options
3. Start conversion process
4. Review HTML reports with VS Code integration
5. Validate converted Python 3 code

This structure provides a complete, professional Python 2 to 3 conversion solution with comprehensive testing, documentation, and distribution support.