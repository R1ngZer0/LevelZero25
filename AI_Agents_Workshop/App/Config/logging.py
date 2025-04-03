"""
Logging configuration for the OT Interview Application.

This file configures the logging system for the application,
including log formats, levels, and output destinations.
"""

import logging
import logging.config
import os
from datetime import datetime
from pathlib import Path

from AI_Agents_Workshop.App.Config.settings import get_settings

settings = get_settings()

# Configure the base log directory
LOG_DIR = Path(__file__).parent.parent / "Logs"
LOG_DIR.mkdir(exist_ok=True)

# Create a timestamped log file
LOG_FILE = LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


def configure_logging():
    """
    Sets up logging for the application.
    """
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': str(LOG_FILE),
                'maxBytes': 10485760,  # 10 MB
                'backupCount': 5,
                'encoding': 'utf8',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True
            },
            'AI_Agents_Workshop': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False
            },
            'uvicorn': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }
    
    logging.config.dictConfig(logging_config)
    logging.info("Logging configured successfully") 