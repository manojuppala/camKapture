"""Color-based effects and filters."""
import cv2
import numpy as np
from .base import Effect


class Negative(Effect):
    """Color negative effect (different from simple invert)."""
    
    def __init__(self):
        super().__init__("Negative")
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        return cv2.bitwise_not(frame)


class DuoTone(Effect):
    """Duo-tone color effect."""
    
    def __init__(self, color1: tuple = (255, 100, 0), color2: tuple = (0, 100, 255)):
        super().__init__("Duo Tone", color1=color1, color2=color2)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        color1 = self.get_param('color1', (255, 100, 0))
        color2 = self.get_param('color2', (0, 100, 255))
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Normalize
        normalized = gray.astype(np.float32) / 255.0
        
        # Create duo-tone
        result = np.zeros(frame.shape, dtype=np.float32)
        for i in range(3):
            result[:, :, i] = normalized * color1[i] + (1 - normalized) * color2[i]
        
        return np.clip(result, 0, 255).astype(np.uint8)


class ColorPop(Effect):
    """Keep one color, desaturate rest."""
    
    def __init__(self, hue_target: int = 0, hue_range: int = 30):
        """
        Args:
            hue_target: Target hue to keep (0-179 in OpenCV HSV)
            hue_range: Range around target hue to keep
        """
        super().__init__("Color Pop", hue_target=hue_target, hue_range=hue_range)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        hue_target = self.get_param('hue_target', 0)
        hue_range = self.get_param('hue_range', 30)
        
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for target color
        lower = np.array([max(0, hue_target - hue_range), 50, 50])
        upper = np.array([min(179, hue_target + hue_range), 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        
        # Desaturate everything
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        desaturated = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        # Keep only target color from original
        result = desaturated.copy()
        result[mask > 0] = frame[mask > 0]
        
        return result


class LUT(Effect):
    """Apply Look-Up Table for color grading."""
    
    def __init__(self, lut_type: str = 'warm'):
        super().__init__("LUT", lut_type=lut_type)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        lut_type = self.get_param('lut_type', 'warm')
        
        # Create LUT based on type
        if lut_type == 'warm':
            # Warm LUT
            lut = np.array([i for i in range(256)]).astype(np.uint8)
            lut_red = np.clip(lut * 1.1, 0, 255).astype(np.uint8)
            lut_green = lut
            lut_blue = np.clip(lut * 0.9, 0, 255).astype(np.uint8)
        elif lut_type == 'cool':
            # Cool LUT
            lut = np.array([i for i in range(256)]).astype(np.uint8)
            lut_red = np.clip(lut * 0.9, 0, 255).astype(np.uint8)
            lut_green = lut
            lut_blue = np.clip(lut * 1.1, 0, 255).astype(np.uint8)
        else:  # contrast
            # High contrast LUT
            lut = np.array([int(((i / 255.0) ** 0.7) * 255) for i in range(256)]).astype(np.uint8)
            lut_red = lut_green = lut_blue = lut
        
        # Apply LUT to each channel
        result = frame.copy()
        result[:, :, 0] = cv2.LUT(frame[:, :, 0], lut_blue)
        result[:, :, 1] = cv2.LUT(frame[:, :, 1], lut_green)
        result[:, :, 2] = cv2.LUT(frame[:, :, 2], lut_red)
        
        return result


class ChannelSwap(Effect):
    """Swap color channels."""
    
    def __init__(self, mode: str = 'BGR2RGB'):
        super().__init__("Channel Swap", mode=mode)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        mode = self.get_param('mode', 'BGR2RGB')
        
        if mode == 'BGR2RGB':
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif mode == 'BGR2GBR':
            return frame[:, :, [1, 0, 2]]
        elif mode == 'BGR2RBG':
            return frame[:, :, [2, 0, 1]]
        else:
            return frame


class ColorBalance(Effect):
    """Adjust color balance."""
    
    def __init__(self, red: float = 1.0, green: float = 1.0, blue: float = 1.0):
        super().__init__("Color Balance", red=red, green=green, blue=blue)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        red = self.get_param('red', 1.0)
        green = self.get_param('green', 1.0)
        blue = self.get_param('blue', 1.0)
        
        result = frame.astype(np.float32)
        result[:, :, 0] *= blue
        result[:, :, 1] *= green
        result[:, :, 2] *= red
        
        return np.clip(result, 0, 255).astype(np.uint8)
