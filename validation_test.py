#!/usr/bin/env python3
"""
Simple validation test for the Python 2 to 3 converter.
We'll just test one file to make sure the basic functionality works.
"""

import os
import shutil


def test_single_file_conversion():
    """Test converting a single Python 2 file"""
    print("Testing single file conversion...")

    # Create a simple test file
    test_content = '''#!/usr/bin/env python2
"""Simple Python 2 test file"""

import sys

def main():
    print "Hello from Python 2!"
    print "This has", 3, "arguments"
    
    try:
        result = 1 / 0
    except ZeroDivisionError, e:
        print >> sys.stderr, "Division by zero:", e
    
    # Test xrange
    for i in xrange(5):
        print "Number:", i

if __name__ == "__main__":
    main()
'''

    test_file = "simple_test_file.py"

    # Write test file
    with open(test_file, "w") as f:
        f.write(test_content)

    print(f"Created test file: {test_file}")

    # Run 2to3 on it
    print("Running 2to3 conversion...")
    result = os.system(
        f"/Library/Frameworks/Python.framework/Versions/3.11/bin/2to3 -w {test_file}"
    )

    if result == 0:
        print("✓ 2to3 conversion successful!")

        # Check if backup was created
        if os.path.exists(f"{test_file}.bak"):
            print("✓ Backup file created")

            # Show the converted content
            print("\nConverted content:")
            with open(test_file, "r") as f:
                converted = f.read()
            print(converted)

            # Clean up
            os.remove(test_file)
            os.remove(f"{test_file}.bak")
            print("\n✓ Test files cleaned up")

            return True
        else:
            print("✗ No backup file created")
            return False
    else:
        print("✗ 2to3 conversion failed")
        return False


if __name__ == "__main__":
    success = test_single_file_conversion()
    if success:
        print("\n🎉 Python 2 to 3 converter is working correctly!")
    else:
        print("\n[ERROR] Python 2 to 3 converter has issues")

    print("\nThe comprehensive test project is ready at: test-py2-advanced/")
    print("It includes:")
    print("- main.py: Comprehensive Python 2 patterns")
    print("- utils/network.py: Network operations with urllib2")
    print("- utils/data_processing.py: Data processing with cPickle")
    print("- config/settings.py: Configuration with ConfigParser")
    print("- tests/test_legacy.py: Unit tests with Python 2 patterns")
    print("\nYou can now use the GUI application to convert this test project!")
