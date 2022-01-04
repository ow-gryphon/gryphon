"""
Module containing the code for the init command in the CLI.
"""
import os
from pathlib import Path
from .command_operations import (
    install_libraries,
    copy_project_template,
    create_venv,
    init_new_git_repo,
    initial_git_commit,
    populate_rc_file,
    change_shell_folder_and_activate_venv
)
from .logging import Logging

PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))


def init(template_path, location, **kwargs):
    """
    Init command from the OW Gryphon CLI.
    """
    Logging.log("Creating project scaffolding.", fg='green')
    kwargs.copy()

    Logging.log(f"Initializing project at {location}")
    copy_project_template(
        template_destiny=Path(location),
        template_source=Path(template_path)
    )
    populate_rc_file(folder=location)
    create_venv(folder=location)
    install_libraries(folder=location)
    repo = init_new_git_repo(folder=location)
    initial_git_commit(repo)
    change_shell_folder_and_activate_venv(location)
