"""
Gryphon interactive wizard.
"""
import os
import json
import shutil
import logging
import platform
import argparse
import traceback
from .core.registry import RegistryCollection
from .wizard import init, generate, add, about, exit_program, settings
from .wizard.wizard_text import Text
from .wizard.questions import CommonQuestions
from .constants import (
    INIT, GENERATE, ADD, ABOUT, QUIT, BACK, SETTINGS,
    GRYPHON_HOME, DEFAULT_CONFIG_FILE, CONFIG_FILE, DATA_PATH
)
from .logger import logger


def output_error(er: Exception):
    logger.debug("Traceback (most recent call last):")
    for line in traceback.format_tb(er.__traceback__):
        logger.debug(line)

    # sample:                    ValueError(er)
    logger.error(f'{er.__class__.__name__}({er}). Please report to the support.')


if platform.system() == "Windows":
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from colorama import init as init_colorama
    init_colorama()

try:
    with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
        settings_file = json.load(f)

    with open(DEFAULT_CONFIG_FILE, "r", encoding="UTF-8") as f:
        default_settings_file = json.load(f)

    try:
        if settings_file["config_version"] < default_settings_file["config_version"]:
            os.remove(CONFIG_FILE)
            raise FileNotFoundError()
    except KeyError:
        raise FileNotFoundError()

except FileNotFoundError:
    if not GRYPHON_HOME.is_dir():
        os.makedirs(GRYPHON_HOME)
    
    shutil.copy(
        src=DEFAULT_CONFIG_FILE,
        dst=CONFIG_FILE
    )
    with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
        settings_file = json.load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true')
    debug = parser.parse_args().debug
    if debug:
        logger.warning("Starting Gryphon in debug mode.")

        handler = list(filter(lambda x: x.name == "console", logger.handlers))[0]
        handler.setLevel(logging.DEBUG)

    registry = None
    try:

        registry = RegistryCollection.from_config_file(
            settings=settings_file,
            data_path=GRYPHON_HOME / "registry"
        )
    except Exception as e:
        logger.error(f'Registry loading error.')
        output_error(e)
        exit(1)

    logger.info(Text.welcome)

    while True:
        chosen_command = CommonQuestions.main_question()
        
        function = {
            INIT: init,
            GENERATE: generate,
            ADD: add,
            ABOUT: about,
            SETTINGS: settings,
            QUIT: exit_program
        }[chosen_command]

        try:
            response = function(DATA_PATH, registry)
            if response != BACK:
                if chosen_command in [GENERATE, ADD]:
                    logger.info("\n\n")
                    continue
                break

        except RuntimeError as er:
            logger.error(f'Runtime error: {er}')
            exit(1)

        except KeyboardInterrupt:
            logger.warning(f'Operation cancelled by user')
            exit(0)

        except Exception as er:
            output_error(er)
            exit(1)


def did_you_mean_gryphon():
    logger.info("Did you mean \"gryphon\"?")

# TODO: On generate, check if there are both a conda and a venv inside folder and use the one that is available
# TODO: Test installation.
# TODO: Resizing error on windows (duplicating texts).

# TODO: Have a single readme file with all the readmes from other templates
# TODO: Find a way to install wexpect for windows and pexpect for linux
# TODO: Implement gitflow guidelines
# TODO: Check if the user is really on a gryphon project folder


if __name__ == '__main__':
    main()

# TODO: make local templates use the same format as the index
# TODO: Automatically add
