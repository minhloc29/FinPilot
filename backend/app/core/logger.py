"""
Logging configuration
"""
import logging
import sys
from loguru import logger

# Remove default handler
logger.remove()

# Add custom handler
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# Add file handler
logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    compression="zip",
    level="DEBUG"
)
