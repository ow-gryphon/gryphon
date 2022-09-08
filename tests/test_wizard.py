import glob

import pytest

from gryphon.constants import (
    CONDA, VENV, SYSTEM_DEFAULT, ALWAYS_ASK,
    USE_LATEST, VENV_FOLDER, CONDA_FOLDER
)
from gryphon.core.operations import SettingsManager
from .ui_interaction.add import add_library_from_menu, add_library_typing, add_library_selecting_version
from .ui_interaction.generate import generate_template
from .ui_interaction.init import start_new_project

python_versions = [SYSTEM_DEFAULT, ALWAYS_ASK]
environment_managers = [CONDA, VENV]
template_version_politics = [ALWAYS_ASK, USE_LATEST]
lib_install_method = ["type", "select", "version"]
dataviz = "Data Visualization"
seaborn = "seaborn"
SAMPLE_REQUIREMENTS = "sample_requirements.txt"


@pytest.mark.parametrize('python_version', python_versions)
@pytest.mark.parametrize('environment_manager', environment_managers)
@pytest.mark.parametrize('template_version', template_version_politics)
def test_project_functions(
    setup, teardown, get_pip_libraries, get_conda_libraries,
    python_version, environment_manager, template_version
):

    cwd = setup()
    project_name = "test_project"
    project_folder = cwd / project_name

    notebook_pattern = str(project_folder / "notebooks" / "**")

    # Set up config conditions
    SettingsManager.change_template_version_policy(template_version)
    SettingsManager.change_environment_manager(environment_manager)
    SettingsManager.change_default_python_version(python_version)
    SettingsManager.change_handover_file_size_limit(10.0)

    try:
        start_new_project(project_name, working_directory=cwd)

        assert (project_folder / "notebooks").is_dir()
        assert (project_folder / "data").is_dir()

        n_files_notebooks_before = len(glob.glob(notebook_pattern, recursive=True))

        # assert folders are not empty
        assert n_files_notebooks_before > 0

        # assert venv/conda folder
        libraries_before = []
        if environment_manager == VENV:
            libraries_before = get_pip_libraries(project_folder)
            assert (project_folder / VENV_FOLDER).is_dir()
        elif environment_manager == CONDA:
            libraries_before = get_conda_libraries(project_folder)
            assert (project_folder / CONDA_FOLDER).is_dir()

        add_library_selecting_version(
            working_directory=project_folder,
            menu_way=[dataviz, "seaborn"],
            version="0.11.0"
        )

        # assert venv/conda folder
        libraries_after = []
        if environment_manager == VENV:
            libraries_after = get_pip_libraries(project_folder)
        elif environment_manager == CONDA:
            libraries_after = get_conda_libraries(project_folder)

        assert "seaborn" not in libraries_before
        assert "seaborn" in libraries_after

        with open(project_folder / "requirements.txt", "r", encoding="UTF-8") as f:
            assert "seaborn==0.11.0" in f.read()

        generate_template(working_directory=project_folder)

        # assert the number of files changed after rendering the template
        n_files_notebooks_after = len(glob.glob(notebook_pattern, recursive=True))
        assert n_files_notebooks_after > n_files_notebooks_before

    finally:
        teardown()
        # pass


@pytest.mark.parametrize('lib_install', lib_install_method)
def test_add_methods(
    setup, teardown, get_pip_libraries, get_conda_libraries,
    lib_install
):

    cwd = setup()
    project_name = "test_project"
    project_folder = cwd / project_name

    notebook_pattern = str(project_folder / "notebooks" / "**")

    # Set up config conditions
    SettingsManager.change_environment_manager(VENV)
    SettingsManager.change_default_python_version(SYSTEM_DEFAULT)

    try:
        start_new_project(project_name, working_directory=cwd)

        assert (project_folder / "notebooks").is_dir()
        assert (project_folder / "data").is_dir()

        n_files_notebooks_before = len(glob.glob(notebook_pattern, recursive=True))

        # assert folders are not empty
        assert n_files_notebooks_before > 0

        # assert venv/conda folder
        libraries_before = get_pip_libraries(project_folder)
        assert (project_folder / VENV_FOLDER).is_dir()

        if lib_install == "type":
            add_library_typing(working_directory=project_folder, library="seaborn")

        elif lib_install == "select":
            add_library_from_menu(
                working_directory=project_folder,
                tree_way=[dataviz, "seaborn"]
            )

        elif lib_install == "version":
            add_library_selecting_version(
                working_directory=project_folder,
                menu_way=[dataviz, "seaborn"],
                version="0.11.0"
            )
        libraries_after = get_pip_libraries(project_folder)

        assert "seaborn" not in libraries_before
        assert "seaborn" in libraries_after

    finally:
        teardown()
