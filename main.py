#!/usr/bin/env python3
"""
camKapture - Professional Webcam Application
Main entry point
"""

import sys
import logging
from camkapture.utils.logger import setup_logging
from camkapture.utils.config import Config
from camkapture.gui.qt_main_window import run_app


def main():
    """Main entry point."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting camKapture v2.0.0")

        # Load configuration
        config = Config()

        # Run Qt application
        sys.exit(run_app(config))

    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
