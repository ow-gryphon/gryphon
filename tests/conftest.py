import glob
import logging
import os
import platform
from os import path
from pathlib import Path
from typing import List

import pytest

from gryphon.logger import logger
from gryphon.constants import GRYPHON_RC
from .utils import (
    remove_folder,
    create_folder,
    get_data_folder,
    get_venv_path, get_conda_path,
    create_folder_with_venv,
    get_pip_path,
    activate_venv
)

# logger = logging.getLogger('gryphon')
INIT_PATH = Path.cwd()
SANDBOX_PATH = Path("sandbox")


@pytest.fixture
def setup() -> callable:

    def _setup() -> Path:
        handler = list(filter(lambda x: x.name == "console", logger.handlers))[0]
        handler.setLevel(logging.DEBUG)

        if SANDBOX_PATH.is_dir():
            remove_folder(SANDBOX_PATH)
        create_folder(SANDBOX_PATH)
        os.chdir(SANDBOX_PATH)
        with open(GRYPHON_RC, "w") as f:
            f.write("{}")

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
def get_conda_libraries() -> callable:

    def _get_libraries(folder=Path.cwd()) -> str:
        conda_path = get_conda_path(base_folder=folder)
        return os.popen(f"conda list --explicit --prefix {conda_path}").read()

    return _get_libraries


@pytest.fixture
def data_folder() -> Path:
    return get_data_folder()


@pytest.fixture
def install_gryphon():

    def _install_gryphon(cwd):
        create_folder_with_venv(cwd)
        pip_path = get_pip_path(cwd)

        activate_venv()
        os.system(f"""{pip_path} install ../""")

    return _install_gryphon
