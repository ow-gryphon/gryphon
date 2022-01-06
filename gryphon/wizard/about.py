import os
import platform
import logging
from .functions import erase_lines
from .wizard_text import Text
from .questions import Questions
from .constants import *


logger = logging.getLogger('gryphon')


def about(_, __):
    logger.info(Text.about)

    response = None
    while response != "quit":
        response = Questions.prompt_about()

        if response == "quit":
            return

        if response == BACK:
            erase_lines(n_lines=8)
            return BACK

        if platform.system() == "Windows":
            os.system(f"start {response}")
            erase_lines(n_lines=1)
        else:
            os.system(f"""nohup xdg-open "{response}" """)
            os.system(f"""rm nohup.out""")
            erase_lines()
