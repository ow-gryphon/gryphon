"""
Utility functions for the test suite.
"""

import os
from os import path
import platform
import shutil
from labskit_commands.command_operations import (
    create_venv,
    get_destination_path,
    escape_windows_path
)

TEST_FOLDER = os.path.abspath("tests")
VENV = ".venv"


def remove_folder(folder):
    """
    Removes a folder (location relative to cwd or absolute).
    """
    shutil.rmtree(folder, ignore_errors=True)


def create_folder(folder):
    """
    Create a folder in the given path (location relative to cwd or absolute).
    """
    os.makedirs(folder, exist_ok=True)


def create_folder_with_venv(folder_name, requirements=None):
    """
    Creates a folder, creates a venv inside it and copies a sample requirements.txt file.
    """
    create_folder(folder_name)
    create_venv(folder_name)
    if requirements is None:
        requirements = os.path.join(get_data_folder(), "sample_requirements.txt")

    destination = get_destination_path(folder_name)
    shutil.copyfile(
        src=requirements,
        dst=destination / "requirements.txt"
    )


def get_data_folder():
    return os.path.join(TEST_FOLDER, "data")


def get_pip_path(base_folder=""):
    if platform.system() == "Windows":
        # On windows the venv folder structure is different from unix
        pip_path = path.join(base_folder, VENV, "Scripts", "pip")
        pip_path = escape_windows_path(pip_path)
    else:
        pip_path = path.join(base_folder, VENV, "bin", "pip")

    return pip_path


def get_requirements_path(base_folder):
    requirements_path = path.join(base_folder, "requirements.txt")

    if platform.system() == "Windows":
        requirements_path = escape_windows_path(requirements_path)

    return requirements_path


def get_venv_path(base_folder):
    return path.join(base_folder, VENV)
