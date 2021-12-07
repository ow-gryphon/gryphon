"""
Utility functions for the test suite.
"""

from pathlib import Path
import platform
import shutil
from labskit_commands.command_operations import (
    create_venv,
    get_destination_path
)

TEST_FOLDER = Path("tests").resolve()
VENV = ".venv"


def remove_folder(folder):
    """
    Removes a folder (location relative to cwd or absolute).
    """
    shutil.rmtree(folder, ignore_errors=True)


def create_folder(folder: Path):
    """
    Create a folder in the given path (location relative to cwd or absolute).
    """
    folder.mkdir(exist_ok=True)


def create_folder_with_venv(folder_name: Path = Path.cwd(), requirements=None):
    """
    Creates a folder, creates a venv inside it and copies a sample requirements.txt file.
    """
    create_folder(folder_name)
    create_venv(folder_name)
    if requirements is None:
        requirements = get_data_folder() / "sample_requirements.txt"

    destination = get_destination_path(folder_name)
    shutil.copyfile(
        src=requirements,
        dst=destination / "requirements.txt"
    )


def get_data_folder() -> Path:
    return TEST_FOLDER / "data"


def get_pip_path(base_folder=Path.cwd()):
    if platform.system() == "Windows":
        # On windows the venv folder structure is different from unix
        pip_path = base_folder / VENV / "Scripts" / "pip.exe"
    else:
        pip_path = base_folder / VENV / "bin" / "pip"

    return pip_path


def get_requirements_path(base_folder: Path):
    return base_folder / "requirements.txt"


def get_venv_path(base_folder: Path) -> Path:
    return base_folder / VENV
