#!/usr/bin/env python2
"""
Configuration management using Python 2 patterns
"""

import configparser
import sys
import os

class AppConfig(object):
    """Application configuration using ConfigParser"""
    
    def __init__(self, config_file="app.conf"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        print("Loading configuration from:", self.config_file)
        
        try:
            # Set defaults
            self.config.add_section('general')
            self.config.set('general', 'app_name', 'Python2 Test App')
            self.config.set('general', 'version', '1.0')
            self.config.set('general', 'debug', 'False')
            
            self.config.add_section('database')
            self.config.set('database', 'host', 'localhost')
            self.config.set('database', 'port', '5432')
            self.config.set('database', 'name', 'testdb')
            
            # Try to read existing config
            if os.path.exists(self.config_file):
                self.config.read(self.config_file)
                print("Configuration loaded successfully")
            else:
                print("Configuration file not found, using defaults")
                self.save_config()
                
        except configparser.Error as e:
            print("Configuration error:", e, file=sys.stderr)
        except Exception as e:
            print("Failed to load config:", e, file=sys.stderr)
    
    def save_config(self):
        """Save configuration to file"""
        print("Saving configuration to:", self.config_file)
        
        try:
            with open(self.config_file, 'wb') as configfile:
                self.config.write(configfile)
            print("Configuration saved successfully")
        except Exception as e:
            print("Failed to save config:", e, file=sys.stderr)
    
    def get_value(self, section, option, fallback=None):
        """Get configuration value with fallback"""
        try:
            if self.config.has_option(section, option):
                return self.config.get(section, option)
            else:
                print("Option %s.%s not found, using fallback" % (section, option))
                return fallback
        except configparser.NoSectionError as e:
            print("Section not found:", section)
            return fallback
        except Exception as e:
            print("Error getting config value:", e)
            return fallback
    
    def set_value(self, section, option, value):
        """Set configuration value"""
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)
            
            self.config.set(section, option, str(value))
            print("Set %s.%s = %s" % (section, option, value))
            
        except Exception as e:
            print("Error setting config value:", e)
    
    def get_boolean(self, section, option, fallback=False):
        """Get boolean configuration value"""
        try:
            return self.config.getboolean(section, option)
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            print("Boolean option not found:", section, option)
            return fallback
        except ValueError as e:
            print("Invalid boolean value:", e)
            return fallback
    
    def get_int(self, section, option, fallback=0):
        """Get integer configuration value"""
        try:
            return self.config.getint(section, option)
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            print("Integer option not found:", section, option)
            return fallback
        except ValueError as e:
            print("Invalid integer value:", e)
            return fallback
    
    def list_all_options(self):
        """List all configuration options"""
        print("Configuration sections and options:")
        
        for section_name in self.config.sections():
            print("  [%s]" % section_name)
            
            try:
                for option_name in self.config.options(section_name):
                    value = self.config.get(section_name, option_name)
                    print("    %s = %s" % (option_name, value))
            except configparser.Error as e:
                print("    Error reading section:", e)
            
            print()

def test_legacy_imports():
    """Test various Python 2 import patterns"""
    print("Testing legacy import patterns...")
    
    try:
        # Test importing renamed modules
        import pickle
        print("cPickle imported successfully")
        
        import io
        print("cStringIO imported successfully")
        
        # Test importing removed modules
        try:
            import sets
            print("sets module imported")
        except ImportError as e:
            print("sets module not available:", e)
        
        try:
            import md5
            print("md5 module imported")
        except ImportError as e:
            print("md5 module not available:", e)
        
        try:
            import sha
            print("sha module imported")  
        except ImportError as e:
            print("sha module not available:", e)
            
    except ImportError as e:
        print("Import error:", e)

if __name__ == "__main__":
    print("Configuration management test")
    print("=" * 50)
    
    # Test configuration
    config = AppConfig("test_config.ini")
    
    # Test getting values
    app_name = config.get_value('general', 'app_name')
    debug_mode = config.get_boolean('general', 'debug')
    db_port = config.get_int('database', 'port')
    
    print("App name:", app_name)
    print("Debug mode:", debug_mode)
    print("Database port:", db_port)
    print()
    
    # Test setting values
    config.set_value('general', 'last_run', '2023-01-01')
    config.set_value('features', 'feature_x', 'enabled')
    
    # List all options
    config.list_all_options()
    
    # Test legacy imports
    test_legacy_imports()