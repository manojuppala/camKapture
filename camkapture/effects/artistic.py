"""Artistic effects."""
import cv2
import numpy as np
from .base import Effect


class Cartoonify(Effect):
    """Apply cartoon effect."""
    
    def __init__(self, bilateral_d: int = 9, edge_threshold1: int = 100, edge_threshold2: int = 200):
        super().__init__("Cartoonify", bilateral_d=bilateral_d, 
                        edge_threshold1=edge_threshold1, edge_threshold2=edge_threshold2)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        bilateral_d = self.get_param('bilateral_d', 9)
        threshold1 = self.get_param('edge_threshold1', 100)
        threshold2 = self.get_param('edge_threshold2', 200)
        
        # Apply bilateral filter to reduce noise while keeping edges sharp
        color = cv2.bilateralFilter(frame, bilateral_d, 75, 75)
        
        # Detect edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                      cv2.THRESH_BINARY, 9, 9)
        
        # Combine color and edges
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(color, edges_colored)
        
        return cartoon


class Sketch(Effect):
    """Apply pencil sketch effect."""
    
    def __init__(self, colored: bool = False):
        super().__init__("Sketch", colored=colored)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        colored = self.get_param('colored', False)
        
        if colored:
            sketch_gray, sketch_color = cv2.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
            return sketch_color
        else:
            sketch_gray, _ = cv2.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
            return cv2.cvtColor(sketch_gray, cv2.COLOR_GRAY2BGR)


class OilPainting(Effect):
    """Apply oil painting effect."""
    
    def __init__(self, size: int = 7, dynRatio: int = 1):
        super().__init__("Oil Painting", size=size, dynRatio=dynRatio)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        size = self.get_param('size', 7)
        dynRatio = self.get_param('dynRatio', 1)
        
        try:
            # xphoto module might not be available in all OpenCV builds
            return cv2.xphoto.oilPainting(frame, size, dynRatio)
        except AttributeError:
            # Fallback to bilateral filter approximation
            return cv2.bilateralFilter(frame, 9, 75, 75)


class Vintage(Effect):
    """Apply vintage/retro effect."""
    
    def __init__(self, intensity: float = 0.7):
        super().__init__("Vintage", intensity=intensity)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        intensity = self.get_param('intensity', 0.7)
        
        # Create vintage color transformation
        vintage_filter = np.array([[0.393, 0.769, 0.189],
                                   [0.349, 0.686, 0.168],
                                   [0.272, 0.534, 0.131]])
        
        vintage_frame = cv2.transform(frame, vintage_filter)
        
        # Add slight blur for old photo effect
        vintage_frame = cv2.GaussianBlur(vintage_frame, (3, 3), 0)
        
        # Reduce saturation
        hsv = cv2.cvtColor(vintage_frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] *= 0.6
        vintage_frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Blend with original
        result = cv2.addWeighted(frame, 1 - intensity, vintage_frame, intensity, 0)
        return np.clip(result, 0, 255).astype(np.uint8)


class Vignette(Effect):
    """Apply vignette effect (darkened corners)."""
    
    def __init__(self, intensity: float = 0.5):
        super().__init__("Vignette", intensity=intensity)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        intensity = self.get_param('intensity', 0.5)
        
        rows, cols = frame.shape[:2]
        
        # Create radial gradient mask
        X_resultant_kernel = cv2.getGaussianKernel(cols, cols / 2)
        Y_resultant_kernel = cv2.getGaussianKernel(rows, rows / 2)
        
        kernel = Y_resultant_kernel * X_resultant_kernel.T
        mask = kernel / kernel.max()
        mask = np.dstack([mask] * 3)
        
        # Apply vignette
        vignetted = frame.astype(np.float32) * (1 - intensity + mask * intensity)
        return np.clip(vignetted, 0, 255).astype(np.uint8)


