# Contributing to camKapture

Thank you for your interest in contributing to camKapture! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/camKapture.git`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Install development dependencies: `pip install pytest pytest-cov`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write/update tests as needed
4. Run tests: `python -m pytest tests/`
5. Commit your changes: `git commit -m "Description of changes"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Add docstrings to classes and methods
- Keep functions focused and modular
- Use type hints where appropriate

## Adding New Effects

To add a new image effect:

1. Create your effect class in the appropriate module:
   - Basic transformations → `camkapture/effects/basic.py`
   - Artistic effects → `camkapture/effects/artistic.py`
   - Adjustments → `camkapture/effects/adjustments.py`
   - Edge detection → `camkapture/effects/edge.py`

2. Inherit from the `Effect` base class:

```python
from .base import Effect

class MyNewEffect(Effect):
    def __init__(self, param1=default_value):
        super().__init__("My New Effect", param1=param1)

    def apply(self, frame):
        # Your effect implementation
        processed = process_frame(frame)
        return processed
```

3. Add to exports in `camkapture/effects/__init__.py`

4. Register in `camkapture/gui/qt_main_window.py` in the `effect_map` dictionary

5. Add tests in `tests/test_effects.py`

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Aim for good code coverage

Run tests:

```bash
python -m pytest tests/
```

Run with coverage:

```bash
python -m pytest --cov=camkapture tests/
```

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed
- Keep PRs focused on a single feature/fix

## Bug Reports

When reporting bugs, please include:

- Operating system and version
- Python version
- camKapture version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs if applicable

## Feature Requests

We welcome feature requests! Please:

- Check if the feature already exists
- Provide a clear use case
- Describe the expected behavior
- Consider if it fits the project's scope

## Questions?

Feel free to open an issue for questions or discussions.

Thank you for contributing to camKapture! 🎉
