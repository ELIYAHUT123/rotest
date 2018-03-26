"""Tree format log to screen stream handler."""
import logging

from rotest.common import core_log
from rotest.core.utils.pretty import wrap_title, Result
from stream_handler import EventStreamHandler
from rotest.common.log import ColoredFormatter


class LogStreamHandler(EventStreamHandler):
    """Log to screen handler.

    Overrides result handler's methods to print each event change in the main
    result object to the given stream, and pipe log records to it.

    Attributes:
        LOG_FORMAT (str): format of the printed messages.
        LOG_HANDLER_NAME (str): name of the log-to-screen log handler.
    """
    LOG_HANDLER_NAME = "Log to screen handler"
    LOG_FORMAT = '    %(asctime)s : %(message)s'

    def __init__(self, *args, **kwargs):
        """Initialize the handler and register the new stream log handler."""
        super(LogStreamHandler, self).__init__(*args, **kwargs)

        if all(handler.get_name() != self.LOG_HANDLER_NAME
               for handler in core_log.handlers):

            current_log_stream = logging.StreamHandler(self.stream)
            current_log_stream.setLevel(self.LEVEL)
            current_log_stream.set_name(self.LOG_HANDLER_NAME)
            formatter = ColoredFormatter(self.LOG_FORMAT,
                                         datefmt="%H:%M:%S")
            current_log_stream.setFormatter(formatter)
            core_log.addHandler(current_log_stream)


class LogInfoHandler(LogStreamHandler):
    """Info-level log to screen handler."""
    NAME = 'loginfo'
    LEVEL = logging.INFO


class LogDebugHandler(LogStreamHandler):
    """Debug-level log to screen handler."""
    NAME = 'logdebug'
    LEVEL = logging.DEBUG


class PrettyHandler(LogStreamHandler):
    NAME = 'pretty'
    LEVEL = logging.DEBUG

    def start_test(self, test):
        self.stream.writeln(wrap_title(test, Result.started))

    def stop_test(self, test):
        pass

    def stop_test_run(self):
        pass

    def add_success(self, test):
        self.stream.writeln(wrap_title(test, Result.success))

    def add_skip(self, test, reason):
        self.stream.writeln(wrap_title(test, Result.skip))

    def add_error(self, test, exception_str):
        self.stream.writeln(wrap_title(test, Result.error))

    def add_failure(self, test, exception_str):
        self.stream.writeln(wrap_title(test, Result.failure))
