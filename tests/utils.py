"""
Utility functions for the test suite.
"""

import os
import shutil
from labskit_commands.command_operations import (
    create_venv,
    get_destination_path
)

TEST_FOLDER = os.path.abspath("tests")


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
        dst=os.path.join(destination, "requirements.txt")
    )


def get_data_folder():
    return os.path.join(TEST_FOLDER, "data")
