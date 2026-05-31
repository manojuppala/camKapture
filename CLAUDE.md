# Claude Development Guide for camKapture

This document provides comprehensive guidance for AI assistants (like Claude) working on the camKapture project.

## Project Overview

**camKapture v2.0** is a production-grade desktop webcam application built with:
- **Language**: Python 3.7+
- **GUI Framework**: PySide6 (Qt for Python)
- **Computer Vision**: OpenCV
- **Architecture**: Modular, class-based design

## Project Structure

```
camKapture/
├── camkapture/              # Main package
│   ├── __init__.py         # Package initialization
│   ├── core/               # Core functionality
│   │   ├── camera.py       # Camera management with error handling
│   │   └── capture.py      # Image/video capture operations
│   ├── effects/            # Image effects library (20+ effects)
│   │   ├── base.py         # Abstract Effect base class
│   │   ├── basic.py        # Basic transformations (flip, grayscale, etc.)
│   │   ├── artistic.py     # Artistic effects (cartoon, sketch, vintage)
│   │   ├── adjustments.py  # Adjustments (brightness, blur, sharpen)
│   │   └── edge.py         # Edge detection (Canny, Sobel, Emboss)
│   ├── gui/                # GUI layer (Qt-based)
│   │   └── qt_main_window.py  # Main window with QThread camera capture
│   └── utils/              # Utilities
│       ├── config.py       # JSON configuration management
│       └── logger.py       # Logging setup
├── tests/                  # Unit tests
│   ├── test_camera.py
│   ├── test_config.py
│   └── test_effects.py
├── docs/                   # Documentation
│   └── ARCHITECTURE.md
├── main.py                 # Application entry point
├── setup.py                # Package distribution
└── requirements.txt        # Dependencies
```

## Key Design Principles

### 1. Modular Architecture
- **Separation of Concerns**: Core, GUI, Effects, Utils are independent
- **Single Responsibility**: Each class has one clear purpose
- **Dependency Injection**: Config and dependencies passed to constructors

### 2. Error Handling
- Custom exceptions (e.g., `CameraError`)
- Try-catch blocks with logging
- Graceful fallbacks for optional features
- User-friendly error messages via Qt dialogs

### 3. Threading Model
- **Main Thread**: Qt GUI event loop
- **CameraThread**: Background QThread for camera capture
- **Signal/Slot**: Thread-safe communication (frame_ready signal)
- Never block the main thread

### 4. Configuration Management
- JSON-based config at `~/.camkapture/config.json`
- Dot notation for nested access: `config.get('camera.width')`
- Automatic defaults and merging
- Persistent across sessions

## Code Standards

### Python Style
```python
# Use type hints
def capture_photo(self, frame: np.ndarray) -> str:
    """Docstring with Args and Returns."""
    pass

# Use context managers
with Camera(device_id=0) as camera:
    frame = camera.read()

# Use logging, not print
logger.info("Camera initialized")
logger.error(f"Failed: {e}")

# Use descriptive names
is_recording = False  # Good
rec = False           # Bad
```

### Qt Best Practices
```python
# Use signals for thread communication
class CameraThread(QThread):
    frame_ready = Signal(np.ndarray)
    
    def run(self):
        self.frame_ready.emit(frame)

# Connect slots
self.camera_thread.frame_ready.connect(self.update_frame)

# Use Qt layouts, not absolute positioning
layout = QHBoxLayout()
layout.addWidget(button)

# Clean up resources
def closeEvent(self, event):
    self.cleanup()
    event.accept()
```

### Effect Development
```python
from .base import Effect

class MyEffect(Effect):
    def __init__(self, intensity: float = 1.0):
        super().__init__("My Effect", intensity=intensity)
    
    def apply(self, frame: np.ndarray) -> np.ndarray:
        # Process frame
        result = cv2.someFunction(frame)
        return result
```

## Common Tasks

### Adding a New Effect

1. **Create effect class** in appropriate module:
   ```python
   # camkapture/effects/artistic.py
   class Watercolor(Effect):
       def __init__(self):
           super().__init__("Watercolor")
       
       def apply(self, frame: np.ndarray) -> np.ndarray:
           result = cv2.stylization(frame, sigma_s=60, sigma_r=0.6)
           return result
   ```

2. **Export in __init__.py**:
   ```python
   # camkapture/effects/__init__.py
   from .artistic import (..., Watercolor)
   __all__ = [..., 'Watercolor']
   ```

