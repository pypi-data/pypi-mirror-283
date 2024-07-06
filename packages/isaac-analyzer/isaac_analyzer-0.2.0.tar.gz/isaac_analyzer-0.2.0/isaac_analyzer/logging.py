import logging


class Colors:
    grey = "\x1b[0;37m"
    green = "\x1b[1;32m"
    yellow = "\x1b[1;33m"
    red = "\x1b[1;31m"
    purple = "\x1b[1;35m"
    blue = "\x1b[1;34m"
    light_blue = "\x1b[1;36m"
    reset = "\x1b[0m"
    blink_red = "\x1b[5m\x1b[1;31m"


class ColorFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    def __init__(self, auto_colorized=True, custom_format: str = None):
        super(ColorFormatter, self).__init__()
        self.auto_colorized = auto_colorized
        self.custom_format = custom_format
        self.FORMATS = self.define_format()

    def define_format(self):
        format_prefix = f"{Colors.light_blue}%(asctime)s " f"%(name)s{Colors.reset} "
        # f"(%(filename)s:%(lineno)d){Colors.reset} "

        format_suffix = f"%(levelname)s{Colors.reset} - %(message)s"

        return {
            logging.DEBUG: format_prefix + Colors.blue + format_suffix + Colors.reset,
            logging.INFO: format_prefix
            + Colors.light_blue
            + format_suffix
            + Colors.reset,
            logging.WARNING: format_prefix
            + Colors.yellow
            + format_suffix
            + Colors.reset,
            logging.ERROR: format_prefix + Colors.red + format_suffix + Colors.reset,
            logging.CRITICAL: format_prefix
            + Colors.blink_red
            + format_suffix
            + Colors.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class FileFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    def __init__(self, auto_colorized=True, custom_format: str = None):
        super(FileFormatter, self).__init__()
        self.auto_colorized = auto_colorized
        self.custom_format = custom_format
        self.FORMATS = self.define_format()

    def define_format(self):
        format_prefix = "%(asctime)s " "%(name)s "

        format_suffix = "%(levelname)s - %(message)s"

        return {
            logging.DEBUG: format_prefix + format_suffix,
            logging.INFO: format_prefix + format_suffix,
            logging.WARNING: format_prefix + format_suffix,
            logging.ERROR: format_prefix + format_suffix,
            logging.CRITICAL: format_prefix + format_suffix,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Configure logging


def setColoredLogger(logger: logging.Logger):
    logging.basicConfig(level=logging.INFO)
    loggingStream = logging.StreamHandler()
    fileStream = logging.FileHandler("log.log")
    loggingStream.setLevel(logging.DEBUG)
    fileStream.setLevel(logging.DEBUG)
    loggingStream.setFormatter(ColorFormatter())
    fileStream.setFormatter(FileFormatter())
    logger.addHandler(loggingStream)
    logger.addHandler(fileStream)
    logger.propagate = False
    return logger


def init(defaultLevel):
    logging.getLogger().setLevel(defaultLevel)
    mpl_logger = logging.getLogger("matplotlib")
    mpl_logger.setLevel(logging.WARNING)
    PIL_logger = logging.getLogger("PIL")
    PIL_logger.setLevel(logging.WARNING)


def getLogger(name):
    logger = logging.getLogger(name)
    return setColoredLogger(logger)
