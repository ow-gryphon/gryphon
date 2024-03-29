import logging
import os
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter

from .constants import GRYPHON_HOME

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

DEBUG_FORMATTER = '%(levelname)s %(asctime)s - %(message)s'


class DebugFormatter(ColoredFormatter):

    default_formatter = "%(log_color)s%(msg)s"

    def __init__(self):
        ColoredFormatter.__init__(
            self,
            self.default_formatter,
            log_colors={
                'SUCCESS': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white'
            }
        )

    def format(self, record):

        if record.levelno == logging.DEBUG:
            self._style._fmt = DEBUG_FORMATTER

        # Call the original formatter class to do the grunt work
        result = ColoredFormatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = self.default_formatter

        return result


console_handler = logging.StreamHandler()
console_handler.set_name("console")
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(DebugFormatter())


LOGFILE = GRYPHON_HOME / "logs" / "app.log"
if not LOGFILE.is_file():
    if not LOGFILE.parent.is_dir():
        os.makedirs(LOGFILE.parent)
    open(LOGFILE, "w", encoding="UTF-8").close()

file_handler = RotatingFileHandler(
    filename=LOGFILE,
    maxBytes=(1048576*5),
    backupCount=20,
    encoding="UTF-8"
)
file_handler.set_name("file")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)


logger = logging.getLogger('gryphon')
logger.addHandler(console_handler)
logger.addHandler(file_handler)