3. **Register in GUI**:
   ```python
   # camkapture/gui/qt_main_window.py
   effect_map = {
       ...
       "Watercolor": Watercolor()
   }
   
   self.effects_combo.addItems([..., "Watercolor"])
   ```

4. **Add test**:
   ```python
   # tests/test_effects.py
   def test_watercolor(self):
       effect = Watercolor()
       result = effect.apply(self.test_image)
       self.assertEqual(result.shape, self.test_image.shape)
   ```

### Modifying Camera Behavior

**Camera class** (`core/camera.py`):
- Use context manager pattern
- Handle errors with CameraError
- Log all operations

```python
try:
    with Camera(device_id=0) as camera:
        success, frame = camera.read()
except CameraError as e:
    logger.error(f"Camera failed: {e}")
```

### Adding Configuration Options

1. **Update default config**:
   ```python
   # camkapture/utils/config.py
   DEFAULT_CONFIG = {
       "new_feature": {
           "enabled": True,
           "value": 42
       }
   }
   ```

2. **Access in code**:
   ```python
   enabled = self.config.get('new_feature.enabled', True)
   ```

## Testing Guidelines

### Unit Tests
```python
import unittest
from camkapture.core.camera import Camera

class TestCamera(unittest.TestCase):
    def setUp(self):
        """Setup before each test."""
        self.test_data = create_test_data()
    
    def test_camera_init(self):
        """Test camera initialization."""
        camera = Camera(device_id=0)
        self.assertIsNotNone(camera)
    
    def tearDown(self):
        """Cleanup after each test."""
        cleanup_test_data()
```

### Mock External Dependencies
```python
from unittest.mock import Mock, patch

@patch('cv2.VideoCapture')
def test_camera_with_mock(self, mock_capture):
    mock_cap = Mock()
    mock_cap.isOpened.return_value = True
    mock_capture.return_value = mock_cap
    # Test code here
```

### Run Tests
```bash
# All tests
python -m pytest tests/

# Specific test
python -m pytest tests/test_camera.py::TestCamera::test_camera_init

# With coverage
python -m pytest --cov=camkapture tests/
```

## Debugging

### Logging
Logs are written to `~/.camkapture/logs/camkapture_YYYYMMDD.log`

```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Detailed info")
logger.info("Normal operation")
logger.warning("Warning message")
logger.error("Error occurred")
logger.exception("Exception with traceback")
```

### Common Issues

**Issue**: Black screen in GUI
- **Cause**: Camera not capturing or display not updating
- **Debug**: Check `self.camera.is_open`, verify `update_frame()` is called
- **Solution**: Ensure QThread is running and signal is connected

**Issue**: Effect not applying
- **Cause**: Effect not registered or error in apply()
- **Debug**: Add logging in `apply()` method
- **Solution**: Check effect_map in qt_main_window.py

**Issue**: Import errors
- **Cause**: Circular imports or missing __init__.py
- **Debug**: Check import order and __all__ exports
- **Solution**: Use relative imports, add to __init__.py

## Performance Optimization

### Frame Processing
```python
# Good: Process in background thread
class CameraThread(QThread):
    def run(self):
        frame = self.camera.read()
        if self.effect:
            frame = self.effect.apply(frame)  # Done in thread
        self.frame_ready.emit(frame)

# Bad: Process in main thread (blocks GUI)
def update_frame(self, frame):
    frame = self.effect.apply(frame)  # Blocks UI!
```

### Memory Management
```python
# Good: Clean up resources
def closeEvent(self, event):
    if self.video_writer:
        self.video_writer.release()
    if self.camera:
        self.camera.release()

# Good: Use context managers
with Camera() as cam:
    # Auto cleanup
    pass
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-effect

# Make changes, test thoroughly
python -m pytest tests/

# Commit with descriptive message
git commit -m "Add watercolor effect with intensity parameter"

# Push and create PR
git push origin feature/new-effect
```

## Dependencies

**Core**:
- `opencv-python >= 4.5.0` - Computer vision
- `numpy >= 1.19.0, < 2.0.0` - Array operations
- `PySide6 >= 6.0.0` - Qt GUI framework

**Development**:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting

## Resources

- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## Quick Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Run tests
python -m pytest tests/

# Install as package
pip install -e .

# Clean cache
rm -rf **/__pycache__

# Check code
python -m pylint camkapture/

# Format code
python -m black camkapture/
```

---

**Remember**: Production-grade code means robust error handling, comprehensive logging, proper threading, and thorough testing. Always test changes before committing!
