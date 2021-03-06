import shutil

from gryphon.core import add
from gryphon.core.operations import RCManager
from .utils import (
    create_folder_with_venv, create_folder_with_conda_env,
    MOCK_CONFIG_FILE_PATH, CONFIG_FILE_NAME, TEST_FOLDER
)


def test_add_1(setup, teardown, get_pip_libraries, mocker):
    lib = "scipy"

    cwd = setup()

    file = cwd / CONFIG_FILE_NAME
    shutil.copy(
        src=TEST_FOLDER / "data" / "gryphon_config_venv.json",
        dst=file
    )

    with mocker.patch(
            target=MOCK_CONFIG_FILE_PATH,
            return_value=file
    ):

        try:
            create_folder_with_venv()
            add(library_name=lib, cwd=cwd)

            with open(cwd / "requirements.txt", encoding="UTF-8") as r:
                requirements = r.read()
                assert lib in requirements

            installed_libs = get_pip_libraries(cwd)

            assert lib in installed_libs

        finally:
            teardown()


def test_add_2(setup, teardown, get_conda_libraries, mocker):
    lib = "scipy"

    cwd = setup()

    try:

        create_folder_with_conda_env(cwd)
        RCManager.set_environment_manager("conda")
        RCManager.set_environment_manager_path(cwd / "envs")

        file = cwd / CONFIG_FILE_NAME
        shutil.copy(
            src=TEST_FOLDER / "data" / CONFIG_FILE_NAME,
            dst=file
        )

        with mocker.patch(
                target=MOCK_CONFIG_FILE_PATH,
                return_value=file
        ):

            add(library_name=lib, cwd=cwd)

        with open(cwd / "requirements.txt", encoding="UTF-8") as r:
            requirements = r.read()
            assert lib in requirements

        installed_libs = get_conda_libraries(cwd)

        assert lib in installed_libs

    finally:
        teardown()
