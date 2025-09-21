"""
Preprocessor for Python 2 syntax to make files parseable by Python 3 tools like fissix.

This module handles basic Python 2 syntax that prevents parsing by Python 3 parsers:
- Print statements -> print() function calls
- Exception handling syntax
- Other minimal syntax fixes

This is NOT a complete Python 2to3 converter, just a minimal preprocessor to enable
parsing by modern tools like fissix.
"""

import re
import ast
from typing import List, Tuple


class Python2SyntaxPreprocessor:
    """Preprocesses Python 2 files to make them parseable by Python 3 tools."""

    def __init__(self):
        # Regex patterns for Python 2 syntax that prevents parsing

        # Match print statements (not print function calls)
        # This is a simplified pattern - doesn't handle all edge cases but covers most common ones
        self.print_statement_pattern = re.compile(
            r"^(\s*)print\s+([^(].*?)$", re.MULTILINE
        )

        # Match except clauses with comma syntax: except Exception, e:
        self.except_clause_pattern = re.compile(
            r"^(\s*)except\s+([^,]+),\s*([^:]+):(.*)$", re.MULTILINE
        )

    def preprocess_print_statements(self, content: str) -> str:
        """Convert print statements to print() function calls."""

        def replace_print_statement(match):
            indent = match.group(1)
            args = match.group(2).strip()

            # Handle special cases
            if not args:
                # Just 'print' with no arguments
                return f"{indent}print()"

            # Handle multiple arguments separated by commas
            # This is a basic implementation - might need refinement for complex cases
            if args.endswith(","):
                # Print statement ending with comma (no newline)
                args = args[:-1].strip()
                if args:
                    return f"{indent}print({args}, end=' ')"
                else:
                    return f"{indent}print(end=' ')"
            else:
                # Regular print statement
                return f"{indent}print({args})"

        return self.print_statement_pattern.sub(replace_print_statement, content)

    def preprocess_except_clauses(self, content: str) -> str:
        """Convert old except syntax to new syntax."""

        def replace_except_clause(match):
            indent = match.group(1)
            exception_type = match.group(2).strip()
            variable = match.group(3).strip()
            rest = match.group(4)

            return f"{indent}except {exception_type} as {variable}:{rest}"

        return self.except_clause_pattern.sub(replace_except_clause, content)

    def preprocess(self, content: str) -> str:
        """Apply all preprocessing steps to make Python 2 code parseable by Python 3."""

        # Apply transformations in order
        content = self.preprocess_print_statements(content)
        content = self.preprocess_except_clauses(content)

        return content

    def preprocess_file(self, file_path: str) -> str:
        """Preprocess a file and return the modified content."""
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        preprocessed_content = self.preprocess(original_content)
        return preprocessed_content

    def can_parse_as_python3(self, content: str) -> bool:
        """Check if content can be parsed as valid Python 3 syntax."""
        try:
            ast.parse(content)
            return True
        except SyntaxError:
            return False


def test_preprocessor():
    """Test the preprocessor with some sample Python 2 code."""

    sample_py2_code = """
def test_function():
    print "Hello, World!"
    print "Multiple", "arguments"
    print
    
    try:
        x = 1 / 0
    except ZeroDivisionError, e:
        print "Error:", e
    
    print "Done",
"""

    preprocessor = Python2SyntaxPreprocessor()

    print("Original Python 2 code:")
    print(sample_py2_code)
    print("\n" + "=" * 50)

    preprocessed = preprocessor.preprocess(sample_py2_code)
    print("Preprocessed code:")
    print(preprocessed)
    print("\n" + "=" * 50)

    print(f"Can parse as Python 3: {preprocessor.can_parse_as_python3(preprocessed)}")


if __name__ == "__main__":
    test_preprocessor()
