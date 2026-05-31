"""Image adjustment effects (brightness, contrast, blur, etc.)."""
import cv2
import numpy as np
from .base import Effect


class Brightness(Effect):
    """Adjust image brightness."""
    
    def __init__(self, value: int = 0):
        """
        Initialize brightness effect.
        
        Args:
            value: Brightness adjustment (-100 to 100)
        """
        super().__init__("Brightness", value=value)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        value = self.get_param('value', 0)
        return cv2.convertScaleAbs(frame, alpha=1, beta=value)


class Contrast(Effect):
    """Adjust image contrast."""
    
    def __init__(self, value: float = 1.0):
        """
        Initialize contrast effect.
        
        Args:
            value: Contrast multiplier (0.5 to 3.0)
        """
        super().__init__("Contrast", value=value)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        value = self.get_param('value', 1.0)
        return cv2.convertScaleAbs(frame, alpha=value, beta=0)


class Saturation(Effect):
    """Adjust color saturation."""
    
    def __init__(self, value: float = 1.0):
        """
        Initialize saturation effect.
        
        Args:
            value: Saturation multiplier (0.0 to 2.0)
        """
        super().__init__("Saturation", value=value)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        value = self.get_param('value', 1.0)
        
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Adjust saturation
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * value, 0, 255)
        
        # Convert back to BGR
        hsv = hsv.astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


class Blur(Effect):
    """Apply blur effect."""
    
    def __init__(self, kernel_size: int = 5):
        """
        Initialize blur effect.
        
        Args:
            kernel_size: Blur kernel size (must be odd, 3-31)
        """
        super().__init__("Blur", kernel_size=kernel_size)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        kernel_size = self.get_param('kernel_size', 5)
        # Ensure kernel size is odd
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.blur(frame, (kernel_size, kernel_size))


class GaussianBlur(Effect):
    """Apply Gaussian blur effect."""
    
    def __init__(self, kernel_size: int = 5, sigma: float = 0):
        """
        Initialize Gaussian blur effect.
        
        Args:
            kernel_size: Blur kernel size (must be odd)
            sigma: Gaussian kernel standard deviation
        """
        super().__init__("Gaussian Blur", kernel_size=kernel_size, sigma=sigma)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        kernel_size = self.get_param('kernel_size', 5)
        sigma = self.get_param('sigma', 0)
        # Ensure kernel size is odd
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.GaussianBlur(frame, (kernel_size, kernel_size), sigma)


class Sharpen(Effect):
    """Sharpen image."""
    
    def __init__(self, intensity: float = 1.0):
        """
        Initialize sharpen effect.
        
        Args:
            intensity: Sharpening intensity (0.0 to 2.0)
        """
        super().__init__("Sharpen", intensity=intensity)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        intensity = self.get_param('intensity', 1.0)
        
        # Sharpening kernel
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]]) * intensity
        kernel[1, 1] = 8 * intensity + 1
        
        sharpened = cv2.filter2D(frame, -1, kernel)
        return np.clip(sharpened, 0, 255).astype(np.uint8)


class Temperature(Effect):
    """Adjust color temperature."""

    def __init__(self, value: int = 0):
        """
        Initialize temperature effect.

        Args:
            value: Temperature adjustment (-100 to 100, negative=cool, positive=warm)
        """
        super().__init__("Temperature", value=value)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        value = self.get_param('value', 0)

        # Create temperature adjustment matrix
        result = frame.astype(np.float32)
        if value > 0:  # Warm
            result[:, :, 2] += value  # Increase red
            result[:, :, 0] -= value * 0.5  # Decrease blue
        else:  # Cool
            result[:, :, 0] += abs(value)  # Increase blue
            result[:, :, 2] -= abs(value) * 0.5  # Decrease red

        return np.clip(result, 0, 255).astype(np.uint8)


class Denoise(Effect):
    """Remove noise from image."""

    def __init__(self, strength: int = 10):
        super().__init__("Denoise", strength=strength)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        strength = self.get_param('strength', 10)
        return cv2.fastNlMeansDenoisingColored(frame, None, strength, strength, 7, 21)


class MotionBlur(Effect):
    """Apply motion blur effect."""

    def __init__(self, kernel_size: int = 15, angle: float = 0):
        super().__init__("Motion Blur", kernel_size=kernel_size, angle=angle)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        kernel_size = self.get_param('kernel_size', 15)
        angle = self.get_param('angle', 0)

        # Create motion blur kernel
        kernel = np.zeros((kernel_size, kernel_size))
        kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
        kernel = kernel / kernel_size

        # Rotate kernel by angle
        if angle != 0:
            M = cv2.getRotationMatrix2D((kernel_size / 2, kernel_size / 2), angle, 1)
            kernel = cv2.warpAffine(kernel, M, (kernel_size, kernel_size))

        return cv2.filter2D(frame, -1, kernel)


class AutoLevel(Effect):
    """Auto-level image (normalize histogram)."""

    def __init__(self):
        super().__init__("Auto Level")

    def apply(self, frame: np.ndarray) -> np.ndarray:
        # Normalize each channel
        result = np.zeros_like(frame)
        for i in range(3):
            result[:, :, i] = cv2.normalize(frame[:, :, i], None, 0, 255, cv2.NORM_MINMAX)
        return result


class Gamma(Effect):
    """Adjust gamma correction."""

    def __init__(self, gamma: float = 1.0):
        super().__init__("Gamma", gamma=gamma)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        gamma = self.get_param('gamma', 1.0)

        # Build lookup table
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255
                         for i in np.arange(0, 256)]).astype("uint8")

        # Apply gamma correction
        return cv2.LUT(frame, table)
