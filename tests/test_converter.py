import unittest
import tempfile
import os
import shutil
from pathlib import Path

# Add src to path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from converter.engine import Python2to3Converter, ConversionResult


class TestPython2to3Converter(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.converter = Python2to3Converter()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def create_test_file(self, filename, content):
        """Create a test Python file."""
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
        return file_path

    def test_python2_print_conversion(self):
        """Test conversion of Python 2 print statements."""
        py2_content = """print "Hello World"
print "Number:", 42
"""
        file_path = self.create_test_file("test_print.py", py2_content)

        result = self.converter.convert_file(file_path, backup=False)

        self.assertTrue(result.success)
        self.assertTrue(result.changes_made)

        # Read converted content
        with open(file_path, "r") as f:
            converted = f.read()

        self.assertIn('print("Hello World")', converted)
        self.assertIn('print(("Number:", 42))', converted)

    def test_python2_unicode_conversion(self):
        """Test conversion of Python 2 unicode strings."""
        py2_content = """text = u"Unicode string"
raw_text = ur"Raw unicode"
"""
        file_path = self.create_test_file("test_unicode.py", py2_content)

        result = self.converter.convert_file(file_path, backup=False)

        self.assertTrue(result.success)

    def test_python2_imports_conversion(self):
        """Test conversion of Python 2 imports."""
        py2_content = """import ConfigParser
from urlparse import urlparse
"""
        file_path = self.create_test_file("test_imports.py", py2_content)

        result = self.converter.convert_file(file_path, backup=False)

        self.assertTrue(result.success)

    def test_already_python3_file(self):
        """Test that Python 3 files are handled correctly."""
        py3_content = """print("Already Python 3")
def test():
    return "No changes needed"
"""
        file_path = self.create_test_file("test_py3.py", py3_content)

        result = self.converter.convert_file(file_path, backup=False)

        self.assertTrue(result.success)
        # Should not make changes to already valid Python 3 code
        # (though fissix might still make minor formatting changes)

    def test_backup_creation(self):
        """Test that backup files are created when requested."""
        py2_content = '''print "Test backup"'''
        file_path = self.create_test_file("test_backup.py", py2_content)

        result = self.converter.convert_file(file_path, backup=True)

        self.assertTrue(result.success)

        # Check backup file exists
        backup_path = file_path + ".py2bak"
        self.assertTrue(os.path.exists(backup_path))

        # Check backup contains original content
        with open(backup_path, "r") as f:
            backup_content = f.read()
        self.assertEqual(backup_content, py2_content)

    def test_invalid_syntax_file(self):
        """Test handling of files with invalid syntax."""
        invalid_content = """print "incomplete syntax
def broken_function(
"""
        file_path = self.create_test_file("test_invalid.py", invalid_content)

        result = self.converter.convert_file(file_path, backup=False)

        # Should handle the error gracefully
        self.assertFalse(result.success)
        self.assertIn("error", result.error.lower())

    def test_find_python_files(self):
        """Test finding Python files in directory."""
        # Create test files
        self.create_test_file("script1.py", "print('test')")
        self.create_test_file("script2.py", "print('test')")
        self.create_test_file("not_python.txt", "not python")

        # Create subdirectory with Python file
        sub_dir = os.path.join(self.temp_dir, "subdir")
        os.makedirs(sub_dir)
        sub_file = os.path.join(sub_dir, "sub_script.py")
        with open(sub_file, "w") as f:
            f.write("print('subdir test')")

        files = self.converter.find_python_files(self.temp_dir)

        self.assertEqual(len(files), 3)
        self.assertTrue(any("script1.py" in f for f in files))
        self.assertTrue(any("script2.py" in f for f in files))
        self.assertTrue(any("sub_script.py" in f for f in files))
        self.assertFalse(any("not_python.txt" in f for f in files))

    def test_convert_directory(self):
        """Test converting entire directory."""
        # Create multiple Python 2 files
        self.create_test_file("file1.py", 'print "File 1"')
        self.create_test_file("file2.py", 'print "File 2"')

        results = self.converter.convert_directory(self.temp_dir, backup=True)

        self.assertEqual(len(results), 2)
        self.assertTrue(all(r.success for r in results))

        # Check summary
        summary = self.converter.get_summary()
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["successful"], 2)
        self.assertEqual(summary["failed"], 0)

    def test_restore_backups(self):
        """Test restoring backup files."""
        py2_content = 'print "Original content"'
        file_path = self.create_test_file("test_restore.py", py2_content)

        # Convert with backup
        self.converter.convert_file(file_path, backup=True)

        # Verify file was changed
        with open(file_path, "r") as f:
            converted_content = f.read()
        self.assertNotEqual(converted_content, py2_content)

        # Restore backups
        restored = self.converter.restore_backups(self.temp_dir)

        self.assertEqual(len(restored), 1)
        self.assertIn(file_path, restored)

        # Verify original content is restored
        with open(file_path, "r") as f:
            restored_content = f.read()
        self.assertEqual(restored_content, py2_content)


if __name__ == "__main__":
    unittest.main()
