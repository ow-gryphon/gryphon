import logging
import os
import shutil
from pathlib import Path
from textwrap import wrap

from .common_operations import (
    init_new_git_repo, initial_git_commit,
    fetch_template, append_requirement,
    mark_notebooks_as_readonly,
    clean_readonly_folder, list_files
)
from .operations import EnvironmentManagerOperations, RCManager, PathUtils, SettingsManager
from ..constants import (
    GRYPHON_RC, VENV, CONDA, REMOTE_INDEX, LOCAL_TEMPLATE, VENV_FOLDER, CONDA_FOLDER, REQUIREMENTS
)

logger = logging.getLogger('gryphon')


def rename_dir(path):
    i = 0
    new_path = path
    while new_path.is_dir():
        i += 1
        new_path = Path(f"{path}_{i}")

    return new_path


def check_for_history(folder: Path):
    expected_history = folder / GRYPHON_RC

    return expected_history.is_dir()


def process_requirements(location, env, env_path):

    expected_requirements = location / REQUIREMENTS
    if expected_requirements.is_file():

        # DONE: change this to use the environment present in the gryphon_rc
        if env == CONDA:
            EnvironmentManagerOperations.install_libraries_conda(
                environment_path=env_path,
                requirements_path=location / REQUIREMENTS
            )

        elif env == VENV:
            EnvironmentManagerOperations.install_libraries_venv(
                environment_path=env_path,
                requirements_path=location / REQUIREMENTS
            )
    else:
        with open(expected_requirements, "w", encoding="UTF-8") as f:
            f.write("")


# ENVIRONMENT
def check_for_environment(folder: Path):
    expected_conda = folder / CONDA_FOLDER
    expected_venv = folder / VENV_FOLDER

    found_conda = expected_conda.is_dir()
    found_venv = expected_venv.is_dir()

    return found_conda, found_venv, expected_conda, expected_venv


def create_environment(path: Path, env_manager=None):
    if env_manager is None:
        env_manager = SettingsManager.get_environment_manager()

    if env_manager == CONDA:
        return EnvironmentManagerOperations.create_conda_env(path)
    elif env_manager == VENV:
        return EnvironmentManagerOperations.create_venv(path)


def process_environment(location, env_manager, use_existing_environment,
                        existing_env_path, delete_existing, external_env_path):
    print(use_existing_environment, existing_env_path, delete_existing, external_env_path)

    if use_existing_environment:
        if external_env_path is None:
            path = existing_env_path
        else:
            raise RuntimeError("Unexpected condition. Logic failure.")
    else:
        if delete_existing:
            shutil.rmtree(existing_env_path)

        path = PathUtils.get_destination_path(external_env_path)

        if external_env_path is None:

            path = location / VENV_FOLDER

            if env_manager == CONDA:
                path = location / CONDA_FOLDER

            elif env_manager == VENV:
                path = location / VENV_FOLDER

            if path.is_dir():
                path = rename_dir(path)

            path = create_environment(path, env_manager=env_manager)

    logfile = RCManager.get_rc_file(location)
    RCManager.set_environment_manager(env_manager, logfile)
    RCManager.set_environment_manager_path(path, logfile)

    return path


# TEMPLATE

def handle_template(template, project_home):

    if template.registry_type == REMOTE_INDEX:

        template_folder = fetch_template(template, project_home)
        mark_notebooks_as_readonly(template_folder / "notebooks")

    elif template.registry_type == LOCAL_TEMPLATE:
        template_folder = Path(template.path) / "template"

    else:
        raise RuntimeError(f"Invalid registry type: {template.registry_type}.")

    new_files = list_files(template_folder)
    existing_files = list_files(project_home)

    not_collided = [
        file
        for file in new_files
        if file not in existing_files
    ]

    for file in not_collided:

        origin = template_folder / file
        destination = project_home / file

        os.makedirs(destination.parent, exist_ok=True)
        shutil.copy2(
            src=origin,
            dst=destination
        )

    if template.registry_type == REMOTE_INDEX:
        clean_readonly_folder(template_folder)


# CORE
def init_from_existing(template, location: Path, env_manager, use_existing_environment, existing_env_path,
                       delete_existing, external_env_path):

    os.makedirs(location, exist_ok=True)
    rc_path = location / GRYPHON_RC

    if rc_path.is_file():
        gryphon_files_included = RCManager.get_handover_include_gryphon_generated_files(rc_path)
        if gryphon_files_included:
            logger.warning("Every Gryphon file used in this project are present in the current directory.")
        else:
            operations = RCManager.get_gryphon_operations(rc_path)

            template_string_list = '\n\t- '.join(map(lambda x: f'{x["template_name"]} ({x["action"]})', operations))

            message = "There were some Gryphon files originally used in this project that were suppressed on the " \
                      "handover process. Please install the following templates if you want the complete set of files:"

            for line in wrap(message, width=100):
                logger.warning(line)

            logger.warning(f"\n\t- {template_string_list}\n")

    # TEMPLATE
    handle_template(template, project_home=location)

    # ENVIRONMENT
    env_path = process_environment(location, env_manager, use_existing_environment,
                                   existing_env_path, delete_existing, external_env_path)

    # REQUIREMENTS
    for r in template.dependencies:
        append_requirement(r, location)
    process_requirements(location, env_manager, env_path)

    # Git
    repo = init_new_git_repo(folder=location)
    initial_git_commit(repo)

    if env_manager == VENV:
        # VENV
        EnvironmentManagerOperations.change_shell_folder_and_activate_venv(location, alternative_env=env_path)
    elif env_manager == CONDA:
        # CONDA
        EnvironmentManagerOperations.change_shell_folder_and_activate_conda_env(location, alternative_env=env_path)
