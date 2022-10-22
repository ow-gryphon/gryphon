"""
Gryphon interactive wizard.
"""
import argparse
import json
import logging
import os
import platform
import shutil
import sys
import glob
from pathlib import Path

import git

from . import __version__
from .constants import (
    INIT, GENERATE, ADD, ABOUT, QUIT, BACK, SETTINGS, INIT_FROM_EXISTING,
    GRYPHON_HOME, DEFAULT_CONFIG_FILE, CONFIG_FILE, DATA_PATH, HANDOVER,
    CONFIGURE_PROJECT, GRYPHON_RC, YES, EMAIL_RECIPIENT, CONTACT_US
)
from .core.common_operations import sort_versions
from .core.core_text import Text as CoreText
from .core.operations import BashUtils
from .core.registry import RegistryCollection
from .logger import logger
from .wizard import (
    init, generate, add, about, exit_program,
    settings, init_from_existing, handover, configure_project,
    contact_us
)
from .wizard.questions import CommonQuestions
from .wizard.wizard_text import Text


def output_error(er: Exception):
    import traceback

    logger.debug("Traceback (most recent call last):")
    for line in traceback.format_tb(er.__traceback__):
        logger.debug(line)

    # sample:                    ValueError(er)
    logger.error(f'\n{er.__class__.__name__}({er}).')


def initial_setup():
    if platform.system() == "Windows":
        logger.debug("Loading Windows colorama")
        # noinspection PyUnresolvedReferences,PyPackageRequirements
        from colorama import init as init_colorama
        init_colorama()

    logger.debug("Loading settings")
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

    return settings_file


def update_gryphon():
    logger.debug("Updating gryphon")

    def clone_from_remote(destination_path):
        logger.debug("Cloning repo from scratch")
        shutil.rmtree(destination_path, ignore_errors=True)

        return git.Repo.clone_from(
            url="https://github.com/ow-gryphon/gryphon.git",
            to_path=destination_path
        )

    def get_tags():
        temp_file = GRYPHON_HOME / "refs.txt"
        status_code, _ = BashUtils.execute_and_log(
            f"git ls-remote --tags https://github.com/ow-gryphon/gryphon >> \"{str(temp_file)}\""
        )

        if status_code is not None:
            raise RuntimeError(f"Failed to fetch gryphon tags. Status: {status_code}")

        with open(temp_file, 'r') as f:
            contents = f.read().strip()

        lines = contents.split('\n')
        tags = []
        for line in lines:
            ref = line.split(' ')[-1]
            tag = ref.split('/')[-1]
            tags.append(tag)

        os.remove(temp_file)
        return tags

    logger.debug("Fetching remote tags.")
    try:
        remote_tags = get_tags()
    except RuntimeError:
        logger.warning("Failed to check updates for Gryphon.")
        logger.debug("It was not possible to fetch the existing gryphon versions.")
        logger.debug("Failed to update")
        return

    latest_remote_version = sort_versions(remote_tags)[-1]
    latest = sort_versions([__version__, latest_remote_version])[-1]

    if __version__ != latest:
        logger.debug("Update needed")
        logger.warning("A new version from Gryphon is available.")
        logger.warning("Updating ...")
        repo_clone_path = GRYPHON_HOME / "git_gryphon_{}".format(str(latest))
        
        # Try to delete old versions
        for folder in glob.glob(str(GRYPHON_HOME / "git_gryphon*")):
            try:
                if folder != str(repo_clone_path):
                    shutil.rmtree(folder)
            except:
                logger.debug("Failed to completely remove cached old version: {}".format(folder))
        
        try:
            if not repo_clone_path.is_dir():
                repo = clone_from_remote(repo_clone_path)
            else:
                repo = git.Repo(path=repo_clone_path)

            # git clone at the desired tag
            logger.debug("Checkout")
            repo.git.checkout([latest, '-qqq'])

        except git.exc.GitCommandError as e:
            if "unable to access" in str(e):
                logger.warning("Failed to check updates for Gryphon.")
                logger.debug("Failed to update")
                return

        # pip install the version
        logger.debug("Installing the new version")
        BashUtils.execute_and_log(f"python -m pip install \"{repo_clone_path}\" -U -qqq")

        # restart gryphon
        if platform.system() == "Windows":
            logger.info("Update complete. Please start gryphon again by typing “gryphon”")
            exit(0)
        else:
            logger.info("Restarting gryphon")
            os.execv(sys.argv[0], sys.argv)
    else:
        logger.debug("No update needed")

    logger.debug("Update routine finished")


def send_traceback(exception):
    import webbrowser
    import urllib.parse
    import traceback

    tb = "Error Traceback:\n\nTraceback (most recent call last):"
    for line in traceback.format_tb(exception.__traceback__):
        tb += line

    subject = 'Report Crash'

    url_data = urllib.parse.urlencode(
        dict(
            to=EMAIL_RECIPIENT,
            subject=subject,
            body=CoreText.bug_report_email_template.replace("{traceback}", tb)
        )
    )

    webbrowser.open(f"mailto:?{url_data}", new=0)


def ask_to_report(exception):
    response = CommonQuestions.send_feedback()
    if response == YES:
        send_traceback(exception)


def set_log_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true')
    debug = parser.parse_args().debug
    if debug:
        logger.warning("Starting Gryphon in debug mode.")

        handler = list(filter(lambda x: x.name == "console", logger.handlers))[0]
        handler.setLevel(logging.DEBUG)
        # handler.setFormatter(debug_formatter)


def ignore_previous_keystrokes():
    if platform.system() == "Windows":
        # noinspection PyUnresolvedReferences
        import msvcrt

        sys.stdout.flush()
        while msvcrt.kbhit():
            msvcrt.getch()

    else:
        from termios import tcflush, TCIOFLUSH

        sys.stdout.flush()
        tcflush(sys.stdin, TCIOFLUSH)


def start_ui(settings_file):
    logger.debug("Loading registries")
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

    logger.debug("Setup finished")
    logger.warning(Text.welcome)

    while True:
        gryphon_rc = Path.cwd() / GRYPHON_RC

        # ignore partial keystrokes
        ignore_previous_keystrokes()
        chosen_command = CommonQuestions.main_question(
            inside_existing_project=gryphon_rc.is_file()
        )
        
        function = {
            CONFIGURE_PROJECT: configure_project,
            INIT: init,
            INIT_FROM_EXISTING: init_from_existing,
            GENERATE: generate,
            ADD: add,
            HANDOVER: handover,
            ABOUT: about,
            SETTINGS: settings,
            QUIT: exit_program,
            CONTACT_US: contact_us,
        }[chosen_command]

        try:
            try:

                response = function(DATA_PATH, registry)
            except OSError as er:
                response = None
                logger.debug(er)

            if response != BACK:
                if chosen_command in [GENERATE, ADD, CONFIGURE_PROJECT, CONTACT_US]:
                    logger.info("\n\n")
                    ignore_previous_keystrokes()
                    continue
                break

        except RuntimeError as er:
            logger.error(f'Runtime error: {er}')
            ask_to_report(er)
            exit(1)

        except KeyboardInterrupt:
            logger.warning(f'Operation cancelled by user')
            exit(0)

        except Exception as er:
            output_error(er)
            ask_to_report(er)
            exit(1)


def did_you_mean_gryphon():
    logger.info("Did you mean \"gryphon\"?")


def main():
    logger.info("Starting gryphon...")
    set_log_mode()
    BashUtils.execute_and_log("conda config --set notify_outdated_conda false")
    update_gryphon()
    settings_file = initial_setup()
    start_ui(settings_file)


if __name__ == '__main__':
    main()
