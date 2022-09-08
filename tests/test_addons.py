import os
import shutil

import pytest

from gryphon.constants import (
    CONDA, VENV, SYSTEM_DEFAULT, ALWAYS_ASK,
    USE_LATEST, VENV_FOLDER, CONDA_FOLDER, GRYPHON_RC
)
from gryphon.core.operations import SettingsManager
from .ui_interaction.init import start_new_project
# from .ui_interaction.project_configuration import change_addon_options


python_versions = [SYSTEM_DEFAULT, ALWAYS_ASK]
environment_managers = [VENV, CONDA]
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
@pytest.mark.parametrize('all_activated', [False, True])
def test_addons_configuration(
    setup, teardown, get_pip_libraries, get_conda_libraries,
    environment_manager, all_activated
):

    def get_installed_libraries(env_manager):
        if env_manager == CONDA:
            return get_conda_libraries(project_folder)
        elif env_manager == VENV:
            return get_pip_libraries(project_folder)

    def not_in():
        # pre commit
        assert ("pre-commit" not in libraries) or not pre_commit_path.is_file()

        # nbstripout
        assert ("nbstripout" not in libraries) or not pre_commit_path.is_file()

        # nbextensions
        # assert "jupyter-contrib-nbextensions" not in libraries
        # assert "jupyter-nbextensions-configurator" not in libraries

    def _in():

        # pre commit
        assert ("pre-commit" in libraries) or pre_commit_path.is_file()

        # nbstripout
        assert ("nbstripout" in libraries) or nb_strip_out_path.is_file()

        # nbextensions
        # assert "jupyter-contrib-nbextensions" in libraries
        # assert "jupyter-nbextensions-configurator" in libraries

    cwd = setup()
    os.remove(cwd / GRYPHON_RC)
    project_name = "test_project"
    project_folder = cwd / project_name

    # Set up config conditions
    SettingsManager.change_environment_manager(environment_manager)
    SettingsManager.change_template_version_policy(USE_LATEST)
    SettingsManager.change_default_python_version(SYSTEM_DEFAULT)

    try:
        start_new_project(project_name, working_directory=cwd, activate_all=all_activated)
        libraries = get_installed_libraries(environment_manager)

        env_folder = VENV_FOLDER if environment_manager == VENV else CONDA_FOLDER
        pre_commit_path = project_folder / env_folder / "bin" / "pre-commit"
        nb_strip_out_path = project_folder / env_folder / "bin" / "nbstripout"

        if all_activated:
            _in()
        else:
            not_in()

        # change_addon_options(project_folder, activate_all=not all_activated)
        #
        # libraries = get_installed_libraries(environment_manager)
        # # this time the tests are inverted
        # if all_activated:
        #     not_in()
        # else:
        #     _in()

    finally:
        teardown()
        # pass
