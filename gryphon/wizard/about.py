import os
import platform
from .functions import *
from .text import Text
from .questions import Questions

BACK = "back"


def about():
    Logging.log(Text.about)

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
