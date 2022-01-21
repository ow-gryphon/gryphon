import logging
from colorlog import ColoredFormatter


LOG_LEVEL = logging.DEBUG

logging.root.setLevel(LOG_LEVEL)

formatter = ColoredFormatter(
    "%(log_color)s%(message)s",
    log_colors={
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)

stream = logging.StreamHandler()
stream.setFormatter(formatter)

logger = logging.getLogger('gryphon')
logger.addHandler(stream)

# TODO: insert file logging if needed in the future
