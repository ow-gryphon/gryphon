import os

import pytest

from gryphon.constants import (
    CONDA, VENV, REQUIREMENTS, GRYPHON_RC, YES
)
from gryphon.core.operations import RCManager, SettingsManager
from .ui_interaction.init_from_existing import start_project_from_existing
from .utils import create_folder_with_conda_env, create_folder_with_venv

environment_managers = [CONDA, VENV]


def create_environment(path, environment_manager):

    if environment_manager == CONDA:
        return create_folder_with_conda_env(folder_name=path)

    elif environment_manager == VENV:
        return create_folder_with_venv(folder_name=path)


@pytest.mark.parametrize('environment_manager', environment_managers)
@pytest.mark.parametrize('has_existing_env', [True, False])
@pytest.mark.parametrize('uses_existing_env', [YES, "no_ignore", "no_delete"])
@pytest.mark.parametrize('point_external_env', [True, False])
def test_init_from_existing(
        setup, teardown,
        environment_manager, uses_existing_env, point_external_env, has_existing_env
):
    if point_external_env and uses_existing_env == YES:
        return

    if uses_existing_env == YES and not has_existing_env:
        return

    cwd = setup()
    project_name = "test_project"
    project_folder = cwd / project_name

    # Set up config conditions
    SettingsManager.change_environment_manager(environment_manager)
    try:
        external_env_path = None
        if point_external_env:
            external_env_path = create_environment(cwd, environment_manager)
            os.remove(cwd / GRYPHON_RC)

        previous_env_path = None
        if has_existing_env:
            previous_env_path = create_environment(project_folder, environment_manager)
            os.remove(project_folder / GRYPHON_RC)

        start_project_from_existing(
            working_directory=cwd,
            project_name=project_name,

            uses_existing_env=uses_existing_env,
            has_existing_env=has_existing_env,

            point_external_env=point_external_env,
            external_env=external_env_path
        )

        # CHECKS
        # CHECK IF THE ENV IS CORRECTLY SET ON GRYPHON_RC
        logfile = project_folder / GRYPHON_RC

        # CHECK IF THE ENV SET ON GRYPHON_RC exists is folder
        assert logfile.is_file()

        # CHECK IF THE ENVIRONMENT MANAGER WAS PROPERLY SET ACCORDING TO WHAT WE WANTED
        used_env_manager = RCManager.get_environment_manager_path(logfile=logfile)
        used_env_manager_type = RCManager.get_environment_manager(logfile=logfile)

        assert environment_manager == used_env_manager_type

        if uses_existing_env == YES and has_existing_env:
            assert previous_env_path == cwd / used_env_manager

        if uses_existing_env == "no_ignore" and has_existing_env:
            assert cwd / used_env_manager != previous_env_path

        if point_external_env:
            assert external_env_path == cwd / used_env_manager

        # CHECK IF EXISTING ENVIRONMENT WAS SUCCESSFULLY DELETED
        if has_existing_env and uses_existing_env == "no_delete" and point_external_env:
            assert not previous_env_path.is_dir()

        # CHECK IF THERE IS REQUIREMENTS
        assert (project_folder / REQUIREMENTS).is_file()

        # CHECK BASIC FOLDER STRUCTURE
        assert (project_folder / "notebooks").is_dir()
        assert (project_folder / "utilities").is_dir()

    finally:
        teardown()
        # pass
