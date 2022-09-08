from pathlib import Path
from time import sleep

from gryphon.constants import GRYPHON_HOME, CONFIG_FILE
from gryphon.wizard.wizard_text import Text
from .basic_actions import (
    wait_for_output, enter, type_text, quit_process, key_down, start_wizard
)
from .main_menu import select_configure_and_logs_on_main_menu

CONFIG_FILE_PATH = Path(GRYPHON_HOME) / CONFIG_FILE


def select_default_addons(process):
    enter(process)


def select_all_addons(process):
    type_text(process, 'a')
    sleep(1)
    enter(process)


def select_no_addons(process):
    type_text(process, 'a')
    sleep(1)

    type_text(process, ' ')
    key_down(process)
    sleep(1)

    type_text(process, ' ')
    key_down(process)
    sleep(1)

    type_text(process, ' ')
    key_down(process)
    sleep(1)

    enter(process)


def change_addon_options(working_directory: Path = Path.cwd(), activate_all: bool = None):

    process = None
    try:
        process = start_wizard(working_directory)

        select_configure_and_logs_on_main_menu(process)

        if activate_all is None:
            select_default_addons(process)
        elif activate_all:
            select_all_addons(process)
        else:
            select_no_addons(process)

        wait_for_output(process, text="Successfully updated project addons.", timeout=30)

        # print("####### 3")
        # print(repr(process.before))
        # I had to comment the code that creates a new session inside the created
        #  folder in order to make this test to work. It was giving timeout always
        # wait_for_output(process, text="pre-commit installed", timeout=600)

        quit_process(process)
    except Exception as e:
        if process:
            print(process.before)
        raise e
