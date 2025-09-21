import unittest
import tempfile
import os
import shutil
from pathlib import Path

# Add src to path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from tester.validator import (
    ConvertedCodeValidator,
    ValidationResult,
    ConversionTestGenerator,
)


class TestConvertedCodeValidator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.validator = ConvertedCodeValidator()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def create_test_file(self, filename, content):
        """Create a test Python file."""
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
        return file_path

    def test_valid_python3_syntax(self):
        """Test validation of valid Python 3 syntax."""
        valid_content = """
def hello_world():
    print("Hello, World!")
    return True

if __name__ == "__main__":
    hello_world()
"""
        file_path = self.create_test_file("valid.py", valid_content)

        is_valid, error = self.validator.validate_syntax(file_path)

        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_invalid_python_syntax(self):
        """Test validation of invalid Python syntax."""
        invalid_content = """
def broken_function(
    print("This is broken"
"""
        file_path = self.create_test_file("invalid.py", invalid_content)

        is_valid, error = self.validator.validate_syntax(file_path)

        self.assertFalse(is_valid)
        self.assertIn("Syntax error", error)

    def test_valid_imports(self):
        """Test validation of valid imports."""
        valid_content = """
import os
import sys
from pathlib import Path
import json
"""
        file_path = self.create_test_file("valid_imports.py", valid_content)

        is_valid, errors = self.validator.validate_imports(file_path)

        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_invalid_imports(self):
        """Test validation of invalid imports."""
        invalid_content = """
import nonexistent_module_xyz
from another_fake_module import something
import os  # This should be valid
"""
        file_path = self.create_test_file("invalid_imports.py", invalid_content)

        is_valid, errors = self.validator.validate_imports(file_path)

        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        # Should report the nonexistent modules
        error_text = " ".join(errors)
        self.assertIn("nonexistent_module_xyz", error_text)

    def test_validate_file_complete(self):
        """Test complete file validation."""
        content = """
import os
def test_function():
    print("Test")
    return os.path.exists(".")
"""
        file_path = self.create_test_file("complete_test.py", content)

        result = self.validator.validate_file(file_path)

        self.assertIsInstance(result, ValidationResult)
        self.assertEqual(result.file_path, file_path)
        self.assertTrue(result.syntax_valid)
        self.assertTrue(result.imports_valid)
        self.assertTrue(result.overall_valid)

    def test_validate_directory(self):
        """Test validating entire directory."""
        # Create multiple test files
        self.create_test_file("valid1.py", "import os\nprint('valid')")
        self.create_test_file("valid2.py", "import sys\ndef func(): pass")
        self.create_test_file("invalid.py", "def broken(\nprint('broken')")

        results = self.validator.validate_directory(self.temp_dir)

        self.assertEqual(len(results), 3)
        valid_results = [r for r in results if r.overall_valid]
        invalid_results = [r for r in results if not r.overall_valid]

        self.assertEqual(len(valid_results), 2)
        self.assertEqual(len(invalid_results), 1)

    def test_validation_summary(self):
        """Test validation summary statistics."""
        # Create test files
        self.create_test_file("valid.py", "print('valid')")
        self.create_test_file("invalid.py", "def broken(\npass")

        self.validator.validate_directory(self.temp_dir)
        summary = self.validator.get_summary()

        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["valid"], 1)
        self.assertEqual(summary["invalid"], 1)
        self.assertEqual(summary["syntax_errors"], 1)


class TestTestGenerator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_dir = os.path.join(self.temp_dir, "tests")
        self.generator = ConversionTestGenerator()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def create_test_file(self, filename, content):
        """Create a test Python file."""
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
        return file_path

    def test_generate_test_for_simple_module(self):
        """Test generating test for a simple module."""
        module_content = """
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

class Calculator:
    def __init__(self):
        self.result = 0

    def calculate(self, operation):
        pass
"""
        file_path = self.create_test_file("calculator.py", module_content)

        test_file = self.generator.generate_test_for_file(file_path, self.test_dir)

        self.assertIsNotNone(test_file)
        self.assertTrue(os.path.exists(test_file))

        # Read generated test content
        with open(test_file, "r") as f:
            test_content = f.read()

        # Check that test includes expected elements
        self.assertIn("import calculator", test_content)
        self.assertIn("TestCalculator", test_content)
        self.assertIn("test_add_exists", test_content)
        self.assertIn("test_multiply_exists", test_content)
        self.assertIn("test_calculator_class_exists", test_content)

    def test_generate_tests_for_directory(self):
        """Test generating tests for entire directory."""
        # Create multiple modules
        self.create_test_file("module1.py", "def func1(): pass")
        self.create_test_file("module2.py", "class Class2: pass")

        test_files = self.generator.generate_tests_for_directory(
            self.temp_dir, self.test_dir
        )

        self.assertEqual(len(test_files), 2)
        self.assertTrue(all(os.path.exists(f) for f in test_files))

        # Check test files were created in test directory
        test_dir_files = os.listdir(self.test_dir)
        self.assertIn("test_module1.py", test_dir_files)
        self.assertIn("test_module2.py", test_dir_files)

    def test_generate_test_for_module_with_no_functions(self):
        """Test generating test for module with only variables."""
        module_content = """
# Configuration module
DEBUG = True
DATABASE_URL = "sqlite:///test.db"
"""
        file_path = self.create_test_file("config.py", module_content)

        test_file = self.generator.generate_test_for_file(file_path, self.test_dir)

        self.assertIsNotNone(test_file)
        self.assertTrue(os.path.exists(test_file))

        # Should still generate basic import test
        with open(test_file, "r") as f:
            test_content = f.read()

        self.assertIn("import config", test_content)
        self.assertIn("test_module_imports", test_content)


if __name__ == "__main__":
    unittest.main()
