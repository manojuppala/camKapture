"""Configuration management."""
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class Config:
    """Application configuration manager."""
    
    DEFAULT_CONFIG = {
        "camera": {
            "device_id": 0,
            "width": 1280,
            "height": 720,
            "fps": 30
        },
        "output": {
            "image_dir": os.path.join(os.path.expanduser("~"), "Pictures", "camKapture"),
            "video_dir": os.path.join(os.path.expanduser("~"), "Videos", "camKapture"),
            "image_format": "jpg",
            "video_format": "mp4"
        },
        "ui": {
            "theme": "light",
            "window_width": 1024,
            "window_height": 768,
            "preview_width": 640,
            "preview_height": 480
        },
        "capture": {
            "burst_interval": 10,
            "timer_seconds": 10,
            "show_flash": True
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to config file (default: ~/.camkapture/config.json)
        """
        if config_path is None:
            config_dir = os.path.join(os.path.expanduser("~"), ".camkapture")
            os.makedirs(config_dir, exist_ok=True)
            config_path = os.path.join(config_dir, "config.json")

        self.config_path = config_path
        self.data = {}  # Initialize data before _load_config
        self.data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
                # Merge with defaults to handle missing keys
                return self._merge_configs(self.DEFAULT_CONFIG.copy(), config)
            except Exception as e:
                logger.error(f"Failed to load config: {e}. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save()
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: Dict, custom: Dict) -> Dict:
        """Recursively merge custom config with default."""
        for key, value in custom.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                default[key] = self._merge_configs(default[key], value)
            else:
                default[key] = value
        return default
    
    def save(self):
        """Save current configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.data, f, indent=4)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Config key path (e.g., 'camera.width')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation.
        
        Args:
            key_path: Config key path (e.g., 'camera.width')
            value: Value to set
        """
        keys = key_path.split('.')
        data = self.data
        for key in keys[:-1]:
            if key not in data:
                data[key] = {}
            data = data[key]
        data[keys[-1]] = value
