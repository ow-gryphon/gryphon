import glob
import shutil
import zipfile
from pathlib import Path

import pytest
import yaml

from gryphon.constants import (
    CONDA, VENV, SYSTEM_DEFAULT, USE_LATEST, VENV_FOLDER, CONDA_FOLDER
)
from gryphon.core.operations import SettingsManager
from .ui_interaction.generate import generate_template
from .ui_interaction.handover import generate_handover_package
from .ui_interaction.init import start_new_project

environment_managers = [CONDA, VENV]
SAMPLE_REQUIREMENTS = "sample_requirements.txt"


@pytest.mark.parametrize('environment_manager', environment_managers)
@pytest.mark.parametrize('file_size_limit', [0, 0.25, 10])
@pytest.mark.parametrize('include_gryphon_files', [True, False])
@pytest.mark.parametrize('change_settings', [None, "change_size_limit", "change_gryphon_politics"])
def test_handover(
        setup, teardown, data_folder,
        environment_manager, file_size_limit, include_gryphon_files, change_settings
):

    cwd = setup()
    project_name = "test_project"
    project_folder = cwd / project_name

    notebook_pattern = str(project_folder / "notebooks" / "**")

    # Set up config conditions
    SettingsManager.change_template_version_policy(USE_LATEST)
    SettingsManager.change_default_python_version(SYSTEM_DEFAULT)
    SettingsManager.change_environment_manager(environment_manager)
    SettingsManager.change_handover_file_size_limit(10.0)
    SettingsManager.change_handover_include_gryphon_generated_files(True)

    try:
        start_new_project(project_name, working_directory=cwd)

        assert (project_folder / "notebooks").is_dir()
        assert (project_folder / "data").is_dir()

        n_files_notebooks_before = len(glob.glob(notebook_pattern, recursive=True))

        # assert folders are not empty
        assert n_files_notebooks_before > 0

        # assert venv/conda folder
        if environment_manager == VENV:
            assert (project_folder / VENV_FOLDER).is_dir()
        elif environment_manager == CONDA:
            assert (project_folder / CONDA_FOLDER).is_dir()

        generate_template(working_directory=project_folder)

        # assert the number of files changed after rendering the template
        n_files_notebooks_after = len(glob.glob(notebook_pattern, recursive=True))
        assert n_files_notebooks_after > n_files_notebooks_before

        shutil.copy(data_folder / SAMPLE_REQUIREMENTS, project_folder / SAMPLE_REQUIREMENTS)

        generate_handover_package(
            working_directory=cwd,
            handover_folder=project_folder,
            change_configs=change_settings,
            file_size_limit=file_size_limit,
            include_gryphon_files=include_gryphon_files
        )

        zip_path = glob.glob(str(cwd / "**.zip"))[0]
        logfile = zip_path[:-4] + "_log.txt"

        assert Path(zip_path).is_file()
        assert Path(logfile).is_file()

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall("unziped")

        unzip_folder = cwd / "unziped" / project_name

        with open(logfile, "r") as f:
            data = yaml.load(
                stream=f,
                Loader=yaml.FullLoader
            )

        assert "excluded_large_files" in data
        assert "excluded_gryphon_files" in data

        assert "file_size_limit" in data
        assert "keep_gryphon_files" in data

        for file in data["excluded_large_files"]:
            assert not Path(unzip_folder / file).is_file()

        for file in data["excluded_gryphon_files"]:
            assert not Path(unzip_folder / file).is_file()

        unzipped_notebook = (unzip_folder / "notebooks" / "data_exploration.ipynb")

        if change_settings is None:
            # pass
            assert unzipped_notebook.is_file()
        elif change_settings == "change_size_limit":
            if file_size_limit == 0.25:
                assert not unzipped_notebook.is_file()
            else:
                assert unzipped_notebook.is_file()

        elif change_settings == "change_gryphon_politics":
            if include_gryphon_files:
                assert unzipped_notebook.is_file()
            else:
                assert not unzipped_notebook.is_file()

        assert (unzip_folder / SAMPLE_REQUIREMENTS).is_file()

    finally:
        teardown()
        # pass
