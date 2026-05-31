"""Qt-based main window - production-grade GUI."""
import sys
import logging
from typing import Optional
import numpy as np
import cv2

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QSlider, QGroupBox, QMessageBox,
    QFileDialog, QStatusBar, QMenuBar, QMenu
)
from PySide6.QtCore import QTimer, Qt, Signal, QThread
from PySide6.QtGui import QImage, QPixmap, QAction

from ..core.camera import Camera, CameraError
from ..core.capture import CaptureManager
from ..utils.config import Config
from ..effects.base import Effect

logger = logging.getLogger(__name__)


class CameraThread(QThread):
    """Thread for camera capture to keep UI responsive."""
    frame_ready = Signal(np.ndarray)
    
    def __init__(self, camera: Camera):
        super().__init__()
        self.camera = camera
        self.running = True
        self.current_effect = None
        
    def run(self):
        """Capture frames in background thread."""
        while self.running:
            success, frame = self.camera.read()
            if success:
                # Apply effect if set
                if self.current_effect is not None:
                    try:
                        frame = self.current_effect(frame)
                    except Exception as e:
                        logger.error(f"Effect error: {e}")
                
                self.frame_ready.emit(frame)
            
            self.msleep(33)  # ~30 FPS
    
    def stop(self):
        """Stop the thread."""
        self.running = False
        self.wait()


