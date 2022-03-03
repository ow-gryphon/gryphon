import json
import shutil

from gryphon.core.settings import SettingsManager
from .utils import TEST_FOLDER, CONFIG_FILE_NAME, MOCK_CONFIG_FILE_PATH


def base_test(function):

    def _test(setup, teardown, *args, **kwargs):
        try:
            cwd = setup()
            function(cwd, *args, **kwargs)
        finally:
            teardown()

    return _test


def test_restore_default_settings(setup, teardown, mocker):
    try:
        cwd = setup()
        file = cwd / CONFIG_FILE_NAME
        shutil.copy(
            src=TEST_FOLDER / "data" / CONFIG_FILE_NAME,
            dst=file
        )

        with mocker.patch(
                target=MOCK_CONFIG_FILE_PATH,
                return_value=file
        ):

            with open(file, "r") as f:
                data = json.load(f)
                # I put this argument inside the test file just to verify it
                assert "this_is_just_a_test" in data
                assert data["environment_management"] == "conda"

            manager = SettingsManager()
            manager.restore_default_config_file()

            with open(file, "r") as f:
                data = json.load(f)
                assert "this_is_just_a_test" not in data
                # venv should be the default env manager
                assert data["environment_management"] == "venv"

    finally:
        teardown()


def test_change_environment_manager(setup, teardown, mocker):
    try:
        cwd = setup()
        file = cwd / CONFIG_FILE_NAME
        shutil.copy(
            src=TEST_FOLDER / "data" / CONFIG_FILE_NAME,
            dst=file
        )

        with mocker.patch(
                target=MOCK_CONFIG_FILE_PATH,
                return_value=file
        ):

            with open(file, "r") as f:
                data = json.load(f)
                # I put this argument inside the test file just to verify it
                assert data["environment_management"] == "conda"

            manager = SettingsManager()
            manager.change_environment_manager("venv")

            with open(file, "r") as f:
                data = json.load(f)
                # venv should be the default env manager
                assert data["environment_management"] == "venv"

    finally:
        teardown()


def test_add_git_template_registry(setup, teardown, mocker):
    url = "https://github.com/SAMPLE_USER/SAMPLE_REPO"
    name = "sample registry"
    try:
        cwd = setup()
        file = cwd / CONFIG_FILE_NAME
        shutil.copy(
            src=TEST_FOLDER / "data" / CONFIG_FILE_NAME,
            dst=file
        )

        with mocker.patch(
                target=MOCK_CONFIG_FILE_PATH,
                return_value=file
        ):

            with open(file, "r") as f:
                data = json.load(f)
                # I put this argument inside the test file just to verify it
                assert "git_registry" in data
                assert "open-source" in data["git_registry"].keys()

            manager = SettingsManager()
            manager.add_git_template_registry(
                registry_repo=url,
                registry_name=name
            )

            with open(file, "r") as f:
                data = json.load(f)
                # venv should be the default env manager
                assert "git_registry" in data
                assert name in data["git_registry"].keys()
                assert data["git_registry"][name] == url

    finally:
        teardown()


def test_add_local_template_registry(setup, teardown, mocker):
    path = "/path/to/repo"
    name = "sample registry"
    try:
        cwd = setup()
        file = cwd / CONFIG_FILE_NAME
        shutil.copy(
            src=TEST_FOLDER / "data" / CONFIG_FILE_NAME,
            dst=file
        )

        with mocker.patch(
                target=MOCK_CONFIG_FILE_PATH,
                return_value=file
        ):

            with open(file, "r") as f:
                data = json.load(f)

                assert "local_registry" in data
                assert "default_registry" in data["local_registry"].keys()

            manager = SettingsManager()
            manager.add_local_template_registry(
                registry_path=path,
                registry_name=name
            )

            with open(file, "r") as f:
                data = json.load(f)

                assert "local_registry" in data
                assert name in data["local_registry"].keys()
                assert data["local_registry"][name] == path

    finally:
        teardown()


def test_remove_template_registry(setup, teardown, mocker):
    name = "open-source"
    try:
        cwd = setup()
        file = cwd / CONFIG_FILE_NAME
        shutil.copy(
            src=TEST_FOLDER / "data" / CONFIG_FILE_NAME,
            dst=file
        )

        with mocker.patch(
                target=MOCK_CONFIG_FILE_PATH,
                return_value=file
        ):

            with open(file, "r") as f:
                data = json.load(f)

                assert "git_registry" in data
                assert name in data["git_registry"].keys()

            manager = SettingsManager()
            manager.remove_template_registry(registry_name=name)

            with open(file, "r") as f:
                data = json.load(f)

                assert "git_registry" in data
                assert name not in data["git_registry"].keys()

    finally:
        teardown()


def test_restore_registries(setup, teardown, mocker):
    name = "ow-private"
    try:
        cwd = setup()
        file = cwd / CONFIG_FILE_NAME
        shutil.copy(
            src=TEST_FOLDER / "data" / CONFIG_FILE_NAME,
            dst=file
        )

        with mocker.patch(
                target=MOCK_CONFIG_FILE_PATH,
                return_value=file
        ):

            with open(file, "r") as f:
                data = json.load(f)

                assert "git_registry" in data
                assert name not in data["git_registry"].keys()
                previous_manager = data["environment_management"]

            manager = SettingsManager()
            manager.restore_registries()

            with open(file, "r") as f:
                data = json.load(f)

                assert "git_registry" in data
                assert name in data["git_registry"].keys()
                assert data["environment_management"] == previous_manager

    finally:
        teardown()
