"""
Utility functions for the test suite.
"""

import os
from labskit_commands.command_operations import (
    create_venv, get_destination_path)


def remove_folder(folder):
    """
    Removes a folder (location relative to cwd or absolute).
    """
    os.system(f"rm -rf {folder}")


def create_folder(folder):
    """
    Create a folder in the given path (location relative to cwd or absolute).
    """
    os.system(f"mkdir -p {folder}")


def create_folder_with_venv(folder_name, requirements=None):
    """
    Creates a folder, creates a venv inside it and copies a sample requirements.txt file.
    """
    create_folder(folder_name)
    create_venv(folder_name)
    if requirements is None:
        requirements = os.path.join(os.getcwd(), "tests/data/sample_requirements.txt")

    destination = get_destination_path(folder_name)
    os.system(f"cp {requirements} {destination}/requirements.txt")
