"""
Gryphon interactive wizard.
"""
import json
import platform
import argparse
from pathlib import Path
from gryphon.core.registry import RegistryCollection
from gryphon import wizard
from gryphon.wizard.wizard_text import Text
from gryphon.wizard.questions import CommonQuestions
from gryphon.wizard.constants import INIT, GENERATE, ADD, ABOUT, QUIT, BACK
from .logger import logger


if platform.system() == "Windows":
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from colorama import init
    init()

PACKAGE_PATH = Path(__file__).parent
DATA_PATH = PACKAGE_PATH / "data"

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
        # TODO: Activate a verbose level of log when with this mode activated.
        logger.warning("Starting Gryphon in debug mode.")

    logger.info(Text.welcome)

    while True:
        chosen_command = CommonQuestions.main_question()

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

# TODO: Test installation.
# TODO: Figure out if the user is in a folder with .venv (and inform the user)
# TODO: Create .labskitrc and populate it accordingly
# TODO: Developer documentations
# TODO: Handle errors from the pip commands

# TODO: Find a way to install wexpect for windows and pexpect for linux
# TODO: Power user configurations
    # TODO: Whether to install gryphon inside the .venv created for projects or not
    # TODO: Change repository urls and
# TODO: Have a single readme file with al the readmes from other templates
# TODO: Implement gitflow guidelines
