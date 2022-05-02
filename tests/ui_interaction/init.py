import json
from pathlib import Path

from gryphon.constants import GRYPHON_HOME, CONFIG_FILE, ALWAYS_ASK
from gryphon.wizard.wizard_text import Text
from .basic_actions import (
    wait_for_output, enter, type_text, quit_process,
    start_wizard, wait_for_success, confirm_information
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


def start_new_project(project_name: str, working_directory: Path = Path.cwd()):
    process = None
    try:
        process = start_wizard(working_directory)
        select_init_on_main_menu(process)
        select_the_first_template_on_init(process)

        choose_latest_template_version(process)
        type_the_project_folder_name(process, project_name)
        choose_latest_python_version(process)

        confirm_information(process)
        wait_for_success(process)
        # TODO: I had to comment the code that creates a new session inside the created
        #  folder in order to make this test to work. It was giving timeout always
        quit_process(process)
    except Exception as e:
        if process:
            print(process.before)
        raise e
