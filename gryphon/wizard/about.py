import json
import logging
import os
import platform

from .functions import erase_lines
from .questions import CommonQuestions
from .wizard_text import Text
from .. import __version__
from ..constants import QUIT, BACK

logger = logging.getLogger('gryphon')


def about(data_path, _):
    logger.info(Text.about)
    logger.info(f"Current version: {__version__}\n")

    with open(data_path / "links_about.json", encoding='utf-8') as f:
        links = json.loads(f.read())

    response = None
    while response != QUIT:
        response = CommonQuestions.prompt_about(links)

        if response == QUIT:
            return

        if response == BACK:
            erase_lines(n_lines=len(Text.about.split('\n')) + 2)
            return BACK

        if platform.system() == "Windows":
            os.system(f"start {response}")
            erase_lines(n_lines=1)
        else:
            os.system(f"""nohup xdg-open "{response}" """)
            os.system(f"""rm nohup.out""")
            erase_lines()
