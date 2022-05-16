import json
import os
import shutil
from pathlib import Path

from ..constants import CONDA, VENV, REQUIREMENTS
from ..constants import VENV_FOLDER, CONDA_FOLDER, GRYPHON_HISTORY, YES, NO
from ..core.operations import EnvironmentManagerOperations, RCManager
from ..core.settings import SettingsManager


def check_for_history(folder: Path):
    expected_history = folder / GRYPHON_HISTORY

    return expected_history.is_dir()


def check_for_environment(folder: Path):
    expected_conda = folder / CONDA_FOLDER
    expected_venv = folder / VENV_FOLDER

    found_conda = expected_conda.is_dir()
    found_venv = expected_venv.is_dir()

    return found_conda, found_venv, expected_conda, expected_venv


def check_for_requirements(folder: Path):
    expected_requirements = folder / REQUIREMENTS

    return expected_requirements.is_dir()


def process_requirements(location, env, env_path):
    found_requirements = check_for_requirements(location)
    if found_requirements:

        # TODO: change this to use the environment present in the
        if env == CONDA:
            EnvironmentManagerOperations.install_libraries_conda(external_environment_path=env_path)
        elif env == VENV:
            EnvironmentManagerOperations.install_libraries_venv(external_environment_path=env_path)
    else:
        with open(location / REQUIREMENTS, "w", encoding="UTF-8") as f:
            f.write("")


def get_environment_manager():
    with open(SettingsManager.get_config_path(), "r", encoding="UTF-8") as f:
        return json.load(f)["environment_management"]


def create_environment(path: Path, env_manager=None):
    if env_manager is None:
        env_manager = get_environment_manager()

    if env_manager == CONDA:
        return EnvironmentManagerOperations.create_conda_env(path)
    elif env_manager == VENV:
        return EnvironmentManagerOperations.create_venv(path)


def process_environment_core(location, env_manager, use_existing_environment, env_path, history_file):
    if use_existing_environment == "no_delete":
        shutil.rmtree(env_path)

    if use_existing_environment != YES:
        if env_path.is_dir():
            pass
            # rename folder
        env_path = create_environment(location, env_manager=env_manager)

    # TODO: put information about the env manager and env into the rc file


def init_from_existing(location, env_manager, use_existing_environment, env_path):

    # HISTORY
    history_file = RCManager.get_rc_file(location)
    # TODO: rename environments when we already have one on the folder (no_ignore)

    # ENVIRONMENT
    process_environment_core(location, env_manager, use_existing_environment, env_path, history_file)

    # REQUIREMENTS
    process_requirements(location, env_manager, env_path)

    os.makedirs(location / "notebooks", exist_ok=True)
    os.makedirs(location / "data", exist_ok=True)

    # TODO: Ask template before the other prompts?
    # TODO: What will be the existing files policy? Overwrite or ignore?
    # TODO: BACK options are needed in every menu
