"""Tests for effects module."""
import unittest
import numpy as np
import cv2

from camkapture.effects.basic import (
    FlipVertical, FlipHorizontal, Grayscale, Sepia, Invert
)
from camkapture.effects.adjustments import (
    Brightness, Contrast, Blur, Sharpen
)
from camkapture.effects.artistic import (
    Cartoonify, Vintage, Vignette
)
from camkapture.effects.edge import (
    EdgeDetection, Sobel, Emboss
)


class TestEffects(unittest.TestCase):
    """Test image effects."""
    
    def setUp(self):
        """Create test image."""
        # Create a simple test image (100x100 RGB)
        self.test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    def test_flip_vertical(self):
        """Test vertical flip effect."""
        effect = FlipVertical()
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
        self.assertIsInstance(result, np.ndarray)
    
    def test_flip_horizontal(self):
        """Test horizontal flip effect."""
        effect = FlipHorizontal()
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_grayscale(self):
        """Test grayscale effect."""
        effect = Grayscale()
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_sepia(self):
        """Test sepia effect."""
        effect = Sepia(intensity=0.7)
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
        self.assertEqual(result.dtype, np.uint8)
    
    def test_invert(self):
        """Test invert effect."""
        effect = Invert()
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_brightness(self):
        """Test brightness adjustment."""
        effect = Brightness(value=50)
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_contrast(self):
        """Test contrast adjustment."""
        effect = Contrast(value=1.5)
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_blur(self):
        """Test blur effect."""
        effect = Blur(kernel_size=5)
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_sharpen(self):
        """Test sharpen effect."""
        effect = Sharpen(intensity=1.0)
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
        self.assertEqual(result.dtype, np.uint8)
    
    def test_vintage(self):
        """Test vintage effect."""
        effect = Vintage(intensity=0.7)
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_vignette(self):
        """Test vignette effect."""
        effect = Vignette(intensity=0.5)
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_edge_detection(self):
        """Test edge detection."""
        effect = EdgeDetection(threshold1=100, threshold2=200)
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_sobel(self):
        """Test Sobel edge detection."""
        effect = Sobel()
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_emboss(self):
        """Test emboss effect."""
        effect = Emboss(intensity=1.0)
        result = effect.apply(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_effect_toggle(self):
        """Test effect enable/disable."""
        effect = Grayscale()
        self.assertTrue(effect.enabled)
        
        effect.toggle()
        self.assertFalse(effect.enabled)
        
        # When disabled, should return original image
        result = effect(self.test_image)
        np.testing.assert_array_equal(result, self.test_image)
    
    def test_effect_parameters(self):
        """Test effect parameter management."""
        effect = Brightness(value=50)
        self.assertEqual(effect.get_param('value'), 50)
        
        effect.set_param('value', 100)
        self.assertEqual(effect.get_param('value'), 100)


if __name__ == '__main__':
    unittest.main()
