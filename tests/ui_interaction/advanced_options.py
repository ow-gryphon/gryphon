from pathlib import Path

from gryphon.constants import GRYPHON_HOME, CONFIG_FILE
from gryphon.wizard.wizard_text import Text
from .basic_actions import (
    start_wizard, quit_process, wait_for_success,
    confirm_information, select_nth_option,
    enter, wait_for_output, type_text
)
from .init import select_default_addons
from .main_menu import select_advanced_on_main_menu

CONFIG_FILE_PATH = Path(GRYPHON_HOME) / CONFIG_FILE


def select_create_template_scaffold(process):
    select_nth_option(process, n=1)
    wait_for_output(process, Text.init_prompt_location_question)


def type_folder_name(process, folder):
    type_text(process, folder)
    enter(process)


def create_template_scaffold(working_directory):
    process = None
    try:
        process = start_wizard(working_directory)

        select_advanced_on_main_menu(process)
        select_create_template_scaffold(process)
        type_folder_name(process, "test_template")

        select_default_addons(process)

        confirm_information(process)
        wait_for_success(process)
        quit_process(process)
    except Exception as e:
        if process:
            print(process.before)
        raise e
