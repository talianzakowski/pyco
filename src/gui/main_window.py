import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
import webbrowser

from ..converter.engine import Python2to3Converter, ConversionResult
from ..reporter.logger import ConversionReporter


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 2 to 3 Converter")
        self.root.geometry("800x600")

        # Variables
        self.selected_directory = tk.StringVar()
        self.create_backup = tk.BooleanVar(value=True)
        self.use_fissix_enhancement = tk.BooleanVar(value=True)
        self.conversion_running = False

        # Initialize components
        self.converter = None
        self.reporter = None

        # Setup GUI
        self.setup_gui()

    def setup_gui(self):
        """Create the main GUI layout."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame, text="Python 2 to 3 Converter", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Directory selection
        ttk.Label(main_frame, text="Select Directory:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )

        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        dir_frame.columnconfigure(0, weight=1)

        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.selected_directory)
        self.dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))

        # Add tooltip and enable manual entry
        self.dir_entry.bind("<Return>", self.on_path_entered)

        self.browse_button = ttk.Button(
            dir_frame, text="Browse", command=self.browse_directory
        )
        self.browse_button.grid(row=0, column=1)

        # Add help text
        help_label = ttk.Label(
            main_frame,
            text="Tip: You can type a path directly or click Browse to select",
            font=("Arial", 9),
            foreground="gray",
        )
        help_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))

        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        self.backup_checkbox = ttk.Checkbutton(
            options_frame,
            text="Create backup files (.py2bak)",
            variable=self.create_backup,
        )
        self.backup_checkbox.grid(row=0, column=0, sticky=tk.W)

        self.fissix_checkbox = ttk.Checkbutton(
            options_frame,
            text="Use enhanced conversion (fissix) for sort(cmp=...) patterns",
            variable=self.use_fissix_enhancement,
        )
        self.fissix_checkbox.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))

        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)

        self.progress_label = ttk.Label(
            progress_frame, text="Ready to start conversion"
        )
        self.progress_label.grid(row=0, column=0, sticky=tk.W)

        self.progress_bar = ttk.Progressbar(progress_frame, mode="determinate")
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)

        self.convert_button = ttk.Button(
            button_frame,
            text="Start Conversion",
            command=self.start_conversion,
            style="Accent.TButton",
        )
        self.convert_button.pack(side=tk.LEFT, padx=5)

        self.restore_button = ttk.Button(
            button_frame,
            text="Restore Backups",
            command=self.restore_backups,
            state="disabled",
        )
        self.restore_button.pack(side=tk.LEFT, padx=5)

        self.view_logs_button = ttk.Button(
            button_frame, text="View Logs", command=self.view_logs, state="normal"
        )  # Always enabled
        self.view_logs_button.pack(side=tk.LEFT, padx=5)

        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(
            row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10
        )
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)

        # Results text area with scrollbar
        self.results_text = scrolledtext.ScrolledText(
            results_frame, height=15, state="disabled"
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Status bar
        self.status_bar = ttk.Label(
            main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.grid(
            row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0)
        )

    def browse_directory(self):
        """Open directory browser dialog."""
        try:
            # Add some debug info
            self.update_status("Opening directory browser...")

            # Configure the file dialog
            directory = filedialog.askdirectory(
                title="Select Python project directory", mustexist=True
            )

            if directory:
                self.selected_directory.set(directory)
                self.update_status(f"Selected: {directory}")
                self.log_to_results(f"Selected directory: {directory}", "INFO")
            else:
                self.update_status("No directory selected")

        except Exception as e:
            error_msg = f"Error opening directory browser: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("Error", error_msg)

    def on_path_entered(self, event):
        """Handle manual path entry when user presses Enter."""
        path = self.selected_directory.get().strip()
        if path:
            if os.path.exists(path):
                self.update_status(f"Path entered: {path}")
                self.log_to_results(f"Manual path entered: {path}", "INFO")
            else:
                self.update_status(f"Path does not exist: {path}")
                messagebox.showwarning(
                    "Invalid Path", f"The path does not exist:\n{path}"
                )

    def update_status(self, message):
        """Update the status bar."""
        self.status_bar.config(text=message)

    def update_progress(self, message, progress):
        """Update progress bar and label."""
        self.progress_label.config(text=message)
        self.progress_bar["value"] = progress
        self.root.update_idletasks()

    def log_to_results(self, message, level="INFO"):
        """Add message to results text area."""
        self.results_text.config(state="normal")

        # Add color coding based on level
        if level == "ERROR":
            tag = "error"
            self.results_text.tag_config(tag, foreground="red")
        elif level == "SUCCESS":
            tag = "success"
            self.results_text.tag_config(tag, foreground="green")
        elif level == "WARNING":
            tag = "warning"
            self.results_text.tag_config(tag, foreground="orange")
        else:
            tag = "info"
            self.results_text.tag_config(tag, foreground="black")

        self.results_text.insert(tk.END, message + "\n", tag)
        self.results_text.see(tk.END)
        self.results_text.config(state="disabled")

    def validate_directory(self):
        """Validate selected directory."""
        directory = self.selected_directory.get()

        if not directory:
            messagebox.showerror("Error", "Please select a directory first.")
            return False

        if not os.path.exists(directory):
            messagebox.showerror("Error", "Selected directory does not exist.")
            return False

        # Check if directory contains Python files
        python_files = []
        for root, dirs, files in os.walk(directory):
            python_files.extend([f for f in files if f.endswith(".py")])

        if not python_files:
            result = messagebox.askyesno(
                "Warning",
                "No Python files found in the selected directory. Continue anyway?",
            )
            return result

        return True

    def start_conversion(self):
        """Start the conversion process in a separate thread."""
        print("DEBUG: start_conversion called!")  # Debug line

        if not self.validate_directory():
            print("DEBUG: Directory validation failed")  # Debug line
            return

        if self.conversion_running:
            print("DEBUG: Conversion already running")  # Debug line
            messagebox.showwarning("Warning", "Conversion is already running.")
            return

        print("DEBUG: Starting conversion process")  # Debug line

        # Confirm action
        directory = self.selected_directory.get()
        backup_msg = (
            " (with backups)" if self.create_backup.get() else " (without backups)"
        )

        result = messagebox.askyesno(
            "Confirm",
            f"Start converting Python files in:\n{directory}{backup_msg}\n\n"
            "This will modify Python files. Continue?",
        )
        if not result:
            return

        # Disable buttons and clear results
        self.convert_button.config(state="disabled")
        self.browse_button.config(state="disabled")
        self.backup_checkbox.config(state="disabled")
        self.fissix_checkbox.config(state="disabled")
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state="disabled")

        self.conversion_running = True

        # Start conversion in separate thread
        thread = threading.Thread(target=self.run_conversion, daemon=True)
        thread.start()

    def run_conversion(self):
        """Run the actual conversion process."""
        try:
            directory = self.selected_directory.get()

            # Initialize reporter
            self.reporter = ConversionReporter()

            # Initialize converter with progress callback
            self.converter = Python2to3Converter(
                progress_callback=self.update_progress,
                use_fissix_second_stage=self.use_fissix_enhancement.get()
            )

            # Find Python files
            python_files = self.converter.find_python_files(directory)

            self.log_to_results(
                f"Found {len(python_files)} Python files in {directory}"
            )
            self.reporter.log_start(directory, len(python_files))

            # Convert files
            results = self.converter.convert_directory(
                directory, self.create_backup.get()
            )

            # Process results
            for result in results:
                if result.success:
                    if result.changes_made:
                        self.log_to_results(
                            f"✓ Converted: {os.path.basename(result.file_path)}",
                            "SUCCESS",
                        )
                    else:
                        self.log_to_results(
                            f"○ No changes: {os.path.basename(result.file_path)}",
                            "INFO",
                        )
                else:
                    self.log_to_results(
                        f"✗ Failed: {os.path.basename(result.file_path)} - {result.error}",
                        "ERROR",
                    )

                self.reporter.log_file_conversion(
                    result.file_path, result.success, result.changes_made, result.error
                )

            # Show summary
            summary = self.converter.get_summary()
            self.reporter.log_completion()

            self.log_to_results("\n" + "=" * 50, "INFO")
            self.log_to_results("CONVERSION SUMMARY", "INFO")
            self.log_to_results("=" * 50, "INFO")
            self.log_to_results(f"Total files: {summary['total']}", "INFO")
            self.log_to_results(f"Successful: {summary['successful']}", "SUCCESS")
            self.log_to_results(
                f"Failed: {summary['failed']}",
                "ERROR" if summary["failed"] > 0 else "INFO",
            )
            self.log_to_results(f"Modified: {summary['modified']}", "SUCCESS")
            self.log_to_results(f"Unchanged: {summary['unchanged']}", "INFO")

            if summary["failed"] > 0:
                self.log_to_results(
                    f"\nCheck logs for detailed error information.", "WARNING"
                )

            self.update_status("Conversion completed")

            # Enable restore button if backups were created
            if self.create_backup.get():
                self.restore_button.config(state="normal")

        except Exception as e:
            self.log_to_results(f"Conversion failed: {str(e)}", "ERROR")
            self.update_status("Conversion failed")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

        finally:
            # Re-enable buttons
            self.conversion_running = False
            self.convert_button.config(state="normal")
            self.browse_button.config(state="normal")
            self.backup_checkbox.config(state="normal")
            self.fissix_checkbox.config(state="normal")
            self.update_progress("Conversion complete", 100)

    def restore_backups(self):
        """Restore backup files."""
        if not self.converter:
            messagebox.showwarning("Warning", "No conversion has been performed yet.")
            return

        directory = self.selected_directory.get()
        result = messagebox.askyesno(
            "Confirm",
            f"Restore all backup files in:\n{directory}\n\n"
            "This will overwrite converted files. Continue?",
        )
        if not result:
            return

        try:
            restored = self.converter.restore_backups(directory)
            self.log_to_results(
                f"\nRestored {len(restored)} files from backups", "SUCCESS"
            )
            for file_path in restored:
                self.log_to_results(f"Restored: {os.path.basename(file_path)}", "INFO")

            self.update_status(f"Restored {len(restored)} files")
            messagebox.showinfo(
                "Success", f"Restored {len(restored)} files from backups."
            )

        except Exception as e:
            self.log_to_results(f"Restore failed: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Restore failed: {str(e)}")

    def view_logs(self):
        """Open the log directory in file manager."""
        log_dir = "logs"  # Default log directory

        # If we have an active reporter, use its log directory
        if self.reporter:
            log_dir = str(self.reporter.log_dir)

        # Check if log directory exists
        if not os.path.exists(log_dir):
            messagebox.showwarning(
                "Warning", f"Log directory '{log_dir}' does not exist."
            )
            return

        # Check if there are any log files
        log_files = [
            f for f in os.listdir(log_dir) if f.endswith(".log") or f.endswith(".html")
        ]
        if not log_files:
            messagebox.showwarning("Warning", "No log files found.")
            return

        try:
            # Try to find and open the most recent HTML report
            html_files = [f for f in os.listdir(log_dir) if f.endswith(".html")]
            if html_files:
                # Get the most recent HTML file
                html_files.sort(reverse=True)
                html_report = os.path.join(log_dir, html_files[0])
                webbrowser.open(f"file://{os.path.abspath(html_report)}")
            else:
                # No HTML report, just open the log directory
                if os.name == "nt":  # Windows
                    os.startfile(log_dir)
                elif os.name == "posix":  # macOS and Linux
                    import subprocess

                    if os.uname().sysname == "Darwin":  # macOS
                        subprocess.run(["open", log_dir])
                    else:  # Linux
                        subprocess.run(["xdg-open", log_dir])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open logs: {str(e)}")


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
