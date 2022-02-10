import os
import json
import platform
import logging
from .functions import erase_lines
from .wizard_text import Text
from .questions import CommonQuestions
from ..constants import QUIT, BACK


logger = logging.getLogger('gryphon')


def about(data_path, _):
    logger.info(Text.about)

    with open(data_path / "links_about.json") as f:
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
