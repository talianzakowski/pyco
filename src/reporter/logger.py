import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import json


class ConversionReporter:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Set up logging
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"conversion_{self.timestamp}.log"
        self.report_file = self.log_dir / f"report_{self.timestamp}.json"

        # Configure logger
        self.logger = logging.getLogger("py2to3_converter")
        self.logger.setLevel(logging.DEBUG)

        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers if not already added
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        self.conversion_data = {
            "timestamp": self.timestamp,
            "start_time": datetime.now().isoformat(),
            "total_files": 0,
            "successful_conversions": 0,
            "failed_conversions": 0,
            "files_modified": 0,
            "files_unchanged": 0,
            "errors": [],
            "warnings": [],
            "file_details": [],
        }

    def log_start(self, directory: str, total_files: int):
        """Log the start of conversion process."""
        self.logger.info(f"Starting conversion of {total_files} files in {directory}")
        self.conversion_data.update(
            {"source_directory": directory, "total_files": total_files}
        )

    def log_file_conversion(
        self, file_path: str, success: bool, changes_made: bool = False, error: str = ""
    ):
        """Log the result of converting a single file."""
        relative_path = os.path.relpath(file_path)

        if success:
            if changes_made:
                self.logger.info(f"✓ Converted: {relative_path}")
                self.conversion_data["files_modified"] += 1
            else:
                self.logger.info(f"○ No changes needed: {relative_path}")
                self.conversion_data["files_unchanged"] += 1
            self.conversion_data["successful_conversions"] += 1
        else:
            self.logger.error(f"✗ Failed: {relative_path} - {error}")
            self.conversion_data["failed_conversions"] += 1
            self.conversion_data["errors"].append(
                {
                    "file": relative_path,
                    "error": error,
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Store detailed file information
        self.conversion_data["file_details"].append(
            {
                "file_path": relative_path,
                "success": success,
                "changes_made": changes_made,
                "error": error if error else None,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def log_warning(self, message: str, file_path: str = ""):
        """Log a warning message."""
        full_message = f"{message}" + (f" in {file_path}" if file_path else "")
        self.logger.warning(full_message)
        self.conversion_data["warnings"].append(
            {
                "message": message,
                "file": file_path,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def log_completion(self):
        """Log the completion of conversion process."""
        self.conversion_data["end_time"] = datetime.now().isoformat()

        summary = self.get_summary()
        self.logger.info("=" * 50)
        self.logger.info("CONVERSION SUMMARY")
        self.logger.info("=" * 50)
        self.logger.info(f"Total files processed: {summary['total']}")
        self.logger.info(f"Successful conversions: {summary['successful']}")
        self.logger.info(f"Failed conversions: {summary['failed']}")
        self.logger.info(f"Files modified: {summary['modified']}")
        self.logger.info(f"Files unchanged: {summary['unchanged']}")

        if summary["failed"] > 0:
            self.logger.info(f"See {self.log_file} for detailed error information")

        # Generate JSON report
        self.generate_report()

    def get_summary(self) -> Dict[str, int]:
        """Get a summary of the conversion results."""
        return {
            "total": self.conversion_data["total_files"],
            "successful": self.conversion_data["successful_conversions"],
            "failed": self.conversion_data["failed_conversions"],
            "modified": self.conversion_data["files_modified"],
            "unchanged": self.conversion_data["files_unchanged"],
        }

    def get_failed_files(self) -> List[Dict[str, Any]]:
        """Get list of files that failed conversion."""
        return self.conversion_data["errors"]

    def get_modified_files(self) -> List[str]:
        """Get list of files that were modified."""
        return [
            detail["file_path"]
            for detail in self.conversion_data["file_details"]
            if detail["changes_made"]
        ]

    def generate_report(self):
        """Generate a detailed JSON report."""
        try:
            with open(self.report_file, "w") as f:
                json.dump(self.conversion_data, f, indent=2)
            self.logger.info(f"Detailed report saved to: {self.report_file}")
        except Exception as e:
            self.logger.error(f"Failed to generate report: {e}")

    def generate_html_report(self) -> str:
        """Generate an HTML report for better readability with VS Code links."""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Python 2 to 3 Conversion Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
        .success {{ color: green; }}
        .error {{ color: red; }}
        .warning {{ color: orange; }}
        .file-list {{ margin-top: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .vscode-link {{ 
            color: #007acc; 
            text-decoration: none; 
            font-family: monospace;
            background: #f8f8f8;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        .vscode-link:hover {{ 
            background: #e0e0e0; 
            text-decoration: underline;
        }}
        .error-details {{
            font-size: 0.9em;
            color: #666;
            font-family: monospace;
            background: #ffe6e6;
            padding: 5px;
            border-radius: 3px;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <h1>Python 2 to 3 Conversion Report</h1>
    <div class="summary">
        <h2>Summary</h2>
        <p><strong>Conversion Time:</strong> {self.conversion_data["start_time"]}</p>
        <p><strong>Source Directory:</strong> {self.conversion_data.get("source_directory", "N/A")}</p>
        <p><strong>Total Files:</strong> {self.conversion_data["total_files"]}</p>
        <p class="success"><strong>Successful:</strong> {self.conversion_data["successful_conversions"]}</p>
        <p class="error"><strong>Failed:</strong> {self.conversion_data["failed_conversions"]}</p>
        <p><strong>Modified:</strong> {self.conversion_data["files_modified"]}</p>
        <p><strong>Unchanged:</strong> {self.conversion_data["files_unchanged"]}</p>
    </div>
"""

        # Add failed conversions section with VS Code links
        if self.conversion_data["errors"]:
            html_content += """
    <div class="file-list">
        <h2 class="error">Failed Conversions</h2>
        <table>
            <tr><th>File</th><th>Error</th></tr>
"""
            for error in self.conversion_data["errors"]:
                file_path = error["file"]
                # Create VS Code link
                vscode_link = f'<a href="vscode://file/{os.path.abspath(file_path)}" class="vscode-link">{file_path}</a>'

                # Parse error for line number if available
                error_text = error["error"]
                line_info = ""
                if "line" in error_text.lower() or "context" in error_text.lower():
                    # Try to extract line number from error messages like "context=(' ', (24, 10))"
                    import re

                    line_match = re.search(r"\((\d+),\s*\d+\)", error_text)
                    if line_match:
                        line_num = line_match.group(1)
                        vscode_link = f'<a href="vscode://file/{os.path.abspath(file_path)}:{line_num}" class="vscode-link">{file_path}:{line_num}</a>'
                        line_info = f" (line {line_num})"

                html_content += f"""
                <tr>
                    <td>{vscode_link}</td>
                    <td>
                        {error_text}
                        <div class="error-details">Click the file link to open in VS Code{line_info}</div>
                    </td>
                </tr>"""
            html_content += "</table></div>"

        # Add all files section with VS Code links
        html_content += """
    <div class="file-list">
        <h2>All Files</h2>
        <table>
            <tr><th>File</th><th>Status</th><th>Changes Made</th></tr>
"""
        for detail in self.conversion_data["file_details"]:
            status = "✓ Success" if detail["success"] else "✗ Failed"
            status_class = "success" if detail["success"] else "error"
            changes = "Yes" if detail["changes_made"] else "No"
            file_path = detail["file_path"]

            # Create VS Code link for each file
            vscode_link = f'<a href="vscode://file/{os.path.abspath(file_path)}" class="vscode-link">{file_path}</a>'

            html_content += f'<tr><td>{vscode_link}</td><td class="{status_class}">{status}</td><td>{changes}</td></tr>'

        html_content += """
        </table>
    </div>
    <div style="margin-top: 20px; padding: 10px; background: #e8f4fd; border-radius: 5px;">
        <p><strong>💡 Tip:</strong> Click on any file path to open it directly in VS Code!</p>
        <p><small>Make sure VS Code is installed and the <code>code</code> command is available in your PATH.</small></p>
    </div>
</body>
</html>
"""

        html_file = self.log_dir / f"report_{self.timestamp}.html"
        try:
            with open(html_file, "w") as f:
                f.write(html_content)
            self.logger.info(f"HTML report saved to: {html_file}")
            return str(html_file)
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {e}")
            return ""
