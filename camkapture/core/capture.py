"""Image and video capture functionality."""
import cv2
import os
import logging
from datetime import datetime
from typing import Optional, Callable, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class CaptureManager:
    """Manages image and video capture operations."""
    
    def __init__(self, img_directory: str, vid_directory: str):
        """
        Initialize capture manager.
        
        Args:
            img_directory: Directory to save images
            vid_directory: Directory to save videos
        """
        self.img_directory = img_directory
        self.vid_directory = vid_directory
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Create output directories if they don't exist."""
        os.makedirs(self.img_directory, exist_ok=True)
        os.makedirs(self.vid_directory, exist_ok=True)
        logger.info(f"Output directories: {self.img_directory}, {self.vid_directory}")
    
    def save_image(self, frame: np.ndarray, prefix: str = "image") -> str:
        """
        Save an image frame.
        
        Args:
            frame: Image frame to save
            prefix: Filename prefix
            
        Returns:
            Path to saved image
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{prefix}_{timestamp}.jpg"
        filepath = os.path.join(self.img_directory, filename)
        
        try:
            cv2.imwrite(filepath, frame)
            logger.info(f"Image saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save image: {e}")
            raise
    
    def create_video_writer(self, width: int, height: int, fps: int = 30, 
                           prefix: str = "video") -> Tuple[cv2.VideoWriter, str]:
        """
        Create a video writer.
        
        Args:
            width: Frame width
            height: Frame height
            fps: Frames per second
            prefix: Filename prefix
            
        Returns:
            Tuple of (VideoWriter, filepath)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.mp4"
        filepath = os.path.join(self.vid_directory, filename)
        
        # Use H264 codec for better compatibility
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
        
        if not writer.isOpened():
            logger.error("Failed to create video writer")
            raise Exception("Cannot create video writer")
        
        logger.info(f"Video writer created: {filepath}")
        return writer, filepath


class BurstCapture:
    """Handles burst mode capture."""
    
    def __init__(self, capture_manager: CaptureManager, interval: int = 10):
        """
        Initialize burst capture.
        
        Args:
            capture_manager: CaptureManager instance
            interval: Frame interval between captures
        """
        self.capture_manager = capture_manager
        self.interval = interval
        self.frame_count = 0
        
    def should_capture(self) -> bool:
        """Check if current frame should be captured."""
        self.frame_count += 1
        if self.frame_count >= self.interval:
            self.frame_count = 0
            return True
        return False
    
    def reset(self):
        """Reset frame counter."""
        self.frame_count = 0


class TimerCapture:
    """Handles timer-based capture with countdown."""
    
    def __init__(self, countdown_seconds: int = 10):
        """
        Initialize timer capture.
        
        Args:
            countdown_seconds: Countdown duration
        """
        self.countdown_seconds = countdown_seconds
        self.frames_remaining = countdown_seconds * 10  # Assuming ~10 fps for countdown
        
    def get_countdown_text(self) -> Optional[str]:
        """
        Get countdown text to display.
        
        Returns:
            Countdown text or None if countdown complete
        """
        seconds = self.frames_remaining // 10
        if seconds > 0:
            self.frames_remaining -= 1
            return str(seconds)
        return None
    
    def is_complete(self) -> bool:
        """Check if countdown is complete."""
        return self.frames_remaining <= 0
    
    def reset(self, countdown_seconds: Optional[int] = None):
        """Reset timer."""
        if countdown_seconds is not None:
            self.countdown_seconds = countdown_seconds
        self.frames_remaining = self.countdown_seconds * 10
