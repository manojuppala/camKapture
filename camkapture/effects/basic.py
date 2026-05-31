"""Basic image effects."""
import cv2
import numpy as np
from .base import Effect


class FlipVertical(Effect):
    """Flip image vertically (mirror effect)."""
    
    def __init__(self):
        super().__init__("Flip Vertical")
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        return cv2.flip(frame, 1)


class FlipHorizontal(Effect):
    """Flip image horizontally."""
    
    def __init__(self):
        super().__init__("Flip Horizontal")
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        return cv2.flip(frame, 0)


class Grayscale(Effect):
    """Convert image to grayscale."""
    
    def __init__(self):
        super().__init__("Grayscale")
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


class Sepia(Effect):
    """Apply sepia tone effect."""
    
    def __init__(self, intensity: float = 1.0):
        super().__init__("Sepia", intensity=intensity)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        intensity = self.get_param('intensity', 1.0)
        
        # Sepia transformation matrix
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        
        # Apply sepia filter
        sepia_frame = cv2.transform(frame, sepia_filter)
        
        # Blend with original based on intensity
        result = cv2.addWeighted(frame, 1 - intensity, sepia_frame, intensity, 0)
        return np.clip(result, 0, 255).astype(np.uint8)


class Invert(Effect):
    """Invert image colors (negative effect)."""
    
    def __init__(self):
        super().__init__("Invert")
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        return cv2.bitwise_not(frame)


class Rotate90(Effect):
    """Rotate image 90 degrees clockwise."""
    
    def __init__(self):
        super().__init__("Rotate 90°")
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)


class Rotate180(Effect):
    """Rotate image 180 degrees."""
    
    def __init__(self):
        super().__init__("Rotate 180°")
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        return cv2.rotate(frame, cv2.ROTATE_180)


class Rotate270(Effect):
    """Rotate image 270 degrees clockwise."""

    def __init__(self):
        super().__init__("Rotate 270°")

    def apply(self, frame: np.ndarray) -> np.ndarray:
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)


class BlackAndWhite(Effect):
    """High contrast black and white effect."""

    def __init__(self, threshold: int = 128):
        super().__init__("Black & White", threshold=threshold)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        threshold = self.get_param('threshold', 128)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return cv2.cvtColor(bw, cv2.COLOR_GRAY2BGR)


class Posterize(Effect):
    """Reduce number of colors (posterization effect)."""

    def __init__(self, levels: int = 4):
        super().__init__("Posterize", levels=levels)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        levels = self.get_param('levels', 4)

        # Reduce color depth
        indices = np.arange(0, 256)
        divider = np.linspace(0, 255, levels + 1)[1]
        quantiz = np.int0(np.linspace(0, 255, levels))
        color_levels = np.clip(np.int0(indices / divider), 0, levels - 1)
        palette = quantiz[color_levels]

        # Apply posterization
        result = palette[frame]
        return result.astype(np.uint8)


class Solarize(Effect):
    """Solarization effect (partially inverted based on threshold)."""

    def __init__(self, threshold: int = 128):
        super().__init__("Solarize", threshold=threshold)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        threshold = self.get_param('threshold', 128)

        # Invert pixels above threshold
        result = frame.copy()
        mask = frame > threshold
        result[mask] = 255 - frame[mask]

        return result
