import logging
import time


# Custom formatter class
class _TimedLogger:
    """Logger class that prefixes each message with elapsed time since instantiation."""

    def __init__(self):
        self.reset_time()

    def reset_time(self):
        self.start_time = time.time()
        self.logger = logging.getLogger("logger")
        self.logger.setLevel(logging.INFO)  # Set the desired default logging level

        # Create a StreamHandler with a custom formatter
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self._CustomFormatter(self.start_time))

        # Clear existing handlers to avoid duplicate logs in case of reinitialization
        self.logger.handlers = []
        self.logger.addHandler(stream_handler)

    class _CustomFormatter(logging.Formatter):
        """Custom formatter to add time since start to logs."""

        def __init__(self, start_time):
            super().__init__("%(message)s")
            self.start_time = start_time

        def format(self, record):
            elapsed_seconds = time.time() - self.start_time
            # Format time as seconds.milliseconds
            formatted_time = f"{int(elapsed_seconds)}.{int((elapsed_seconds - int(elapsed_seconds)) * 1000)}"
            # Set the prefix with formatted time
            record.msg = f"[{formatted_time}] {record.msg}"
            return super().format(record)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)


logger = _TimedLogger()
