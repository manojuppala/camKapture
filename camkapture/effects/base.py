"""Base effect class."""
from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, Any


class Effect(ABC):
    """Base class for all image effects."""
    
    def __init__(self, name: str, **params):
        """
        Initialize effect.
        
        Args:
            name: Effect name
            **params: Effect parameters
        """
        self.name = name
        self.params = params
        self.enabled = True
    
    @abstractmethod
    def apply(self, frame: np.ndarray) -> np.ndarray:
        """
        Apply effect to frame.
        
        Args:
            frame: Input frame
            
        Returns:
            Processed frame
        """
        pass
    
    def __call__(self, frame: np.ndarray) -> np.ndarray:
        """Make effect callable."""
        if not self.enabled:
            return frame
        return self.apply(frame)
    
    def set_param(self, key: str, value: Any):
        """Set effect parameter."""
        self.params[key] = value
    
    def get_param(self, key: str, default: Any = None) -> Any:
        """Get effect parameter."""
        return self.params.get(key, default)
    
    def toggle(self):
        """Toggle effect on/off."""
        self.enabled = not self.enabled
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', enabled={self.enabled})"
