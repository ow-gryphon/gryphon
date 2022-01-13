"""
Gryphon interactive wizard.
"""
import os
import json
import platform
from pathlib import Path
from gryphon.core.registry import RegistryCollection
from gryphon import wizard
from gryphon.wizard.wizard_text import Text
from gryphon.wizard.questions import Questions
from .logger import logger
from wizard.constants import INIT, GENERATE, ADD, ABOUT, QUIT


if platform.system() == "Windows":
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from colorama import init
    init()

PACKAGE_PATH = Path(__file__).parent
DATA_PATH = PACKAGE_PATH / "data"
BACK = "back"

# Load contents of configuration file
with open(DATA_PATH / "gryphon_config.json", "r") as f:
    settings = json.load(f)

try:
    # loads registry of templates to memory
    registry = RegistryCollection.from_config_file(
        settings=settings,
        data_path=DATA_PATH / "template_registry"
    )
except Exception as e:
    logger.error(f'Registry loading error. {e}')
    exit(1)


def main():
    logger.info(Text.welcome)

    while True:
        chosen_command = Questions.main_question()

        function = {
            INIT: wizard.init,
            GENERATE: wizard.generate,
            ADD: wizard.add,
            ABOUT: wizard.about,
            QUIT: wizard.exit_program
        }[chosen_command]

        try:
            response = function(DATA_PATH, registry)
            if response != BACK:
                break
        except RuntimeError as er:
            logger.error(f'Runtime error. {er}')


def did_you_mean_gryphon():
    logger.info("Did you mean \"gryphon\"?")


# this enables us to use the cli without having to install each time
# by using `python gryphon_wizard.py`
if __name__ == '__main__':
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    main()

# TODO: Figure out if the user is in a folder with .venv (and inform the user)
