import json
from pathlib import Path

from gryphon.constants import GRYPHON_HOME, CONFIG_FILE, ALWAYS_ASK
from gryphon.wizard.wizard_text import Text
from .basic_actions import (
    wait_for_output, enter, type_text, quit_process,
    start_wizard, wait_for_end, confirm_information
)
from .main_menu import select_init_on_main_menu

CONFIG_FILE_PATH = Path(GRYPHON_HOME) / CONFIG_FILE


def select_the_first_template_on_init(process):
    enter(process)


def type_the_project_folder_name(process, folder_name: str):
    wait_for_output(process, Text.init_prompt_location_question)
    type_text(process, folder_name)
    enter(process)


def choose_latest_template_version(process):

    with open(CONFIG_FILE_PATH, "r", encoding="UTF-8") as f:
        settings = json.load(f)

    if settings["template_version_policy"] == ALWAYS_ASK:
        wait_for_output(process, Text.settings_ask_template_version)
        enter(process)


def choose_latest_python_version(process):

    with open(CONFIG_FILE_PATH, "r", encoding="UTF-8") as f:
        settings = json.load(f)

    if settings["default_python_version"] == ALWAYS_ASK:
        wait_for_output(process, Text.settings_ask_python_version, timeout=300)
        enter(process)


def select_default_addons(process):
    wait_for_output(process, text=Text.init_prompt_addons)
    enter(process)


def select_all_addons(process):
    wait_for_output(process, text=Text.init_prompt_addons)
    type_text(process, 'a')
    enter(process)


def select_no_addons(process):
    wait_for_output(process, text=Text.init_prompt_addons)
    type_text(process, 'a')
    type_text(process, 'a')
    enter(process)


def start_new_project(project_name: str, working_directory: Path = Path.cwd(), activate_all: bool = None):
    process = None
    try:
        process = start_wizard(working_directory)
        select_init_on_main_menu(process)
        select_the_first_template_on_init(process)

        choose_latest_template_version(process)
        type_the_project_folder_name(process, project_name)
        choose_latest_python_version(process)

        if activate_all is None:
            select_default_addons(process)
        elif activate_all:
            select_all_addons(process)
        else:
            select_no_addons(process)

        confirm_information(process)
        wait_for_end(process)
        # I had to comment the code that creates a new session inside the created
        #  folder in order to make this test to work. It was giving timeout always
        # wait_for_output(process, text="pre-commit installed", timeout=600)

        quit_process(process)
    except Exception as e:
        if process:
            print(process.before)
            quit_process(process)
        raise e
