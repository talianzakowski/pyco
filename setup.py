"""
Setup script for Python 2 to 3 Converter
"""

from setuptools import setup, find_packages

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="cc-py2to3",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive GUI application for converting Python 2 codebases to Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/cc-py2to3",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=7.0.0",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "cc-py2to3=main:main",
        ],
        "gui_scripts": [
            "cc-py2to3-gui=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
    project_urls={
        "Bug Reports": "https://github.com/your-username/cc-py2to3/issues",
        "Source": "https://github.com/your-username/cc-py2to3",
        "Documentation": "https://github.com/your-username/cc-py2to3#readme",
    },
)
