import shutil

import pytest

from gryphon.constants import (
    CONDA, VENV, SYSTEM_DEFAULT, ALWAYS_ASK,
    USE_LATEST, VENV_FOLDER, CONDA_FOLDER
)
from gryphon.core.operations import SettingsManager
from .ui_interaction.init import start_new_project

python_versions = [SYSTEM_DEFAULT, ALWAYS_ASK]
environment_managers = [CONDA, VENV]
template_version_politics = [ALWAYS_ASK, USE_LATEST]
lib_install_method = ["type", "select", "version"]
dataviz = "Data Visualization"
seaborn = "seaborn"
SAMPLE_REQUIREMENTS = "sample_requirements.txt"


def execute_and_log(command) -> tuple:
    from subprocess import PIPE, Popen

    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    return stderr.decode(), stdout.decode()


@pytest.mark.parametrize('environment_manager', environment_managers)
@pytest.mark.parametrize('large_file', [True, False])
def test_pre_commit_hooks(
        setup, teardown, data_folder,
        environment_manager, large_file
):

    str_passed_large_files = "check for added large files..............................................Passed"
    str_ignore_files = "Ignore undesirable files.................................................Passed"
    str_failed_large_files = "check for added large files..............................................Failed"

    cwd = setup()
    project_name = "test_project"
    project_folder = cwd / project_name

    # Set up config conditions
    SettingsManager.change_environment_manager(environment_manager)
    SettingsManager.change_template_version_policy(USE_LATEST)
    SettingsManager.change_default_python_version(SYSTEM_DEFAULT)
    SettingsManager.change_pre_commit_file_size_limit(10)

    try:
        start_new_project(project_name, working_directory=cwd)

        if large_file:
            shutil.copy(
                src=data_folder / "large_file.test",
                dst=project_folder
            )

        env_folder = VENV_FOLDER if environment_manager == VENV else CONDA_FOLDER
        pre_commit_path = (project_folder / env_folder / "bin" / "pre-commit")

        assert pre_commit_path.is_file()

        stderr, stdout = execute_and_log(
            f"cd \"{project_folder}\" && "
            f"git add . && "
            f"git commit -m 'test commit'"
        )

        if large_file:
            assert str_failed_large_files in stderr
        else:
            assert str_passed_large_files in stderr

        assert str_ignore_files in stderr

    finally:
        teardown()
        # pass


@pytest.mark.parametrize('environment_manager', environment_managers)
@pytest.mark.parametrize('all_activated', [True, False])
def test_addons_configuration(
    setup, teardown, get_pip_libraries, get_conda_libraries,
    environment_manager, all_activated
):

    str_passed_large_files = "check for added large files..............................................Passed"
    str_ignore_files = "Ignore undesirable files.................................................Passed"
    str_failed_large_files = "check for added large files..............................................Failed"

    cwd = setup()
    project_name = "test_project"
    project_folder = cwd / project_name

    # Set up config conditions
    SettingsManager.change_environment_manager(environment_manager)
    SettingsManager.change_template_version_policy(USE_LATEST)
    SettingsManager.change_default_python_version(SYSTEM_DEFAULT)
    SettingsManager.change_pre_commit_file_size_limit(10)

    try:
        start_new_project(project_name, working_directory=cwd)

        if large_file:
            shutil.copy(
                src=data_folder / "large_file.test",
                dst=project_folder
            )

        env_folder = VENV_FOLDER if environment_manager == VENV else CONDA_FOLDER
        pre_commit_path = (project_folder / env_folder / "bin" / "pre-commit")

        assert pre_commit_path.is_file()

        stderr, stdout = execute_and_log(
            f"cd \"{project_folder}\" && "
            f"git add . && "
            f"git commit -m 'test commit'"
        )

        if large_file:
            assert str_failed_large_files in stderr
        else:
            assert str_passed_large_files in stderr

        assert str_ignore_files in stderr

    finally:
        teardown()
        # pass
