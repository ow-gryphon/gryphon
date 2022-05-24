import glob
import json
import os

import pytest

from gryphon.constants import CONDA, VENV, SYSTEM_DEFAULT, ALWAYS_ASK, USE_LATEST, REQUIREMENTS, GRYPHON_RC, YES
from gryphon.core.operations import RCManager
from gryphon.core.settings import SettingsManager
from .ui_interaction.add import add_library_from_menu, add_library_typing, add_library_selecting_version
from .ui_interaction.advanced_options import create_template_scaffold
from .ui_interaction.generate import generate_template
from .ui_interaction.init import start_new_project
from .ui_interaction.init_from_existing import start_project_from_existing
from .utils import create_folder_with_conda_env, create_folder_with_venv

python_versions = [SYSTEM_DEFAULT, ALWAYS_ASK]
environment_managers = [CONDA, VENV]
template_version_politics = [ALWAYS_ASK, USE_LATEST]
lib_install_method = ["type", "select", "version"]
dataviz = "Data Visualization"
seaborn = "seaborn"


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
    setup, teardown, get_pip_libraries, get_conda_libraries,
    environment_manager, uses_existing_env,
    point_external_env, has_existing_env
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
            assert previous_env_path == used_env_manager

        if point_external_env:
            assert external_env_path == used_env_manager

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
