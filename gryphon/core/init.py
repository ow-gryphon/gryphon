"""
Module containing the code for the init command in the CLI.
"""
import json
import logging
import shutil
from pathlib import Path
from .settings import SettingsManager
from ..constants import DEFAULT_ENV, INIT, VENV, CONDA
from .common_operations import (
    install_libraries_venv,
    create_venv,
    init_new_git_repo,
    initial_git_commit,
    log_operation, log_new_files,
    change_shell_folder_and_activate_venv,
    change_shell_folder_and_activate_conda_env,
    get_rc_file,
    create_conda_env, install_libraries_conda,
    install_extra_nbextensions_venv,
    install_extra_nbextensions_conda,
    download_template, unzip_templates,
    unify_templates
)


logger = logging.getLogger('gryphon')


def init(template, location, python_version, **kwargs):
    """
    Init command from the OW Gryphon CLI.
    """
    kwargs.copy()

    with open(SettingsManager.get_config_path(), "r", encoding="UTF-8") as f:
        data = json.load(f)
        env_type = data.get("environment_management", DEFAULT_ENV)

    logger.info("Creating project scaffolding.")
    logger.info(f"Initializing project at {location}")

    temporary_folder = download_template(template)
    zip_folder = unzip_templates(temporary_folder)
    template_folder = unify_templates(zip_folder)

    # Move files to destination
    shutil.copytree(
        src=Path(template_folder),
        dst=Path(location),
        dirs_exist_ok=True
    )
    shutil.rmtree(temporary_folder)
    shutil.rmtree(template_folder)

    # RC file
    rc_file = get_rc_file(Path.cwd() / location)
    log_operation(template, performed_action=INIT, logfile=rc_file)
    log_new_files(template, performed_action=INIT, logfile=rc_file)

    # Git
    repo = init_new_git_repo(folder=location)
    initial_git_commit(repo)

    # ENV Manager
    if env_type == VENV:
        # VENV
        create_venv(folder=location, python_version=python_version)
        install_libraries_venv(folder=location)
        install_extra_nbextensions_venv(location)
        change_shell_folder_and_activate_venv(location)
    elif env_type == CONDA:
        # CONDA
        create_conda_env(location, python_version=python_version)
        install_libraries_conda(location)
        install_extra_nbextensions_conda(location)
        change_shell_folder_and_activate_conda_env(location)
    else:
        raise RuntimeError("Invalid \"environment_management\" option on gryphon_config.json file."
                           f"Should be one of {[INIT, CONDA]} but \"{env_type}\" was given.")
