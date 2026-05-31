# Changelog

All notable changes to camKapture will be documented in this file.

## [2.0.0] - 2024-05-31

### 🎉 Major Release - Complete Rewrite

This release represents a complete transformation of camKapture into a production-grade desktop application.

### Added

#### Core Features

- Modern GUI with PySide6 (Qt) interface
- Live camera preview with real-time effect rendering
- Comprehensive settings dialog with resolution presets
- Persistent configuration management (JSON-based)
- Professional logging system with file and console output
- Robust error handling throughout the application
- Context manager support for camera resources

#### Effects System (20+ Effects)

- **Basic Effects**: Flip Vertical/Horizontal, Grayscale, Sepia, Invert, Rotations
- **Artistic Effects**: Cartoonify, Sketch, Oil Painting, Vintage, Vignette, Pixelate, HDR
- **Adjustments**: Brightness, Contrast, Saturation, Blur, Gaussian Blur, Sharpen, Temperature
- **Edge Detection**: Canny, Sobel, Emboss, Laplacian
- Adjustable parameters for all effects
- Effect enable/disable toggle functionality

#### GUI Components

- Camera preview panel with auto-scaling
- Controls panel with photo and video capture
- Effects panel with dropdown selection and parameter controls
- Settings dialog with camera and output configuration
- Status bar with real-time feedback
- Menu bar with file operations and help

#### Developer Features

- Modular architecture (core, effects, gui, utils)
- Comprehensive unit test suite
- Type hints throughout codebase
- Setuptools integration for package distribution
- Documentation (README, CONTRIBUTING, CHANGELOG)
- Development dependencies and test infrastructure

### Changed

- **Architecture**: Migrated from monolithic script to modular package structure
- **UI**: Replaced keyboard-only interface with production-grade Qt (PySide6) GUI
- **GUI Framework**: Migrated from tkinter to PySide6/Qt for better performance and native look
- **Threading**: Background camera capture in separate QThread for responsive UI
- **Effects**: Refactored from simple functions to extensible class-based system
- **Configuration**: Added persistent config with JSON storage
- **Video Format**: Changed from AVI/MJPEG to MP4 for better compatibility
- **Dependencies**: Updated to modern versions (OpenCV 4.5+, NumPy 1.19+, PySide6 6.0+)

### Technical Improvements

- Camera management with proper resource handling
- Video capture with pause/resume functionality
- Smart file naming with timestamps
- Multi-camera support infrastructure
- Resolution presets (720p, 1080p, 4K)
- FPS configuration
- Automatic directory creation

### Removed

- Keyboard-only interface (replaced by GUI)
- Hardcoded paths (now configurable)
- Global state (replaced with proper class structure)

## [1.0.0] - Previous Version

### Features

- Basic webcam capture
- Simple effects (flip vertical/horizontal)
- Keyboard-based controls
- Image and video capture
- Burst mode
- Timer mode

---

## Migration Guide (1.0 → 2.0)

### For Users

1. Install the new version: `pip install -r requirements.txt`
2. Run with: `python main.py`
3. Configure settings through the GUI (Menu → Settings)
4. Output directories can be customized in settings

### For Developers

1. Old effect functions are now classes inheriting from `Effect`
2. Configuration is managed through `Config` class
3. Camera access through `Camera` class with context manager support
4. GUI components are in separate modules for better organization

### Breaking Changes

- Keyboard shortcuts removed in favor of GUI buttons
- Old `camKapture.py` script replaced by `main.py` entry point
- Effects must now be instantiated as classes
- Configuration format changed to JSON

---

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
