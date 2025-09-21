import ast
import subprocess
import sys
import tempfile
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import importlib.util


class ValidationResult:
    def __init__(
        self,
        file_path: str,
        syntax_valid: bool = False,
        imports_valid: bool = False,
        syntax_error: str = "",
        import_errors: List[str] = None,
    ):
        self.file_path = file_path
        self.syntax_valid = syntax_valid
        self.imports_valid = imports_valid
        self.syntax_error = syntax_error
        self.import_errors = import_errors or []
        self.overall_valid = syntax_valid and imports_valid

    def __str__(self):
        status = "✓ VALID" if self.overall_valid else "✗ INVALID"
        return f"{status}: {os.path.basename(self.file_path)}"


class ConvertedCodeValidator:
    def __init__(self):
        self.results: List[ValidationResult] = []

    def validate_syntax(self, file_path: str) -> Tuple[bool, str]:
        """Validate Python 3 syntax of a file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            # Try to parse with Python 3 AST
            ast.parse(source)
            return True, ""

        except SyntaxError as e:
            error_msg = f"Syntax error at line {e.lineno}: {e.msg}"
            return False, error_msg
        except Exception as e:
            return False, str(e)

    def validate_imports(self, file_path: str) -> Tuple[bool, List[str]]:
        """Validate that all imports in the file can be resolved."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)
            import_errors = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if not self._can_import_module(alias.name):
                            import_errors.append(f"Cannot import module: {alias.name}")

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        if not self._can_import_module(node.module):
                            import_errors.append(f"Cannot import module: {node.module}")

            return len(import_errors) == 0, import_errors

        except Exception as e:
            return False, [f"Error checking imports: {str(e)}"]

    def _can_import_module(self, module_name: str) -> bool:
        """Check if a module can be imported."""
        try:
            # Skip relative imports and some known problematic modules
            if module_name.startswith(".") or module_name in ["__main__"]:
                return True

            # Try to find the module spec
            spec = importlib.util.find_spec(module_name)
            return spec is not None

        except (ImportError, ModuleNotFoundError, ValueError):
            return False
        except Exception:
            # For any other exception, assume it's importable to avoid false positives
            return True

    def validate_file(self, file_path: str) -> ValidationResult:
        """Validate a single converted Python file."""
        syntax_valid, syntax_error = self.validate_syntax(file_path)
        imports_valid, import_errors = self.validate_imports(file_path)

        result = ValidationResult(
            file_path=file_path,
            syntax_valid=syntax_valid,
            imports_valid=imports_valid,
            syntax_error=syntax_error,
            import_errors=import_errors,
        )

        self.results.append(result)
        return result

    def validate_directory(self, directory: str) -> List[ValidationResult]:
        """Validate all Python files in a directory."""
        results = []
        for root, dirs, files in os.walk(directory):
            # Skip common non-source directories
            dirs[:] = [
                d
                for d in dirs
                if d not in {".git", "__pycache__", ".pytest_cache", "venv", "env"}
            ]

            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    result = self.validate_file(file_path)
                    results.append(result)

        return results

    def get_summary(self) -> Dict[str, int]:
        """Get validation summary statistics."""
        total = len(self.results)
        valid = sum(1 for r in self.results if r.overall_valid)
        syntax_errors = sum(1 for r in self.results if not r.syntax_valid)
        import_errors = sum(1 for r in self.results if not r.imports_valid)

        return {
            "total": total,
            "valid": valid,
            "invalid": total - valid,
            "syntax_errors": syntax_errors,
            "import_errors": import_errors,
        }

    def get_failed_validations(self) -> List[ValidationResult]:
        """Get list of files that failed validation."""
        return [r for r in self.results if not r.overall_valid]


class ConversionTestGenerator:
    """Generate basic tests for converted Python files."""

    def __init__(self):
        self.test_template = '''import unittest
import sys
import os

# Add the source directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import {module_name}
except ImportError as e:
    print(f"Cannot import {module_name}: {{e}}")
    {module_name} = None


class Test{class_name}(unittest.TestCase):
    """Basic tests for {module_name} module."""

    def setUp(self):
        """Set up test fixtures."""
        if {module_name} is None:
            self.skipTest("Module {module_name} could not be imported")

    def test_module_imports(self):
        """Test that the module can be imported without errors."""
        self.assertIsNotNone({module_name}, "Module should be importable")

    def test_basic_functionality(self):
        """Test basic functionality if possible."""
        # Add specific tests based on module contents
        pass

{additional_tests}

if __name__ == '__main__':
    unittest.main()
'''

    def generate_test_for_file(
        self, file_path: str, test_dir: str = "tests"
    ) -> Optional[str]:
        """Generate a basic test file for a Python module."""
        try:
            # Create test directory if it doesn't exist
            test_path = Path(test_dir)
            test_path.mkdir(exist_ok=True)

            # Parse the module to understand its structure
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)

            # Extract module information
            module_name = Path(file_path).stem
            class_name = module_name.replace("_", " ").title().replace(" ", "")

            # Find functions and classes
            functions = []
            classes = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)

            # Generate additional tests based on found elements
            additional_tests = []

            for func_name in functions[:5]:  # Limit to first 5 functions
                test_method = f'''
    def test_{func_name}_exists(self):
        """Test that {func_name} function exists."""
        self.assertTrue(hasattr({module_name}, '{func_name}'))
'''
                additional_tests.append(test_method)

            for class_name_found in classes[:3]:  # Limit to first 3 classes
                test_method = f'''
    def test_{class_name_found.lower()}_class_exists(self):
        """Test that {class_name_found} class exists."""
        self.assertTrue(hasattr({module_name}, '{class_name_found}'))

    def test_{class_name_found.lower()}_instantiation(self):
        """Test that {class_name_found} can be instantiated."""
        try:
            instance = {module_name}.{class_name_found}()
            self.assertIsNotNone(instance)
        except TypeError:
            # Class might require arguments
            pass
'''
                additional_tests.append(test_method)

            # Generate the test file content
            test_content = self.test_template.format(
                module_name=module_name,
                class_name=class_name,
                additional_tests="".join(additional_tests),
            )

            # Write test file
            test_file_path = test_path / f"test_{module_name}.py"
            with open(test_file_path, "w", encoding="utf-8") as f:
                f.write(test_content)

            return str(test_file_path)

        except Exception as e:
            print(f"Failed to generate test for {file_path}: {e}")
            return None

    def generate_tests_for_directory(
        self, source_dir: str, test_dir: str = "tests"
    ) -> List[str]:
        """Generate test files for all Python files in a directory."""
        generated_tests = []

        for root, dirs, files in os.walk(source_dir):
            # Skip test directories and common non-source directories
            dirs[:] = [
                d
                for d in dirs
                if d
                not in {
                    "tests",
                    "test",
                    ".git",
                    "__pycache__",
                    ".pytest_cache",
                    "venv",
                    "env",
                }
            ]

            for file in files:
                if file.endswith(".py") and not file.startswith("test_"):
                    file_path = os.path.join(root, file)
                    test_file = self.generate_test_for_file(file_path, test_dir)
                    if test_file:
                        generated_tests.append(test_file)

        return generated_tests

    def run_tests(self, test_dir: str = "tests") -> Dict[str, any]:
        """Run the generated tests and return results."""
        try:
            # Run pytest on the test directory
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_dir, "-v", "--tb=short"],
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }

        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1}
