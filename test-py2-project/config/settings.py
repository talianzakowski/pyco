#!/usr/bin/env python2
"""
Configuration settings for the application
"""

# Import statements that changed in Python 3
import configparser
import socketserver
import http.server
import http.server
from urllib.parse import urljoin, urlparse
from urllib.parse import quote, unquote
from html.parser import HTMLParser

# Configuration class
class AppConfig:
    def __init__(self):
        self.config_parser = configparser.SafeConfigParser()
        self.settings = {}
        self._load_defaults()

    def _load_defaults(self):
        """Load default configuration values"""
        self.settings = {
            'database_url': 'sqlite:///app.db',
            'debug': True,
            'port': 8080,
            'host': 'localhost'
        }

        print("Loaded default settings:")
        for key, value in list(self.settings.items()):
            print(("  %s = %r" % (key, value)))

    def load_from_file(self, config_file):
        """Load configuration from INI file"""
        try:
            self.config_parser.read(config_file)
            print(("Loading config from:", config_file))

            # Process each section
            for section in self.config_parser.sections():
                print(("Processing section:", section))
                for option in self.config_parser.options(section):
                    value = self.config_parser.get(section, option)
                    key = "%s_%s" % (section, option)
                    self.settings[key] = value
                    print(("  Set %s = %s" % (key, value)))

        except Exception as e:
            print(("Error loading config:", e))

    def get_setting(self, key, default=None):
        """Get a configuration setting"""
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        """Set a configuration setting"""
        print(("Setting %s = %r" % (key, value)))
        self.settings[key] = value

    def validate_url(self, url):
        """Validate URL using old urlparse"""
        parsed = urlparse(url)
        if parsed.scheme and parsed.netloc:
            print(("Valid URL:", url))
            return True
        else:
            print(("Invalid URL:", url))
            return False

    def encode_url_component(self, text):
        """Encode URL component using old urllib"""
        encoded = quote(text)
        print(("Encoded '%s' as '%s'" % (text, encoded)))
        return encoded

# Global configuration instance
config = AppConfig()

def print_config():
    """Print current configuration"""
    print("Current configuration:")
    print(("=" * 40))
    for key in sorted(config.settings.keys()):
        value = config.settings[key]
        print(("%s: %s" % (key, value)))
    print(("=" * 40))

if __name__ == "__main__":
    print("Configuration module test")

    # Test configuration
    config.set_setting('test_key', 'test_value')

    # Test URL validation
    test_urls = [
        'http://example.com',
        'https://test.org/path',
        'invalid-url',
        'ftp://files.example.com'
    ]

    for url in test_urls:
        config.validate_url(url)

    # Test URL encoding
    test_strings = [
        'hello world',
        'special/chars?&=',
        'unicode: café'
    ]

    for text in test_strings:
        config.encode_url_component(text)

    print_config()