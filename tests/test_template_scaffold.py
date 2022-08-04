import json

import pytest

from gryphon.constants import (
    CONDA, VENV, SYSTEM_DEFAULT, ALWAYS_ASK,
    USE_LATEST
)
from gryphon.core.operations import SettingsManager
from .ui_interaction.advanced_options import create_template_scaffold

python_versions = [SYSTEM_DEFAULT, ALWAYS_ASK]
environment_managers = [CONDA, VENV]
template_version_politics = [ALWAYS_ASK, USE_LATEST]
SAMPLE_REQUIREMENTS = "sample_requirements.txt"


@pytest.mark.parametrize('python_version', python_versions)
@pytest.mark.parametrize('environment_manager', environment_managers)
@pytest.mark.parametrize('template_version', template_version_politics)
def test_template_functions(
        setup, teardown,
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
