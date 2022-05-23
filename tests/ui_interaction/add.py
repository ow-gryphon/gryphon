import platform
from pathlib import Path

from gryphon.constants import GRYPHON_HOME, CONFIG_FILE
from gryphon.wizard.wizard_text import Text
from .basic_actions import (
    start_wizard, quit_process, wait_for_success,
    navigate_libraries, confirm_information,
    key_down, key_up, enter, wait_for_output, type_text
)
from .constants import CONFIRMATION_MESSAGE
from .main_menu import select_add_on_main_menu


CONFIG_FILE_PATH = Path(GRYPHON_HOME) / CONFIG_FILE


def select_type_library(process):
    key_up(process, times=2)
    enter(process)
    wait_for_output(process, Text.type_library_name_menu_option)


def type_library_name(process, library):
    type_text(process, library)
    enter(process)


def confirm_information_typing_version(process, version):
    wait_for_output(process, CONFIRMATION_MESSAGE)
    key_down(process)
    enter(process)
    wait_for_output(process, Text.add_prompt_type_version)
    type_text(process, version)
    enter(process)


def add_library_selecting_version(working_directory, menu_way, version):
    process = None
    try:
        process = start_wizard(working_directory)

        select_add_on_main_menu(process)

        navigate_libraries(process, menu_way)

        confirm_information_typing_version(process, version)
        wait_for_success(process)
        quit_process(process)
    except Exception as e:
        if process:
            print(process.before)
        raise e


def add_library_typing(working_directory, library):
    process = None
    try:
        process = start_wizard(working_directory)

        select_add_on_main_menu(process)
        select_type_library(process)

        type_library_name(process, library)

        confirm_information(process)
        wait_for_success(process)
        quit_process(process)
    except Exception as e:
        if process:
            print(process.before)
        raise e


def add_library_from_menu(working_directory, tree_way):
    process = None
    try:
        process = start_wizard(working_directory)

        select_add_on_main_menu(process)

        navigate_libraries(process, tree_way)

        confirm_information(process)
        wait_for_success(process)
        quit_process(process)
    except Exception as e:
        if process:
            print(process.before)
        raise e
