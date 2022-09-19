from pathlib import Path

from gryphon.constants import GRYPHON_HOME, CONFIG_FILE
from gryphon.core.core_text import Text as CoreText
from gryphon.wizard.wizard_text import Text
from .basic_actions import (
    start_wizard, quit_process, type_text,
    select_nth_option, wait_for_output, enter
)
from .constants import CONFIRMATION_MESSAGE
from .main_menu import select_handover_on_main_menu

CONFIG_FILE_PATH = Path(GRYPHON_HOME) / CONFIG_FILE


def choose_first_template(process):
    select_nth_option(process, n=1)


def type_folder_path(process, path):
    type_text(process, text=str(path))
    enter(process)
    wait_for_output(process, CONFIRMATION_MESSAGE[2:-2], timeout=60)


def get_back_from_change_configuration(process):
    wait_for_output(process, Text.handover_prompt_change_settings[5:-2])
    select_nth_option(process, n=3)
    wait_for_output(process, CONFIRMATION_MESSAGE[2:-2])


def generate_handover_package(working_directory, handover_folder, file_size_limit,
                              include_gryphon_files, change_configs=None):
    process = None
    try:
        process = start_wizard(working_directory)
        select_handover_on_main_menu(process)

        type_folder_path(process, handover_folder)
        if change_configs is None:
            # YES
            select_nth_option(process, n=1)

        elif change_configs == "change_size_limit":
            select_nth_option(process, n=2)
            wait_for_output(process, "setting you want")
            select_nth_option(process, n=1)
            wait_for_output(process, "new size limit you want")
            type_text(process, str(file_size_limit))
            enter(process)

            get_back_from_change_configuration(process)
            select_nth_option(process, n=1)

        elif change_configs == "change_gryphon_politics":
            select_nth_option(process, n=2)
            wait_for_output(process, "setting you want")
            select_nth_option(process, n=2)
            wait_for_output(process, Text.handover_prompt_gryphon_files_policy[5:-2])

            if include_gryphon_files:
                # YES
                select_nth_option(process, n=1)
            else:
                # NO
                select_nth_option(process, n=2)

            get_back_from_change_configuration(process)
            select_nth_option(process, n=1)
        else:
            return
        wait_for_output(process, CoreText.handover_end_message)

        quit_process(process)
    except Exception as e:
        if process:
            print(process.before)
        raise e
