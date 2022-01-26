import logging
from colorlog import ColoredFormatter


LOG_LEVEL = logging.DEBUG

logging.root.setLevel(LOG_LEVEL)
logging.addLevelName(21, 'SUCCESS')

"""
CRITICAL 50
ERROR 40
WARNING 30
INFO 20
DEBUG 10
NOTSET 0
"""

formatter = ColoredFormatter(
    "%(log_color)s%(message)s",
    log_colors={
        # 'DEBUG': 'white',
        # 'INFO': 'white',
        'SUCCESS': 'green',
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
