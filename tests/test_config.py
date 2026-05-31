"""Tests for configuration module."""
import unittest
import tempfile
import os
import json

from camkapture.utils.config import Config


class TestConfig(unittest.TestCase):
    """Test Config class."""
    
    def setUp(self):
        """Create temporary config file."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.json')
    
    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
    
    def test_default_config(self):
        """Test default configuration creation."""
        config = Config(self.config_path)
        
        self.assertEqual(config.get('camera.device_id'), 0)
        self.assertEqual(config.get('camera.width'), 1280)
        self.assertEqual(config.get('camera.height'), 720)
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        config = Config(self.config_path)
        config.set('camera.device_id', 1)
        config.set('camera.width', 1920)
        config.save()
        
        # Load config in new instance
        config2 = Config(self.config_path)
        self.assertEqual(config2.get('camera.device_id'), 1)
        self.assertEqual(config2.get('camera.width'), 1920)
    
    def test_get_nested_value(self):
        """Test getting nested configuration values."""
        config = Config(self.config_path)
        
        width = config.get('camera.width')
        self.assertEqual(width, 1280)
        
        # Test with default value
        unknown = config.get('unknown.key', 'default')
        self.assertEqual(unknown, 'default')
    
    def test_set_nested_value(self):
        """Test setting nested configuration values."""
        config = Config(self.config_path)
        
        config.set('camera.fps', 60)
        self.assertEqual(config.get('camera.fps'), 60)
        
        config.set('new.nested.key', 'value')
        self.assertEqual(config.get('new.nested.key'), 'value')


if __name__ == '__main__':
    unittest.main()
