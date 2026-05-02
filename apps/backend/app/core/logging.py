import logging
import sys
from typing import Any

from loguru import logger


def setup_logging() -> None:
    from asgi_correlation_id.context import correlation_id

    def correlation_id_filter(record: dict[str, Any]) -> bool:
        record["extra"]["correlation_id"] = correlation_id.get("-")
        return True

    logger.remove()
    fmt = "{level}: \t  {time:YYYY-MM-DD HH:mm:ss} {name}:{line} [{extra[correlation_id]}] - {message}"
    logger.add(sys.stdout, format=fmt, level=logging.DEBUG, filter=correlation_id_filter)  # type: ignore
    logger.add(sys.stderr, format=fmt, level=logging.ERROR, filter=correlation_id_filter)  # type: ignore
