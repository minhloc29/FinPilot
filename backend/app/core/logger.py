import sys
from loguru import logger

logger.remove()

logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
)

logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    compression="zip",
    level="DEBUG",
)
