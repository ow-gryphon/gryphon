import json
from pathlib import Path

from gryphon.constants import GRYPHON_HOME, CONFIG_FILE, ALWAYS_ASK
from gryphon.wizard.wizard_text import Text
from .basic_actions import (
    start_wizard, quit_process, wait_for_success,
    select_nth_option, wait_for_output, enter,
    navigate_categories, confirm_information
)
from .main_menu import select_generate_on_main_menu

CONFIG_FILE_PATH = Path(GRYPHON_HOME) / CONFIG_FILE


def choose_third_template(process):
    select_nth_option(process, n=3)


def choose_latest_template_version(process):

    with open(CONFIG_FILE_PATH, "r", encoding="UTF-8") as f:
        settings = json.load(f)

    if settings["template_version_policy"] == ALWAYS_ASK:
        wait_for_output(process, Text.settings_ask_template_version)
        enter(process)


def generate_template(working_directory):
    process = None
    try:
        process = start_wizard(working_directory)
        select_generate_on_main_menu(process)

        navigate_categories(process, ["Methodology", "Data Exploration"])
        choose_third_template(process)

        choose_latest_template_version(process)

        confirm_information(process)
        wait_for_success(process)
        # I had to comment the code that creates a new session inside the created
        #  folder in order to make this test to work. It was giving timeout always
        quit_process(process)
    except Exception as e:
        if process:
            print(process.before)
        raise e
