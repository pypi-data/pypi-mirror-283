import logging
import os

from typing import Optional

from pyhectiqlab.settings import getenv

STEP_HANDLER_NAME = "hectiq-lab-step-handler"

hectiqlab_logger: logging.Logger = logging.getLogger("hectiqlab")
httpx_logger: logging.Logger = logging.getLogger("httpx")


def setup_logging() -> None:
    env = getenv("HECTIQLAB_LOG_LEVEL", "warning").lower()
    logging.basicConfig(
        format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    if env == "info":
        hectiqlab_logger.setLevel(logging.INFO)
        httpx_logger.setLevel(logging.INFO)
    elif env == "warning":
        hectiqlab_logger.setLevel(logging.WARNING)
        httpx_logger.setLevel(logging.WARNING)
    else:
        hectiqlab_logger.setLevel(logging.DEBUG)
        httpx_logger.setLevel(logging.DEBUG)


def stream_log(
    on_dump: callable,
    logger_name: Optional[str] = None,
    log_level: Optional[int] = logging.INFO,
    capacity: Optional[int] = 1000,
) -> None:
    """
    Stream logs to a memory handler.

    Args:
        on_dump (callable): The function to call when the buffer is flushed. Should take a list of strings as argument.
        logger_name (str): The logger name. If None, the root logger is used.
        log_level (int): The log level.
        capacity (int): The buffer capacity.
    """
    handler = MemoryHandler(name=STEP_HANDLER_NAME, capacity=capacity, target=on_dump)  # Flush every 5000 lines
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root = logging.getLogger(logger_name)
    root.addHandler(handler)
    root.setLevel(log_level)
    handler.setLevel(log_level)


def get_handler(logger_name: Optional[str] = None) -> Optional[logging.Handler]:
    """
    Get a handler by name from the logger.

    Args:
        logger_name (str): The logger name. If None, the root logger is used.

    Returns:
        logging.Handler: The handler with the given name or None if not found.
    """
    logger = logging.getLogger(logger_name)
    for handler in logger.handlers:
        if not hasattr(handler, "name"):
            continue
        if handler.name == STEP_HANDLER_NAME:
            return handler
    return None


class MemoryHandler(logging.StreamHandler):
    """
    A handler class which buffers logging records in memory, periodically
    flushing them to a target handler. Flushing occurs whenever the buffer
    is full, or when an event of a certain severity or greater is seen.

    Almost a copy of the standard library MemoryHandler, except that it
    has a formatter.
    """

    def __init__(
        self,
        name: str,
        capacity: int,
        flushLevel: int = logging.CRITICAL,
        target: callable = None,
        format: Optional[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        flushOnClose: Optional[bool] = True,
    ):
        """
        Initialize the handler with the buffer size, the level at which
        flushing should occur and an optional target.

        Note that without a target being set either here or via setTarget(),
        a MemoryStreamHandler is no use to anyone!

        The ``flushOnClose`` argument is ``True`` for backward compatibility
        reasons - the old behaviour is that when the handler is closed, the
        buffer is flushed, even if the flush level hasn't been exceeded nor the
        capacity exceeded. To prevent this, set ``flushOnClose`` to ``False``.
        """
        logging.StreamHandler.__init__(self)
        self.name = name
        self.capacity = capacity
        self.buffer = []
        self.flushLevel = flushLevel
        self.target = target
        self.flushOnClose = flushOnClose
        self.setFormatter(logging.Formatter(format))

    def value(self):
        """
        Get the buffered messages as a list of strings.
        """
        return "\n".join(self.buffer)

    def emit(self, record):
        """
        Emit a record.

        Append the record. If shouldFlush() tells us to, call flush() to process
        the buffer.
        """
        self.buffer.append(self.format(record))
        if self.shouldFlush(record):
            self.flush()

    def shouldFlush(self, record):
        """
        Check for buffer full or a record at the flushLevel or higher.
        """
        return (len(self.buffer) >= self.capacity) or (record.levelno >= self.flushLevel)

    def setTarget(self, target: callable):
        """
        Set the target handler for this handler.
        """
        self.acquire()
        try:
            self.target = target
        finally:
            self.release()

    def flush(self):
        """
        For a MemoryHandler, flushing means just sending the buffered
        records to the target, if there is one. Override if you want
        different behaviour.

        The record buffer is also cleared by this operation.
        """
        self.acquire()
        try:
            if self.target:
                self.target(self.buffer)
                self.buffer.clear()
        finally:
            self.release()

    def close(self, flush: bool = True):
        """
        Flush, if appropriately configured, set the target to None and lose the
        buffer.
        """
        try:
            if self.flushOnClose and flush:
                self.flush()
            self.buffer.clear()
        finally:
            self.acquire()
            try:
                self.target = None
                logging.Handler.close(self)
            finally:
                self.release()