class Pixelate(Effect):
    """Apply pixelation effect."""
    
    def __init__(self, pixel_size: int = 10):
        super().__init__("Pixelate", pixel_size=pixel_size)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        pixel_size = self.get_param('pixel_size', 10)
        
        height, width = frame.shape[:2]
        
        # Shrink image
        temp = cv2.resize(frame, (width // pixel_size, height // pixel_size), 
                         interpolation=cv2.INTER_LINEAR)
        
        # Enlarge back to original size
        output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
        
        return output


class HDR(Effect):
    """Apply HDR (High Dynamic Range) effect."""

    def __init__(self):
        super().__init__("HDR")

    def apply(self, frame: np.ndarray) -> np.ndarray:
        try:
            # Use detail enhancement
            hdr = cv2.detailEnhance(frame, sigma_s=12, sigma_r=0.15)
            return hdr
        except Exception:
            # Fallback if detailEnhance is not available
            return frame


class WarmGlow(Effect):
    """Add warm glow effect."""

    def __init__(self, intensity: float = 0.5):
        super().__init__("Warm Glow", intensity=intensity)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        intensity = self.get_param('intensity', 0.5)

        # Create warm tone
        warm = frame.astype(np.float32)
        warm[:, :, 2] += 30 * intensity  # More red
        warm[:, :, 1] += 15 * intensity  # Some green
        warm = np.clip(warm, 0, 255).astype(np.uint8)

        # Add glow with blur
        glow = cv2.GaussianBlur(warm, (0, 0), 10)
        result = cv2.addWeighted(warm, 1 - intensity * 0.3, glow, intensity * 0.3, 0)

        return result


class CoolTone(Effect):
    """Apply cool/cyan tone effect."""

    def __init__(self, intensity: float = 0.6):
        super().__init__("Cool Tone", intensity=intensity)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        intensity = self.get_param('intensity', 0.6)

        result = frame.astype(np.float32)
        result[:, :, 0] += 30 * intensity  # More blue
        result[:, :, 1] += 15 * intensity  # Some green
        result[:, :, 2] -= 20 * intensity  # Less red

        return np.clip(result, 0, 255).astype(np.uint8)


class FilmGrain(Effect):
    """Add film grain effect."""

    def __init__(self, intensity: float = 0.1):
        super().__init__("Film Grain", intensity=intensity)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        intensity = self.get_param('intensity', 0.1)

        # Generate grain
        grain = np.random.normal(0, 25 * intensity, frame.shape).astype(np.float32)

        # Add grain to frame
        result = frame.astype(np.float32) + grain
        return np.clip(result, 0, 255).astype(np.uint8)


class CrossProcess(Effect):
    """Cross-process film effect."""

    def __init__(self):
        super().__init__("Cross Process")

    def apply(self, frame: np.ndarray) -> np.ndarray:
        # Increase contrast
        result = cv2.convertScaleAbs(frame, alpha=1.3, beta=-30)

        # Shift colors
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 0] = (hsv[:, :, 0] + 10) % 180  # Hue shift
        hsv[:, :, 1] *= 1.2  # More saturation
        hsv = np.clip(hsv, 0, 255).astype(np.uint8)
        hsv[:, :, 0] = np.clip(hsv[:, :, 0], 0, 179)

        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


class Infrared(Effect):
    """Simulate infrared photography."""

    def __init__(self):
        super().__init__("Infrared")

    def apply(self, frame: np.ndarray) -> np.ndarray:
        # Convert to grayscale and invert
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inverted = 255 - gray

        # Create false color infrared look
        result = np.zeros_like(frame)
        result[:, :, 0] = inverted  # Blue channel
        result[:, :, 1] = gray      # Green channel
        result[:, :, 2] = inverted  # Red channel

        return result


class Bleach(Effect):
    """Bleach bypass effect (desaturated, high contrast)."""

    def __init__(self, intensity: float = 0.7):
        super().__init__("Bleach Bypass", intensity=intensity)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        intensity = self.get_param('intensity', 0.7)

        # Increase contrast
        contrasted = cv2.convertScaleAbs(frame, alpha=1.4, beta=-20)

        # Reduce saturation
        hsv = cv2.cvtColor(contrasted, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] *= (1 - intensity * 0.5)
        hsv = np.clip(hsv, 0, 255).astype(np.uint8)

        bleached = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # Blend
        return cv2.addWeighted(frame, 1 - intensity, bleached, intensity, 0)


class Mirror(Effect):
    """Create mirror/kaleidoscope effect."""

    def __init__(self, mode: str = 'horizontal'):
        super().__init__("Mirror", mode=mode)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        mode = self.get_param('mode', 'horizontal')
        h, w = frame.shape[:2]

        if mode == 'horizontal':
            left = frame[:, :w//2]
            mirrored = cv2.flip(left, 1)
            result = np.hstack([left, mirrored])
        elif mode == 'vertical':
            top = frame[:h//2, :]
            mirrored = cv2.flip(top, 0)
            result = np.vstack([top, mirrored])
        else:  # quad
            top_left = frame[:h//2, :w//2]
            top_right = cv2.flip(top_left, 1)
            bottom = cv2.flip(np.hstack([top_left, top_right]), 0)
            result = np.vstack([np.hstack([top_left, top_right]), bottom])

        return cv2.resize(result, (w, h))
