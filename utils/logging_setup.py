import logging


class LogColors:
    GRAY = "\x1b[90m"  # Bright black (gray)
    BRIGHT_BLUE = "\x1b[94m"  # Brighter blue
    YELLOW = "\x1b[33;1m"
    RED = "\x1b[31;1m"
    MAGENTA = "\x1b[35m"  # Magenta
    RESET = "\x1b[0m"
    CYAN = "\x1b[36;1m"  # Turquoise


class CustomFormatter(logging.Formatter):
    FORMAT = (
        "["
        + LogColors.GRAY
        + "%(asctime)s"
        + LogColors.RESET
        + "] [%(levelname)-8s"
        + LogColors.RESET
        + "] %(name)s"
        + LogColors.RESET
        + ": %(message)s"
    )

    COLOR_FORMAT = {
        logging.DEBUG: FORMAT.replace(
            "%(levelname)-8s", LogColors.CYAN + "%(levelname)-8s"
        ).replace("%(name)s", LogColors.MAGENTA + "%(name)s"),
        logging.INFO: FORMAT.replace(
            "%(levelname)-8s", LogColors.BRIGHT_BLUE + "%(levelname)-8s"
        ).replace("%(name)s", LogColors.MAGENTA + "%(name)s"),
        logging.WARNING: FORMAT.replace(
            "%(levelname)-8s", LogColors.YELLOW + "%(levelname)-8s"
        ).replace("%(name)s", LogColors.MAGENTA + "%(name)s"),
        logging.ERROR: FORMAT.replace(
            "%(levelname)-8s", LogColors.RED + "%(levelname)-8s"
        ).replace("%(name)s", LogColors.MAGENTA + "%(name)s"),
        logging.CRITICAL: FORMAT.replace(
            "%(levelname)-8s", LogColors.RED + "%(levelname)-8s"
        ).replace("%(name)s", LogColors.MAGENTA + "%(name)s"),
    }

    def format(self, record):
        log_fmt = self.COLOR_FORMAT.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    file_handler = logging.FileHandler("bot.log")
    log_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
