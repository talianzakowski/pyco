#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Data processing utilities for legacy Python 2 application
"""

import configparser
import urllib.request, urllib.error, urllib.parse
import urllib.parse
from io import StringIO
import pickle as pickle
import builtins

class DataProcessor:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.data_cache = {}

    def process_text(self, text):
        """Process text data with Python 2 patterns"""
        # Old print statement
        print(("Processing text:", repr(text)))

        # Unicode handling
        if isinstance(text, str):
            text = str(text, 'utf-8')

        # String formatting
        result = "Processed: %s (length: %d)" % (text, len(text))

        # Old-style string methods
        if 'special' in text:
            print("Found special key")

        return result

    def fetch_data(self, url):
        """Fetch data from URL using legacy urllib2"""
        try:
            response = urllib.request.urlopen(url)
            data = response.read()
            print(("Fetched %d bytes from %s" % (len(data), url)))
            return data
        except urllib.error.URLError as e:
            print(("Error fetching data:", e))
            return None

    def save_cache(self, filename):
        """Save cache using cPickle"""
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self.data_cache, f, pickle.HIGHEST_PROTOCOL)
            print(("Cache saved to", filename))
        except IOError as e:
            print(("Failed to save cache:", e))

    def process_numbers(self, numbers):
        """Process numbers with xrange and old division"""
        total = 0
        for i in range(len(numbers)):
            # Old division behavior
            result = numbers[i] / 2
            total += result
            print(("Item %d: %f" % (i, result)))

        return total

    def iterate_dict(self, data_dict):
        """Iterate over dictionary using old methods"""
        print("Dictionary contents:")
        for key, value in list(data_dict.items()):
            print(("  %s: %s" % (key, value)))

        keys = list(data_dict.keys())
        values = list(data_dict.values())
        items = list(data_dict.items())

        return len(keys)

def main():
    # Raw input
    try:
        user_input = eval(input("Enter some data: "))
        print(("You entered:", user_input))
    except EOFError:
        print("No input provided")

    # Create processor
    processor = DataProcessor("config.ini")

    # Test data processing
    test_data = [1, 2, 3, 4, 5]
    result = processor.process_numbers(test_data)
    print(("Total result:", result))

    # Test dictionary iteration
    test_dict = {'a': 1, 'b': 2, 'c': 3}
    count = processor.iterate_dict(test_dict)
    print(("Dictionary size:", count))

if __name__ == '__main__':
    main()