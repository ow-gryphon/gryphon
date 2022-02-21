import logging
import os
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter
from .constants import GRYPHON_HOME

LOG_LEVEL = logging.DEBUG

"""
CRITICAL 50
ERROR 40
WARNING 30
SUCCESS 21
INFO 20
DEBUG 10
NOTSET 0
"""

logging.root.setLevel(logging.DEBUG)
logging.addLevelName(21, 'SUCCESS')

formatter = ColoredFormatter(
    "%(log_color)s%(message)s",
    log_colors={
        # 'DEBUG': 'white',
        # 'INFO': 'white',
        'SUCCESS': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white'
    }
)

stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
stream.setFormatter(formatter)

logger = logging.getLogger('gryphon')
logger.addHandler(stream)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


LOGFILE = GRYPHON_HOME / "logs" / "app.log"
if not LOGFILE.is_file():
    if not LOGFILE.parent.is_dir():
        os.makedirs(LOGFILE.parent)

    with open(LOGFILE, "w"):
        pass


fh = RotatingFileHandler(
    filename=LOGFILE,
    maxBytes=(1048576*5),
    backupCount=20
)
fh.setLevel(logging.DEBUG)
fh.setFormatter(file_formatter)
logger.addHandler(fh)
