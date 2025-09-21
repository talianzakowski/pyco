#!/usr/bin/env python3
"""
Python 2 to 3 Converter GUI Application

A comprehensive tool for converting Python 2 codebases to Python 3
with detailed error reporting and validation features.
"""

import sys
import os
import tkinter as tk
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.gui.main_window import MainWindow


def main():
    """Main entry point for the application."""
    try:
        # Create the main tkinter window
        root = tk.Tk()

        # Set application icon (if available)
        try:
            # You can add an icon file here if desired
            # root.iconbitmap("icon.ico")
            pass
        except:
            pass

        # Create and run the main application
        app = MainWindow(root)

        # Start the GUI event loop
        root.mainloop()

    except ImportError as e:
        print(f"Import error: {e}")
        print("Please install required dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)

    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()