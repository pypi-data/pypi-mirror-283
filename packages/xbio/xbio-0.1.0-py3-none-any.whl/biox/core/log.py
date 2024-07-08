import logging
from typing import Optional

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True, enable_link_path=False, show_path=False)
    ],
)


class LoggingMixin:
    _logger: Optional[logging.Logger] = None

    @classmethod
    def _create_logger_name(cls) -> str:
        return cls.__name__

    @property
    def log(self) -> logging.Logger:
        if self._logger is None:
            self._logger = self._get_logger(self._create_logger_name())
        return self._logger

    def _get_logger(self, name: str) -> logging.Logger:
        return logging.getLogger(name)
