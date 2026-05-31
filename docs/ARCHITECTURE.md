# camKapture Architecture Documentation

## Overview

camKapture v2.0 is built with a modular, production-grade architecture that separates concerns and promotes maintainability, testability, and extensibility.

## Architecture Layers

```
┌─────────────────────────────────────────┐
│         GUI Layer (PySide6/Qt)          │
│  - Main Window (QMainWindow)            │
│  - Camera Thread (QThread)              │
│  - Qt Widgets & Layouts                 │
│  - Signal/Slot Event System             │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│          Application Layer              │
│  - Camera Management                    │
│  - Capture Operations                   │
│  - Effect Processing                    │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│           Core Layer                    │
│  - OpenCV Integration                   │
│  - File I/O Operations                  │
│  - Configuration Storage                │
└─────────────────────────────────────────┘
```

## Module Structure

### 1. Core Module (`camkapture/core/`)

**Purpose**: Low-level camera and capture operations

#### `camera.py`

- **Camera Class**: Manages webcam device
  - Device initialization and resource management
  - Resolution configuration
  - Context manager support (with/as)
  - Multi-camera detection
  - Error handling with custom exceptions

#### `capture.py`

- **CaptureManager**: Handles file operations
  - Image saving with timestamps
  - Video writer creation
  - Directory management
- **BurstCapture**: Burst mode logic
- **TimerCapture**: Countdown timer functionality

### 2. Effects Module (`camkapture/effects/`)

**Purpose**: Image processing and filters

#### Base Architecture

```python
Effect (Abstract Base Class)
├── apply(frame) → np.ndarray
├── set_param(key, value)
├── get_param(key)
└── toggle()
```

#### Effect Categories

**basic.py** - Simple transformations

- FlipVertical, FlipHorizontal
- Grayscale, Sepia, Invert
- Rotation (90°, 180°, 270°)

**artistic.py** - Creative effects

- Cartoonify (bilateral filter + edge detection)
- Sketch (pencil sketch algorithm)
- OilPainting (xphoto module)
- Vintage (sepia + desaturation)
- Vignette (radial gradient mask)
- Pixelate (downscale/upscale)
- HDR (detail enhancement)

**adjustments.py** - Parameter-based adjustments

- Brightness (additive adjustment)
- Contrast (multiplicative scaling)
- Saturation (HSV manipulation)
- Blur, GaussianBlur (kernel-based)
- Sharpen (convolution kernel)
- Temperature (color channel adjustment)

**edge.py** - Edge detection algorithms

- EdgeDetection (Canny)
- Sobel (gradient-based)
- Emboss (3D effect)
- Laplacian (second derivative)

### 3. GUI Module (`camkapture/gui/`)

**Purpose**: User interface components

#### `qt_main_window.py`

- **CameraThread Class**: Background camera capture thread
  - Runs in separate QThread
  - Emits frame_ready signal
  - Non-blocking camera operations
  - Effect application in thread

- **MainWindow Class**: Qt-based main window (QMainWindow)
  - Menu bar with QAction items
  - QLabel for video display
  - QPushButton controls
  - QComboBox for effects
  - Signal/slot event handling
  - Hardware-accelerated rendering
  - Thread-safe frame updates

### 4. Utils Module (`camkapture/utils/`)

**Purpose**: Cross-cutting utilities

#### `config.py`

- **Config Class**: Persistent configuration
  - JSON-based storage (~/.camkapture/config.json)
  - Nested key access (dot notation)
  - Default values
  - Merge custom with defaults

#### `logger.py`

- **setup_logging()**: Logging configuration
  - File + console handlers
  - Daily log rotation
  - Structured format

## Data Flow

### Photo Capture Flow

```
User Click → ControlsPanel.capture_photo()
           → MainWindow.capture_photo()
           → Camera.read()
           → Effect.apply() (if active)
           → CaptureManager.save_image()
           → File written to disk
           → Status update
```

### Video Recording Flow

```
Start: User Click → MainWindow.start_video_recording()
                  → CaptureManager.create_video_writer()
                  → is_recording = True

Loop:  MainWindow.update_frame()
     → Camera.read()
     → Effect.apply() (if active)
     → VideoWriter.write()
     → Display frame

Stop:  User Click → MainWindow.stop_video_recording()
                  → VideoWriter.release()
                  → Status update
```

### Effect Application Flow

```
User Selection → EffectsPanel._on_effect_selected()
               → Dynamic parameter UI created

User Adjust → Parameter sliders changed
            → Values updated in real-time

Apply → EffectsPanel._apply_effect()
      → Effect instance created with params
      → MainWindow.set_effect(effect)
      → Applied in update_frame() loop
```

## Configuration Management

### Config File Structure

```json
{
  "camera": {
    "device_id": 0,
    "width": 1280,
    "height": 720,
    "fps": 30
  },
  "output": {
    "image_dir": "~/Pictures/camKapture",
    "video_dir": "~/Videos/camKapture",
    "image_format": "jpg",
    "video_format": "mp4"
  },
  "ui": {
    "window_width": 1024,
    "window_height": 768
  },
  "capture": {
    "burst_interval": 10,
    "timer_seconds": 10
  }
}
```

## Error Handling Strategy

1. **Camera Errors**: Custom `CameraError` exception
2. **File I/O**: Try-catch with logging
3. **Effect Failures**: Graceful fallback, log error
4. **GUI Exceptions**: Show error dialog to user
5. **Resource Cleanup**: Context managers, finally blocks

## Testing Strategy

- **Unit Tests**: Core functionality (camera, effects, config)
- **Mock Objects**: For camera hardware in tests
- **Test Coverage**: Effects, configuration, error paths
- **Integration**: GUI components tested manually

## Extension Points

### Adding New Effects

1. Create class inheriting from `Effect`
2. Implement `apply(frame)` method
3. Add to appropriate module
4. Export in `__init__.py`
5. Register in EffectsPanel

### Adding New Capture Modes

1. Create handler in `capture.py`
2. Add UI in `controls_panel.py`
3. Integrate in `main_window.py`

### Adding New Settings

1. Update default config in `config.py`
2. Add UI in `settings_dialog.py`
3. Use in relevant modules

## Performance Considerations

- Frame processing: ~30 FPS target
- Effect caching: No caching (real-time)
- Memory: Single frame buffer
- Thread safety: Multi-threaded (Qt QThread for camera)

## Future Improvements

- Effect preview thumbnails
- Effect stacking/composition
- GPU acceleration for effects
- Plugin system for custom effects
- Settings dialog with Qt
