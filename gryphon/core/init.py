"""
Module containing the code for the init command in the CLI.
"""
import json
import logging
import os
import shutil
from pathlib import Path

from .common_operations import (
    init_new_git_repo, initial_git_commit,
    fetch_template, append_requirement,
    mark_notebooks_as_readonly,
    clean_readonly_folder, enable_files_overwrite
)
from .operations import (
    BashUtils, EnvironmentManagerOperations, NBStripOutManager,
    RCManager, SettingsManager, PreCommitManager, NBExtensionsManager
)
from .registry import Template
from ..constants import (
    DEFAULT_ENV, INIT, VENV, CONDA, REMOTE_INDEX, SUCCESS,
    LOCAL_TEMPLATE, VENV_FOLDER, CONDA_FOLDER, REQUIREMENTS
)

logger = logging.getLogger('gryphon')


def handle_template(template, project_home, rc_file):
    if template.registry_type == REMOTE_INDEX:

        template_folder = fetch_template(template, project_home)

        try:
            enable_files_overwrite(
                source_folder=template_folder / "notebooks",
                destination_folder=project_home / "notebooks"
            )
            mark_notebooks_as_readonly(template_folder / "notebooks")

            # Move files to destination
            shutil.copytree(
                src=Path(template_folder),
                dst=project_home,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(
                    ".git",
                    ".github",
                    "__pycache__",
                    "envs",
                    ".venv",
                    ".ipynb_checkpoints"
                )
            )
        finally:
            RCManager.log_new_files(template, template_folder, performed_action=INIT, logfile=rc_file)
            clean_readonly_folder(template_folder)

    elif template.registry_type == LOCAL_TEMPLATE:

        BashUtils.copy_project_template(
            template_destiny=project_home,
            template_source=Path(template.path)
        )
        RCManager.log_new_files(template, Path(template.path) / "template", performed_action=INIT, logfile=rc_file)

    else:
        raise RuntimeError(f"Invalid registry type: {template.registry_type}.")


def init(template: Template, location, python_version,
         install_nbextensions=False,
         install_nb_strip_out=False,
         install_pre_commit_hooks=False,
         **kwargs
         ):
    """
    Init command from the OW Gryphon CLI.
    """
    kwargs.copy()
    with open(SettingsManager.get_config_path(), "r", encoding="UTF-8") as f:
        data = json.load(f)
        env_type = data.get("environment_management", DEFAULT_ENV)

    project_home = Path.cwd() / location
    logger.info("Creating project scaffolding.")
    logger.info(f"Initializing project at {project_home}")

    os.makedirs(project_home, exist_ok=True)

    # RC file
    rc_file = RCManager.get_rc_file(project_home)
    RCManager.log_operation(template, performed_action=INIT, logfile=rc_file)

    # TEMPLATE
    handle_template(template, project_home, rc_file)

    if install_pre_commit_hooks:
        PreCommitManager.initial_setup(project_home)

    # Git
    repo = init_new_git_repo(folder=project_home)
    initial_git_commit(repo)

    # Requirements
    for r in template.dependencies:
        append_requirement(r, project_home)

    RCManager.log_add_library(template.dependencies, logfile=rc_file)

    # ENV Manager
    if env_type == VENV:
        # VENV
        env_path = EnvironmentManagerOperations.create_venv(
            folder=project_home / VENV_FOLDER,
            python_version=python_version
        )

        RCManager.set_environment_manager(VENV, logfile=rc_file)
        RCManager.set_environment_manager_path(env_path, logfile=rc_file)

        EnvironmentManagerOperations.install_libraries_venv(
            environment_path=project_home / VENV_FOLDER,
            requirements_path=project_home / REQUIREMENTS
        )

        if install_nbextensions:
            NBExtensionsManager.install_extra_nbextensions_venv(
                environment_path=project_home / VENV_FOLDER,
                requirements_path=project_home / REQUIREMENTS
            )

        # EnvironmentManagerOperations.change_shell_folder_and_activate_venv(project_home)

    elif env_type == CONDA:
        # CONDA

        env_path = EnvironmentManagerOperations.create_conda_env(
            project_home / CONDA_FOLDER,
            python_version=python_version
        )

        RCManager.set_environment_manager(CONDA, logfile=rc_file)
        RCManager.set_environment_manager_path(env_path, logfile=rc_file)

        EnvironmentManagerOperations.install_libraries_conda(
            environment_path=project_home / CONDA_FOLDER,
            requirements_path=project_home / REQUIREMENTS
        )

        if install_nbextensions:
            NBExtensionsManager.install_extra_nbextensions_conda(
                environment_path=project_home / CONDA_FOLDER,
                requirements_path=project_home / REQUIREMENTS
            )

        # EnvironmentManagerOperations.change_shell_folder_and_activate_conda_env(project_home)
    else:
        raise RuntimeError("Invalid \"environment_management\" option on gryphon_config.json file."
                           f"Should be one of {[INIT, CONDA]} but \"{env_type}\" was given.")

    if install_nb_strip_out:
        NBStripOutManager.setup(project_home, environment_path=env_path)

    if install_pre_commit_hooks:
        PreCommitManager.final_setup(project_home)

    # update addons in gryphon_rc
    RCManager.set_addon_states(
        install_nb_strip_out=install_nb_strip_out,
        install_nbextensions=install_nbextensions,
        install_pre_commit_hooks=install_pre_commit_hooks,
        logfile=rc_file
    )

    EnvironmentManagerOperations.final_instructions(project_home, env_manager=env_type)

    logger.log(SUCCESS, "Project created successfully.")


