"""Logging configuration."""
import logging
import os
from datetime import datetime
from typing import Optional


def setup_logging(log_dir: Optional[str] = None, level: int = logging.INFO):
    """
    Setup application logging.
    
    Args:
        log_dir: Directory for log files (default: ~/.camkapture/logs)
        level: Logging level
    """
    if log_dir is None:
        log_dir = os.path.join(os.path.expanduser("~"), ".camkapture", "logs")
    
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log filename with timestamp
    log_file = os.path.join(log_dir, f"camkapture_{datetime.now().strftime('%Y%m%d')}.log")
    
    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging initialized")
