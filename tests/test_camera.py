"""Tests for camera module."""
import unittest
from unittest.mock import Mock, patch
import cv2

from camkapture.core.camera import Camera, CameraError


class TestCamera(unittest.TestCase):
    """Test Camera class."""
    
    @patch('cv2.VideoCapture')
    def test_camera_initialization(self, mock_capture):
        """Test camera initialization."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_capture.return_value = mock_cap
        
        camera = Camera(device_id=0, width=1280, height=720)
        camera.open()
        
        self.assertTrue(camera.is_open)
        mock_cap.set.assert_any_call(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        mock_cap.set.assert_any_call(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    @patch('cv2.VideoCapture')
    def test_camera_open_failure(self, mock_capture):
        """Test camera open failure."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = False
        mock_capture.return_value = mock_cap
        
        camera = Camera(device_id=0)
        
        with self.assertRaises(CameraError):
            camera.open()
    
    @patch('cv2.VideoCapture')
    def test_camera_read(self, mock_capture):
        """Test reading frames."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, None)
        mock_capture.return_value = mock_cap
        
        camera = Camera(device_id=0)
        camera.open()
        
        success, frame = camera.read()
        self.assertTrue(success)
    
    @patch('cv2.VideoCapture')
    def test_camera_release(self, mock_capture):
        """Test camera release."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_capture.return_value = mock_cap
        
        camera = Camera(device_id=0)
        camera.open()
        camera.release()
        
        self.assertFalse(camera.is_open)
        mock_cap.release.assert_called_once()
    
    @patch('cv2.VideoCapture')
    def test_camera_context_manager(self, mock_capture):
        """Test camera as context manager."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_capture.return_value = mock_cap
        
        with Camera(device_id=0) as camera:
            self.assertTrue(camera.is_open)
        
        mock_cap.release.assert_called_once()


if __name__ == '__main__':
    unittest.main()
