import glob
import json

import pytest

from gryphon.constants import CONDA, VENV, SYSTEM_DEFAULT, ALWAYS_ASK, USE_LATEST
from gryphon.core.settings import SettingsManager
from .ui_interaction.add import add_library_from_menu, add_library_typing, add_library_selecting_version
from .ui_interaction.advanced_options import create_template_scaffold
from .ui_interaction.generate import generate_template
from .ui_interaction.init import start_new_project

python_versions = [SYSTEM_DEFAULT, ALWAYS_ASK]
environment_managers = [CONDA, VENV]
template_version_politics = [ALWAYS_ASK, USE_LATEST]
lib_install_method = ["type", "select", "version"]


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
            assert (project_folder / ".venv").is_dir()
        elif environment_manager == CONDA:
            libraries_before = get_conda_libraries(project_folder)
            assert (project_folder / "envs").is_dir()

        add_library_selecting_version(
            working_directory=project_folder,
            menu_way=["Data Visualization", "seaborn"],
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
        pass
        # teardown()


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
        assert (project_folder / ".venv").is_dir()

        if lib_install == "type":
            add_library_typing(working_directory=project_folder, library="seaborn")

        elif lib_install == "select":
            add_library_from_menu(
                working_directory=project_folder,
                tree_way=["Data Visualization", "seaborn"]
            )

        elif lib_install == "version":
            add_library_selecting_version(
                working_directory=project_folder,
                menu_way=["Data Visualization", "seaborn"],
                version="0.11.0"
            )
        libraries_after = get_pip_libraries(project_folder)

        assert "seaborn" not in libraries_before
        assert "seaborn" in libraries_after

    finally:
        teardown()


@pytest.mark.parametrize('python_version', python_versions)
@pytest.mark.parametrize('environment_manager', environment_managers)
@pytest.mark.parametrize('template_version', template_version_politics)
def test_template_functions(
        setup, teardown, get_pip_libraries, get_conda_libraries,
        python_version, environment_manager, template_version
):

    cwd = setup()
    project_name = "test_template"
    project_folder = cwd / project_name

    # Set up config conditions
    SettingsManager.change_template_version_policy(template_version)
    SettingsManager.change_environment_manager(environment_manager)
    SettingsManager.change_default_python_version(python_version)

    try:
        create_template_scaffold(working_directory=cwd)
        assert (project_folder / "requirements.txt").is_file()
        assert (project_folder / "setup.py").is_file()
        assert (project_folder / "metadata.json").is_file()
        assert (project_folder / "README.md").is_file()

        assert (project_folder / "template").is_dir()

        with open(project_folder / "metadata.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # check mandatory fields
        required_fields = ["command", "display_name"]
        faulting_fields = []
        for field in required_fields:
            if field not in metadata:
                faulting_fields.append(field)

        if len(faulting_fields):
            raise AttributeError(f"Some required fields are not present in the metadata.json file: {faulting_fields}")

        # check field formats
        assert type(metadata["command"]) == str

        if "dependencies" in metadata:
            assert type(metadata["dependencies"]) == list

        if "topic" in metadata:
            assert type(metadata["topic"]) == list

        if "methodology" in metadata:
            assert type(metadata["methodology"]) == list

        if "keywords" in metadata:
            assert type(metadata["keywords"]) == list

        # check possible values of command field
        # assert metadata["command"] in ["init", "generate"]

    finally:
        SettingsManager.test_template_cleanup()
        teardown()