class MainWindow(QMainWindow):
    """Main application window with Qt."""
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.camera: Optional[Camera] = None
        self.camera_thread: Optional[CameraThread] = None
        self.capture_manager = CaptureManager(
            config.get('output.image_dir'),
            config.get('output.video_dir')
        )
        
        # State
        self.is_recording = False
        self.video_writer = None
        self.video_path = None
        self.current_frame = None
        
        self.setup_ui()
        self.setup_camera()
        
    def setup_ui(self):
        """Setup user interface."""
        self.setWindowTitle("camKapture - Professional Webcam Application")
        self.setMinimumSize(1024, 768)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left side - Camera preview
        preview_layout = QVBoxLayout()
        
        self.video_label = QLabel()
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setStyleSheet("background-color: black; border: 2px solid #555;")
        self.video_label.setScaledContents(False)
        self.video_label.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.video_label)
        
        main_layout.addLayout(preview_layout, 3)
        
        # Right side - Controls
        controls_layout = QVBoxLayout()
        
        # Capture buttons
        capture_group = QGroupBox("Capture")
        capture_layout = QVBoxLayout()
        
        self.photo_btn = QPushButton("📷 Capture Photo")
        self.photo_btn.setMinimumHeight(40)
        self.photo_btn.clicked.connect(self.capture_photo)
        capture_layout.addWidget(self.photo_btn)
        
        self.record_btn = QPushButton("⏺ Start Recording")
        self.record_btn.setMinimumHeight(40)
        self.record_btn.clicked.connect(self.toggle_recording)
        capture_layout.addWidget(self.record_btn)
        
        capture_group.setLayout(capture_layout)
        controls_layout.addWidget(capture_group)
        
        # Effects
        effects_group = QGroupBox("Effects")
        effects_layout = QVBoxLayout()
        
        QLabel("Select Effect:")
        self.effects_combo = QComboBox()
        self.effects_combo.addItems([
            "None",
            # Basic
            "Grayscale",
            "Sepia",
            "Black & White",
            "Invert",
            "Posterize",
            "Solarize",
            # Artistic
            "Cartoonify",
            "Sketch",
            "Vintage",
            "HDR",
            "Warm Glow",
            "Cool Tone",
            "Film Grain",
            "Cross Process",
            "Infrared",
            "Bleach Bypass",
            "Vignette",
            "Pixelate",
            # Adjustments
            "Blur",
            "Sharpen",
            "Brightness",
            "Contrast",
            "Denoise",
            "Auto Level",
            # Edge
            "Edge Detection",
            "Emboss",
            "Sobel",
            # Color
            "Negative",
            "Duo Tone",
            "Color Pop",
            "Color Balance"
        ])
        self.effects_combo.currentTextChanged.connect(self.apply_effect)
        effects_layout.addWidget(self.effects_combo)
        
        effects_group.setLayout(effects_layout)
        controls_layout.addWidget(effects_group)
        
        controls_layout.addStretch()
        
        main_layout.addLayout(controls_layout, 1)
        
        # Menu bar
        self.create_menu_bar()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_folder_action = QAction("Open Output Folder", self)
        open_folder_action.triggered.connect(self.open_output_folder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_camera(self):
        """Initialize camera."""
        try:
            device_id = self.config.get('camera.device_id', 0)
            width = self.config.get('camera.width', 1280)
            height = self.config.get('camera.height', 720)

            self.camera = Camera(device_id, width, height)
            self.camera.open()

            # Start camera thread
            self.camera_thread = CameraThread(self.camera)
            self.camera_thread.frame_ready.connect(self.update_frame)
            self.camera_thread.start()

            self.status_bar.showMessage(f"Camera connected ({width}x{height})")
            logger.info("Camera initialized successfully")

        except CameraError as e:
            logger.error(f"Camera error: {e}")
            QMessageBox.critical(self, "Camera Error", str(e))
            self.status_bar.showMessage("Camera: Error")

    def update_frame(self, frame: np.ndarray):
        """Update video display with new frame."""
        self.current_frame = frame.copy()

        # Record if active
        if self.is_recording and self.video_writer is not None:
            self.video_writer.write(frame)

        # Convert to Qt format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Scale to fit label
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            self.video_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.video_label.setPixmap(scaled_pixmap)

    def capture_photo(self):
        """Capture a photo."""
        if self.current_frame is None:
            QMessageBox.warning(self, "No Frame", "No camera frame available")
            return

        try:
            filepath = self.capture_manager.save_image(self.current_frame)
            self.status_bar.showMessage(f"Photo saved: {filepath}")
            logger.info(f"Photo captured: {filepath}")

            # Brief flash effect
            QTimer.singleShot(100, lambda: self.status_bar.showMessage("Ready"))

        except Exception as e:
            logger.error(f"Failed to save photo: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save photo: {e}")

    def toggle_recording(self):
        """Toggle video recording."""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Start video recording."""
        if self.camera is None:
            return

        try:
            width, height = self.camera.get_resolution()
            fps = self.config.get('camera.fps', 30)

            self.video_writer, self.video_path = self.capture_manager.create_video_writer(
                width, height, fps
            )
            self.is_recording = True
            self.record_btn.setText("⏹ Stop Recording")
            self.record_btn.setStyleSheet("background-color: #ff4444;")
            self.status_bar.showMessage("Recording...")
            logger.info("Video recording started")

        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            QMessageBox.critical(self, "Recording Error", str(e))

    def stop_recording(self):
        """Stop video recording."""
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

        self.is_recording = False
        self.record_btn.setText("⏺ Start Recording")
        self.record_btn.setStyleSheet("")
        self.status_bar.showMessage(f"Video saved: {self.video_path}")
        logger.info(f"Video recording stopped: {self.video_path}")

    def apply_effect(self, effect_name: str):
        """Apply selected effect."""
        if not self.camera_thread:
            return

        if effect_name == "None":
            self.camera_thread.current_effect = None
            self.status_bar.showMessage("Effect removed")
            return

        # Import effects
        from ..effects import (
            # Basic
            Grayscale, Sepia, Invert, BlackAndWhite, Posterize, Solarize,
            # Artistic
            Cartoonify, Sketch, Vintage, HDR, WarmGlow, CoolTone, FilmGrain,
            CrossProcess, Infrared, Bleach, Vignette, Pixelate,
            # Adjustments
            Blur, Sharpen, Brightness, Contrast, Denoise, AutoLevel,
            # Edge
            EdgeDetection, Emboss, Sobel,
            # Color
            Negative, DuoTone, ColorPop, ColorBalance
        )

        effect_map = {
            # Basic
            "Grayscale": Grayscale(),
            "Sepia": Sepia(intensity=0.7),
            "Black & White": BlackAndWhite(threshold=128),
            "Invert": Invert(),
            "Posterize": Posterize(levels=4),
            "Solarize": Solarize(threshold=128),
            # Artistic
            "Cartoonify": Cartoonify(),
            "Sketch": Sketch(),
            "Vintage": Vintage(intensity=0.7),
            "HDR": HDR(),
            "Warm Glow": WarmGlow(intensity=0.5),
            "Cool Tone": CoolTone(intensity=0.6),
            "Film Grain": FilmGrain(intensity=0.1),
            "Cross Process": CrossProcess(),
            "Infrared": Infrared(),
            "Bleach Bypass": Bleach(intensity=0.7),
            "Vignette": Vignette(intensity=0.5),
            "Pixelate": Pixelate(pixel_size=10),
            # Adjustments
            "Blur": Blur(kernel_size=9),
            "Sharpen": Sharpen(intensity=1.0),
            "Brightness": Brightness(value=30),
            "Contrast": Contrast(value=1.3),
            "Denoise": Denoise(strength=10),
            "Auto Level": AutoLevel(),
            # Edge
            "Edge Detection": EdgeDetection(),
            "Emboss": Emboss(intensity=1.0),
            "Sobel": Sobel(),
            # Color
            "Negative": Negative(),
            "Duo Tone": DuoTone(),
            "Color Pop": ColorPop(hue_target=0, hue_range=30),
            "Color Balance": ColorBalance()
        }

        if effect_name in effect_map:
            self.camera_thread.current_effect = effect_map[effect_name]
            self.status_bar.showMessage(f"Effect applied: {effect_name}")
            logger.info(f"Effect applied: {effect_name}")

    def open_output_folder(self):
        """Open output folder."""
        import subprocess
        import platform

        folder = self.config.get('output.image_dir')
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', folder])
        elif platform.system() == 'Windows':
            subprocess.run(['explorer', folder])
        else:  # Linux
            subprocess.run(['xdg-open', folder])

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About camKapture",
            "camKapture v2.0.0\n\n"
            "Professional Webcam Application\n\n"
            "Built with PySide6 and OpenCV\n\n"
            "© 2024 camKapture Contributors\n"
            "Licensed under GPL v3"
        )

    def closeEvent(self, event):
        """Handle window close event."""
        if self.is_recording:
            self.stop_recording()

        if self.camera_thread:
            self.camera_thread.stop()

        if self.camera:
            self.camera.release()

        cv2.destroyAllWindows()
        event.accept()


def run_app(config: Config):
    """Run the Qt application."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look

    window = MainWindow(config)
    window.show()

    return app.exec()
