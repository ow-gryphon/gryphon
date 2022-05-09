"""
Module containing the code for the init command in the CLI.
"""
import json
import logging
import os
import shutil
from pathlib import Path

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
    unify_templates, copy_project_template,
    append_requirement, log_add_library,
    mark_notebooks_as_readonly,
    clean_temporary_folders, enable_files_overwrite
)
from .registry import Template
from .settings import SettingsManager
from ..constants import DEFAULT_ENV, INIT, VENV, CONDA, REMOTE_INDEX, LOCAL_TEMPLATE

logger = logging.getLogger('gryphon')


def init(template: Template, location, python_version, **kwargs):
    """
    Init command from the OW Gryphon CLI.
    """
    kwargs.copy()
    with open(SettingsManager.get_config_path(), "r", encoding="UTF-8") as f:
        data = json.load(f)
        env_type = data.get("environment_management", DEFAULT_ENV)

    logger.info("Creating project scaffolding.")
    logger.info(f"Initializing project at {location}")

    project_home = Path.cwd() / location
    os.makedirs(project_home, exist_ok=True)

    if template.registry_type == REMOTE_INDEX:

        download_folder = project_home / ".temp"
        zip_folder = project_home / ".unzip"
        template_folder = project_home / ".target"

        clean_temporary_folders(download_folder, zip_folder, template_folder)

        download_template(template, download_folder)
        unzip_templates(download_folder, zip_folder)
        unify_templates(zip_folder, template_folder)

        enable_files_overwrite(
            source_folder=template_folder / "notebooks",
            destination_folder=project_home / "notebooks"
        )
        mark_notebooks_as_readonly(template_folder / "notebooks")

        # Move files to destination
        shutil.copytree(
            src=Path(template_folder),
            dst=project_home,
            dirs_exist_ok=True
        )

        clean_temporary_folders(download_folder, zip_folder, template_folder)

    elif template.registry_type == LOCAL_TEMPLATE:

        copy_project_template(
            template_destiny=project_home,
            template_source=Path(template.path)
        )
    else:
        raise RuntimeError(f"Invalid registry type: {template.registry_type}.")

    # RC file
    rc_file = get_rc_file(Path.cwd() / location)
    log_operation(template, performed_action=INIT, logfile=rc_file)
    log_new_files(template, performed_action=INIT, logfile=rc_file)

    # Git
    repo = init_new_git_repo(folder=project_home)
    initial_git_commit(repo)

    # Requirements
    for r in template.dependencies:
        append_requirement(r, location)

    log_add_library(template.dependencies, logfile=rc_file)

    # ENV Manager
    if env_type == VENV:
        # VENV
        create_venv(folder=location, python_version=python_version)
        install_libraries_venv(folder=project_home)
        install_extra_nbextensions_venv(folder_path=project_home)
        change_shell_folder_and_activate_venv(project_home)
    elif env_type == CONDA:
        # CONDA
        create_conda_env(project_home, python_version=python_version)
        install_libraries_conda(project_home)
        install_extra_nbextensions_conda(project_home)
        change_shell_folder_and_activate_conda_env(project_home)
    else:
        raise RuntimeError("Invalid \"environment_management\" option on gryphon_config.json file."
                           f"Should be one of {[INIT, CONDA]} but \"{env_type}\" was given.")
