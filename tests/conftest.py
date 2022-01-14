import os
import platform
from pathlib import Path
from os import path
import glob
import pytest
from typing import List
from .utils import (
    remove_folder,
    create_folder,
    get_data_folder,
    get_venv_path
)

INIT_PATH = Path.cwd()
SANDBOX_PATH = Path("sandbox")


@pytest.fixture
def setup() -> callable:

    def _setup() -> Path:
        if SANDBOX_PATH.is_dir():
            remove_folder(SANDBOX_PATH)
        create_folder(SANDBOX_PATH)
        os.chdir(SANDBOX_PATH)
        return Path.cwd()
    return _setup


@pytest.fixture
def teardown() -> callable:

    def _teardown():
        os.chdir(INIT_PATH)
        remove_folder(SANDBOX_PATH.resolve())

    return _teardown


@pytest.fixture
def get_pip_libraries() -> callable:

    def _get_libraries(folder=Path.cwd()) -> List[str]:
        venv_path = get_venv_path(base_folder=folder)
        if platform.system() == "Windows":
            glob_pattern = venv_path / "Lib" / "site-packages" / "*"
        else:
            glob_pattern = venv_path / "lib*" / "python*" / "site-packages" / "*"

        lib_folders = glob.glob(str(glob_pattern))
        libs = list(map(path.basename, lib_folders))

        return libs

    return _get_libraries


@pytest.fixture
def data_folder() -> Path:
    return get_data_folder()
