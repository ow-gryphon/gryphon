import os
from os import path
import glob
import pytest
from .utils import (
    remove_folder,
    create_folder,
    get_data_folder,
    get_pip_path,
    get_venv_path
)

INIT_PATH = os.getcwd()
SANDBOX_PATH = os.path.abspath("sandbox")


@pytest.fixture
def setup():

    def _setup():
        remove_folder(SANDBOX_PATH)
        create_folder(SANDBOX_PATH)
        os.chdir(SANDBOX_PATH)
        return SANDBOX_PATH
    return _setup


@pytest.fixture
def teardown():

    def _teardown():
        os.chdir(INIT_PATH)
        remove_folder(SANDBOX_PATH)

    return _teardown


@pytest.fixture
def get_pip_libraries():

    def _get_libraries(folder=""):
        venv_path = get_venv_path(base_folder=folder)

        glob_pattern = path.join(venv_path, "lib*", "python*", "site-packages", "*")
        lib_folders = glob.glob(glob_pattern)
        libs = list(map(path.basename, lib_folders))

        return libs

    return _get_libraries


@pytest.fixture
def data_folder():
    return get_data_folder()
