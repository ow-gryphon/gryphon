import time
from pathlib import Path

from gryphon.constants import GRYPHON_HOME, CONFIG_FILE, YES
from gryphon.wizard.wizard_text import Text
from .basic_actions import (
    wait_for_output, enter, type_text, quit_process,
    start_wizard, wait_for_success, select_nth_option
)
from .main_menu import select_init_from_existing_on_main_menu

CONFIG_FILE_PATH = Path(GRYPHON_HOME) / CONFIG_FILE


def select_the_first_template_on_init(process):
    select_nth_option(process, n=1)


def type_the_project_folder_name(process, folder_name: str):
    wait_for_output(process, Text.init_from_existing_prompt_location_question[:20])
    type_text(process, folder_name)
    enter(process)


def handle_point_to_external_env(process, point_external_env, external_env):
    wait_for_output(process, text=Text.init_from_existing_point_to_external_env)
    if point_external_env:
        select_nth_option(process, n=2)
        wait_for_output(process, text=Text.init_from_existing_ask_external_env_path)
        type_text(process, text=str(external_env))
        enter(process)
    else:
        select_nth_option(process, n=1)


def start_project_from_existing(project_name: str, has_existing_env: bool,
                                uses_existing_env: str, point_external_env: bool, external_env: Path,
                                working_directory: Path = Path.cwd()):
    process = None
    try:
        process = start_wizard(working_directory)
        select_init_from_existing_on_main_menu(process)
        select_the_first_template_on_init(process)
        type_the_project_folder_name(process, project_name)

        if has_existing_env:
            wait_for_output(process, Text.init_from_existing_confirm_conda_question[:10])
            time.sleep(1)

            if uses_existing_env == YES:
                select_nth_option(process, n=1)
            else:
                if uses_existing_env == "no_ignore":
                    select_nth_option(process, n=2)
                elif uses_existing_env == "no_delete":
                    select_nth_option(process, n=3)

                handle_point_to_external_env(process, point_external_env, external_env)

        else:
            handle_point_to_external_env(process, point_external_env, external_env)

        wait_for_success(process)
        quit_process(process)
    except Exception as e:
        if process:
            print(process.before)
        raise e
