# Python 2 to 3 Converter

[![Tests](https://github.com/your-username/cc-py2to3/workflows/Tests/badge.svg)](https://github.com/your-username/cc-py2to3/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive GUI application for converting Python 2 codebases to Python 3 with enhanced conversion capabilities, detailed error reporting, and VS Code integration.

## ✨ Features

- **🖥️ Easy-to-use GUI**: Modern tkinter interface for selecting directories and tracking progress
- **⚡ Two-Stage Conversion**: 
  - **Stage 1**: Core Python 2→3 conversion using standalone 2to3 tool
  - **Stage 2**: Enhanced conversion using fissix for `cmp` parameter handling
- **🔗 VS Code Integration**: HTML reports with clickable `vscode://` links to open files directly
- **📋 Detailed Logging**: Comprehensive error reporting with HTML and JSON reports
- **💾 Backup System**: Automatically creates backup files (.py2bak) before conversion
- **✅ Validation**: Post-conversion syntax and import validation
- **📊 Progress Tracking**: Real-time progress updates during conversion
- **🎯 Comprehensive Coverage**: Handles all major Python 2→3 migration patterns

## 🚀 Installation

1. **Clone this repository:**
```bash
git clone https://github.com/your-username/cc-py2to3.git
cd cc-py2to3
```

2. **Create virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 📖 Usage

### GUI Application

Run the main application:
```bash
python main.py
```

**Steps:**
1. Click "Browse" to select your Python 2 project directory
2. Configure options:
   - ✅ **Create backup files** (.py2bak) - *recommended*
   - ✅ **Use enhanced conversion (fissix)** - *for sort(cmp=...) patterns*
3. Click "Start Conversion" to begin the process
4. Monitor progress in the results panel
5. Click "View Logs" to open HTML reports with VS Code integration

### 🔧 Conversion Features

**Two-Stage Process:**
1. **2to3 Core Conversion** - Handles all standard Python 2→3 transformations
2. **Fissix Enhancement** - Converts `sort(cmp=func)` → `sort(key=cmp_to_key(func))`

**What Gets Converted:**
- Print statements → print() functions
- Exception syntax → modern `except Exception as e:`
- Import renames → Updated module names
- Dictionary methods → Python 3 compatible versions
- Range functions → `xrange()` → `range()`
- Sort comparisons → `cmp` parameter → `key` parameter with `cmp_to_key()`

## 🧪 Sample Projects

The repository includes two comprehensive Python 2 test projects to demonstrate and validate the converter:

### 📁 test-py2-project/
Basic Python 2 patterns for initial testing:
- Simple print statements and basic syntax
- Common import renames
- Basic exception handling
- String operations

### 📁 test-py2-advanced/
Comprehensive Python 2 patterns for thorough testing:
- **main.py**: Extensive Python 2 patterns including complex string operations, iteration, and type checking
- **utils/network.py**: Network operations using `urllib2`, `httplib`, and legacy HTTP patterns  
- **utils/data_processing.py**: Data processing with `cPickle`, `sets` module, and threading
- **config/settings.py**: Configuration management using `ConfigParser` and legacy import patterns
- **tests/test_legacy.py**: Unit tests with Python 2 unittest conventions
- **test_cmp_sorting.py**: Specific test cases for `cmp` parameter conversion (demonstrates fissix enhancement)

**To test the converter:**
1. Run the GUI: `python main.py`
2. Select either `test-py2-project` or `test-py2-advanced` directory
3. Enable both backup and fissix enhancement options
4. Convert and examine the results in the generated HTML reports

**Error Handling:**
- Captures and reports syntax errors
- Logs import resolution issues
- Provides line-by-line error details
- Generates both text and HTML reports

**Backup & Restore:**
- Creates `.py2bak` files alongside originals
- One-click restore functionality
- Preserves file permissions and timestamps

**Validation:**
- Post-conversion syntax checking
- Import dependency validation
- Summary statistics and error counts

## Project Structure

```
cc-py2to3/
├── src/
│   ├── converter/          # Core conversion engine
│   │   ├── __init__.py
│   │   └── engine.py      # Python2to3Converter class
│   ├── gui/               # GUI components
│   │   ├── __init__.py
│   │   └── main_window.py # Main application window
│   ├── reporter/          # Logging and reporting
│   │   ├── __init__.py
│   │   └── logger.py      # ConversionReporter class
│   └── tester/            # Validation and test generation
│       ├── __init__.py
│       └── validator.py   # Validation and TestGenerator classes
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── test_converter.py
│   └── test_validator.py
├── logs/                  # Generated logs (created at runtime)
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Dependencies

- **fissix**: Enhanced Python 2to3 conversion tool
- **pytest**: Testing framework
- **tkinter**: GUI framework (included with Python)

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Or run individual test files:
```bash
python -m pytest tests/test_converter.py
python -m pytest tests/test_validator.py
```

## Common Python 2 → 3 Conversions

This tool handles many common Python 2 to 3 migration patterns:

- `print` statements → `print()` function calls
- `unicode` strings → regular strings
- Import renames (`ConfigParser` → `configparser`, etc.)
- `xrange()` → `range()`
- Division operator behavior
- Dictionary iteration methods
- Exception syntax updates
- And many more...

## Output Files

After conversion, you'll find:

**Log Files (in `logs/` directory):**
**Log Files (in `logs/` directory):**
- `conversion_YYYYMMDD_HHMMSS.log` - Detailed text log
- `report_YYYYMMDD_HHMMSS.json` - Machine-readable report
- `report_YYYYMMDD_HHMMSS.html` - Human-readable HTML report with VS Code links

**Backup Files:**
- `*.py2bak` - Original Python 2 files (if backup enabled)

## 🔧 Requirements

- Python 3.8 or higher
- tkinter (included with most Python installations)
- 2to3 tool (included with Python)
- Dependencies listed in `requirements.txt`

## 🐛 Troubleshooting

**Import Errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that Python 3 is being used: `python --version`

**Conversion Issues:**
- Check the detailed logs for specific error messages
- Some complex Python 2 code may require manual intervention
- Use the backup restore feature if needed
- Try disabling fissix enhancement if issues persist

**GUI Problems:**
- Ensure tkinter is available: `python -c "import tkinter"`
- On some Linux systems: `sudo apt-get install python3-tk`

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Add tests for new functionality
4. Ensure all tests pass (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[fissix](https://github.com/amyreese/fissix)** by John Reese - Enhanced Python 2to3 conversion tool
- **Python's built-in 2to3 tool** - Foundation for Python 2→3 conversion
- **tkinter** - GUI framework included with Python
- All contributors and users who help improve this tool

## 📊 Project Stats

- **15+ Python 2 test files** with comprehensive patterns
- **4 main modules** with clean separation of concerns  
- **2 sample projects** ready for conversion testing
- **Cross-platform** support (Windows, macOS, Linux)
- **VS Code integration** for seamless development workflow