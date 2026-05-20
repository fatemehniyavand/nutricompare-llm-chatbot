import sys

from loguru import logger

from nutricompare.infrastructure.config.settings import get_settings


def setup_logger():
    """
    Configure application logger.
    """

    settings = get_settings()

    logger.remove()

    log_level = "DEBUG" if settings.debug else "INFO"

    logger.add(
        sys.stderr,
        level=log_level,
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
    )

    return logger


app_logger = setup_logger()
