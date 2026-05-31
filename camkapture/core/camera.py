"""Camera management with error handling and device selection."""
import cv2
import logging
from typing import Optional, Tuple, List

logger = logging.getLogger(__name__)


class CameraError(Exception):
    """Custom exception for camera-related errors."""
    pass


class Camera:
    """Manages webcam capture with robust error handling."""
    
    def __init__(self, device_id: int = 0, width: int = 1280, height: int = 720):
        """
        Initialize camera capture.
        
        Args:
            device_id: Camera device ID (default 0 for primary camera)
            width: Frame width in pixels
            height: Frame height in pixels
        """
        self.device_id = device_id
        self.width = width
        self.height = height
        self.cap: Optional[cv2.VideoCapture] = None
        self._is_open = False
        
    def open(self) -> bool:
        """
        Open camera connection.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.device_id)
            if not self.cap.isOpened():
                raise CameraError(f"Cannot open camera {self.device_id}")
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self._is_open = True
            logger.info(f"Camera {self.device_id} opened successfully at {self.width}x{self.height}")
            return True
        except Exception as e:
            logger.error(f"Failed to open camera: {e}")
            raise CameraError(f"Camera initialization failed: {e}")
    
    def read(self) -> Tuple[bool, Optional[any]]:
        """
        Read a frame from the camera.
        
        Returns:
            Tuple of (success, frame)
        """
        if not self._is_open or self.cap is None:
            return False, None
        return self.cap.read()
    
    def release(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            self._is_open = False
            logger.info(f"Camera {self.device_id} released")
    
    @property
    def is_open(self) -> bool:
        """Check if camera is open."""
        return self._is_open
    
    @staticmethod
    def list_available_cameras(max_cameras: int = 5) -> List[int]:
        """
        Find available camera devices.
        
        Args:
            max_cameras: Maximum number of cameras to check
            
        Returns:
            List of available camera IDs
        """
        available = []
        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available.append(i)
                cap.release()
        return available
    
    def get_resolution(self) -> Tuple[int, int]:
        """Get current camera resolution."""
        if self.cap is None:
            return (0, 0)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)
    
    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release()
