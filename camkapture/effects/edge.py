"""Edge detection and related effects."""
import cv2
import numpy as np
from .base import Effect


class EdgeDetection(Effect):
    """Canny edge detection."""
    
    def __init__(self, threshold1: int = 100, threshold2: int = 200):
        super().__init__("Edge Detection", threshold1=threshold1, threshold2=threshold2)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        threshold1 = self.get_param('threshold1', 100)
        threshold2 = self.get_param('threshold2', 200)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)
        
        # Convert back to BGR for display
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


class Sobel(Effect):
    """Sobel edge detection."""
    
    def __init__(self):
        super().__init__("Sobel")
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Sobel operator
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Combine gradients
        sobel = np.sqrt(sobelx**2 + sobely**2)
        sobel = np.clip(sobel, 0, 255).astype(np.uint8)
        
        return cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)


class Emboss(Effect):
    """Apply emboss effect."""
    
    def __init__(self, intensity: float = 1.0):
        super().__init__("Emboss", intensity=intensity)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        intensity = self.get_param('intensity', 1.0)
        
        # Emboss kernel
        kernel = np.array([[-2, -1,  0],
                          [-1,  1,  1],
                          [ 0,  1,  2]]) * intensity
        
        embossed = cv2.filter2D(frame, -1, kernel)
        
        # Add gray offset for better visibility
        embossed = cv2.add(embossed, np.array([128.0]))
        
        return np.clip(embossed, 0, 255).astype(np.uint8)


class Laplacian(Effect):
    """Laplacian edge detection."""

    def __init__(self):
        super().__init__("Laplacian")

    def apply(self, frame: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian = np.abs(laplacian)
        laplacian = np.clip(laplacian, 0, 255).astype(np.uint8)

        return cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)


class Outline(Effect):
    """Create outline effect (inverted edges on white)."""

    def __init__(self):
        super().__init__("Outline")

    def apply(self, frame: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)

        # Invert for white background
        inverted = 255 - edges

        return cv2.cvtColor(inverted, cv2.COLOR_GRAY2BGR)
