"""Image effects and filters."""
from .base import Effect
from .basic import (
    FlipVertical, FlipHorizontal, Grayscale, Sepia, Invert,
    BlackAndWhite, Posterize, Solarize
)
from .artistic import (
    Cartoonify, Sketch, OilPainting, Vintage, Vignette, Pixelate, HDR,
    WarmGlow, CoolTone, FilmGrain, CrossProcess, Infrared, Bleach, Mirror
)
from .adjustments import (
    Brightness, Contrast, Saturation, Blur, Sharpen, GaussianBlur,
    Temperature, Denoise, MotionBlur, AutoLevel, Gamma
)
from .edge import (
    EdgeDetection, Emboss, Sobel, Laplacian
)
from .color import (
    Negative, DuoTone, ColorPop, LUT, ChannelSwap, ColorBalance
)

# Export all effects
__all__ = [
    'Effect',
    # Basic effects
    'FlipVertical', 'FlipHorizontal', 'Grayscale', 'Sepia', 'Invert',
    'BlackAndWhite', 'Posterize', 'Solarize',
    # Artistic effects
    'Cartoonify', 'Sketch', 'OilPainting', 'Vintage', 'Vignette', 'Pixelate', 'HDR',
    'WarmGlow', 'CoolTone', 'FilmGrain', 'CrossProcess', 'Infrared', 'Bleach', 'Mirror',
    # Adjustments
    'Brightness', 'Contrast', 'Saturation', 'Blur', 'Sharpen', 'GaussianBlur',
    'Temperature', 'Denoise', 'MotionBlur', 'AutoLevel', 'Gamma',
    # Edge detection
    'EdgeDetection', 'Emboss', 'Sobel', 'Laplacian',
    # Color effects
    'Negative', 'DuoTone', 'ColorPop', 'LUT', 'ChannelSwap', 'ColorBalance'
]
