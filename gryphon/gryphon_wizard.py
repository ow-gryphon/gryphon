"""
Gryphon interactive wizard.
"""
import os
import json
import platform
import argparse
from pathlib import Path
from gryphon.core.registry import RegistryCollection
from gryphon import wizard
from gryphon.wizard.wizard_text import Text
from gryphon.wizard.questions import Questions
from gryphon.wizard.constants import INIT, GENERATE, ADD, ABOUT, QUIT
from .logger import logger


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
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true')
    debug = parser.parse_args().debug
    if debug:
        logger.warning("Starting Gryphon in debug mode.")

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
                if chosen_command in [GENERATE, ADD]:
                    logger.debug("\n\n")
                    continue
                break

        except RuntimeError as er:
            logger.error(f'Runtime error: {er}')
            exit(1)

        except KeyboardInterrupt:
            logger.warning(f'Operation cancelled by user')
            exit(0)

        except Exception as er:
            if debug:
                raise er
            else:
                logger.error(f'Unexpected error: {er}. Call the support.')
                exit(1)


def did_you_mean_gryphon():
    logger.info("Did you mean \"gryphon\"?")

# TODO: Fix line wrapping on the long descriptions https://docs.python.org/2/library/textwrap.html
# DONE: Install the jupyter extensions libraries along with a new project creation
# DONE: Create the return option on generate command
# DONE: have 3 options when installing the library
    # 1 - yes
    # 2 - link to documentation
    # 3 - no -> back to the previous menu

# DONE: Do not close when installing libs (add command)

# DONE: Refactor generate function in order to use the same logic+data structure as add function

# TODO: Test installation.
# DONE: Test install from github (gryphon)

# TODO: Developers documentations
# TODO: Find a way to install wexpect for windows and pexpect for linux

# TODO: Figure out if the user is in a folder with .venv (and inform the user)
# TODO: Power user configurations
    # TODO: Whether to install gryphon inside the .venv created for projects or not
# TODO: Handle errors from the pip commands
# TODO: Create .labskitrc and populate it accordingly
# TODO: Have a single readme file with al the readmes from other templates
