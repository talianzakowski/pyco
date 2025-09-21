import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Callable
import tempfile
import traceback


class ConversionResult:
    def __init__(
        self,
        file_path: str,
        success: bool,
        output: str = "",
        error: str = "",
        original_content: str = "",
    ):
        self.file_path = file_path
        self.success = success
        self.output = output
        self.error = error
        self.changes_made = bool(output and output.strip() != original_content.strip())


class Python2to3Converter:
    def __init__(
        self,
        progress_callback: Optional[Callable[[str, float], None]] = None,
        use_fissix_second_stage: bool = True,
    ):
        self.progress_callback = progress_callback
        self.conversion_results: List[ConversionResult] = []
        self.use_fissix_second_stage = use_fissix_second_stage

    def find_python_files(self, directory: str) -> List[str]:
        """Find all Python files in directory recursively."""
        python_files = []
        for root, dirs, files in os.walk(directory):
            # Skip common non-source directories
            dirs[:] = [
                d
                for d in dirs
                if d not in {".git", "__pycache__", ".pytest_cache", "venv", "env"}
            ]

            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))

        return python_files

    def convert_file(self, file_path: str, backup: bool = True) -> ConversionResult:
        """Convert a single Python file from Python 2 to 3."""
        try:
            # Read original content for change detection
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            # Create backup if requested
            if backup:
                backup_path = f"{file_path}.py2bak"
                shutil.copy2(file_path, backup_path)

            # Stage 1: Use 2to3 for core conversion
            result_2to3 = self._convert_with_2to3(file_path, original_content)
            if not result_2to3.success:
                return result_2to3

            # Stage 2: Use fissix for enhanced conversion (cmp parameter fix)
            if self.use_fissix_second_stage:
                result_fissix = self._convert_with_fissix(file_path, original_content)
                if result_fissix.success:
                    # Fissix successful, return its result
                    return result_fissix
                else:
                    # Fissix failed, but 2to3 worked, so return 2to3 result with warning
                    warning_msg = f"2to3 succeeded but fissix enhancement failed: {result_fissix.error}"
                    return ConversionResult(
                        file_path,
                        True,
                        result_2to3.output,
                        warning_msg,
                        original_content,
                    )

            return result_2to3

        except Exception as e:
            # Try to read original content for the error case
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    original_content = f.read()
            except Exception:
                original_content = ""

            error_msg = (
                f"Error converting {file_path}: {str(e)}\n{traceback.format_exc()}"
            )
            return ConversionResult(file_path, False, "", error_msg, original_content)

    def _convert_with_2to3(
        self, file_path: str, original_content: str = ""
    ) -> ConversionResult:
        """Convert file using standalone 2to3 tool."""
        try:
            # Read original content if not provided
            if not original_content:
                with open(file_path, "r", encoding="utf-8") as f:
                    original_content = f.read()

            # Find the 2to3 executable
            import shutil as sh
            import platform

            tool_2to3 = sh.which("2to3")
            if not tool_2to3:
                # Try Windows executable name
                tool_2to3 = sh.which("2to3.exe")

            if not tool_2to3:
                # Try to find it in common Python installation paths
                system = platform.system().lower()
                if system == "windows":
                    # Windows paths
                    import sys

                    python_dir = os.path.dirname(sys.executable)
                    possible_paths = [
                        os.path.join(python_dir, "Scripts", "2to3.exe"),
                        os.path.join(python_dir, "Tools", "scripts", "2to3.py"),
                        r"C:\Python*\Scripts\2to3.exe",
                        r"C:\Python*\Tools\scripts\2to3.py",
                    ]
                else:
                    # Unix/Linux/macOS paths
                    possible_paths = [
                        "/Library/Frameworks/Python.framework/Versions/3.11/bin/2to3",
                        "/usr/bin/2to3",
                        "/usr/local/bin/2to3",
                    ]

                for path in possible_paths:
                    if "*" in path:
                        # Handle wildcard paths for Windows
                        import glob

                        matches = glob.glob(path)
                        if matches:
                            tool_2to3 = matches[0]
                            break
                    elif os.path.exists(path):
                        tool_2to3 = path
                        break

                if not tool_2to3:
                    # Last resort: try to find lib2to3 directly
                    try:
                        import lib2to3.main

                        tool_2to3 = "lib2to3.main"
                    except ImportError:
                        # Debug information for troubleshooting
                        debug_info = f"Python executable: {sys.executable}\n"
                        debug_info += (
                            f"Python directory: {os.path.dirname(sys.executable)}\n"
                        )
                        debug_info += f"System: {platform.system()}\n"

                        raise RuntimeError(
                            f"Could not find 2to3 tool. Debug info:\n{debug_info}\n"
                            "Please ensure Python is properly installed with the standard library tools."
                        )

            # Build command
            if tool_2to3 == "lib2to3.main":
                # Use lib2to3 directly through Python
                cmd = [
                    sys.executable,
                    "-m",
                    "lib2to3",
                    "-w",
                    "--no-diffs",
                    os.path.abspath(file_path),
                ]
            elif tool_2to3.endswith(".py"):
                cmd = [
                    sys.executable,
                    tool_2to3,
                    "-w",
                    "--no-diffs",
                    os.path.abspath(file_path),
                ]
            else:
                cmd = [tool_2to3, "-w", "--no-diffs", os.path.abspath(file_path)]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                # Handle errors
                error_msg = f"2to3 failed: {result.stderr}"
                return ConversionResult(
                    file_path, False, "", error_msg, original_content
                )

            # Read converted content
            with open(file_path, "r", encoding="utf-8") as f:
                converted_content = f.read()

            return ConversionResult(
                file_path, True, converted_content, "", original_content
            )

        except Exception as e:
            error_msg = f"2to3 conversion error: {str(e)}"
            return ConversionResult(file_path, False, "", error_msg, original_content)

    def _convert_with_fissix(
        self, file_path: str, original_content: str = ""
    ) -> ConversionResult:
        """Convert file using fissix tool for enhanced conversion."""
        try:
            # Read original content if not provided
            if not original_content:
                with open(file_path, "r", encoding="utf-8") as f:
                    original_content = f.read()

            # Use the current Python environment to run fissix
            python_executable = sys.executable

            cmd = [
                python_executable,
                "-m",
                "fissix",
                "-w",
                "--no-diffs",
                os.path.abspath(file_path),
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                # Handle errors
                error_msg = f"fissix failed: {result.stderr}"
                return ConversionResult(
                    file_path, False, "", error_msg, original_content
                )

            # Read converted content
            with open(file_path, "r", encoding="utf-8") as f:
                converted_content = f.read()

            return ConversionResult(
                file_path, True, converted_content, "", original_content
            )

        except Exception as e:
            error_msg = f"fissix conversion error: {str(e)}"
            return ConversionResult(file_path, False, "", error_msg, original_content)

    def convert_directory(
        self, directory: str, backup: bool = True
    ) -> List[ConversionResult]:
        """Convert all Python files in a directory."""
        python_files = self.find_python_files(directory)
        results = []

        total_files = len(python_files)

        for i, file_path in enumerate(python_files):
            if self.progress_callback:
                progress = (i / total_files) * 100
                self.progress_callback(
                    f"Converting {os.path.basename(file_path)}", progress
                )

            result = self.convert_file(file_path, backup)
            results.append(result)

        if self.progress_callback:
            self.progress_callback("Conversion complete", 100)

        self.conversion_results = results
        return results

    def get_summary(self) -> Dict[str, int]:
        """Get summary statistics of the conversion."""
        total = len(self.conversion_results)
        successful = sum(1 for r in self.conversion_results if r.success)
        failed = total - successful
        modified = sum(
            1 for r in self.conversion_results if r.success and r.changes_made
        )

        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "modified": modified,
            "unchanged": successful - modified,
        }

    def get_failed_conversions(self) -> List[ConversionResult]:
        """Get list of files that failed to convert."""
        return [r for r in self.conversion_results if not r.success]

    def restore_backups(self, directory: str) -> List[str]:
        """Restore all backup files in directory."""
        restored = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py2bak"):
                    backup_path = os.path.join(root, file)
                    original_path = backup_path[:-7]  # Remove .py2bak extension

                    try:
                        shutil.move(backup_path, original_path)
                        restored.append(original_path)
                    except Exception as e:
                        print(f"Failed to restore {backup_path}: {e}")

        return restored
