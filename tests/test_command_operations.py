"""
Module containing tests about the functions in the file command_operations.py
"""
import os
import glob
import pytest
import utils
from labskit_commands.command_operations import (
    create_venv,
    install_libraries
)


def test_create_venv_1():
    """
    Test case:
    A venv is created successfully, in a previously created folder.
    """
    folder_name = "test_temp"

    utils.create_folder(folder_name)
    try:
        create_venv(folder_name)

        path = os.path.abspath(folder_name)
        venv_path = os.path.join(path, ".venv")

        assert os.path.isdir(venv_path)

    finally:
        path = os.path.join(os.getcwd(), folder_name)
        utils.remove_folder(path)


def test_create_venv_2():
    """
    Test case:
    A venv is created in a folder that does not exists previously.
    """
    folder_name = "not_exists"
    folder_path = os.path.abspath(folder_name)
    try:
        create_venv(folder_path)

        venv_path = os.path.join(folder_path, ".venv")
        assert os.path.isdir(venv_path)
    finally:
        utils.remove_folder(folder_path)


def test_install_libraries_1():
    """
    Test case:
    In a prepared folder with venv, install libraries from the requirements.txt
    """
    folder_name = "install_libs_test"
    folder_path = os.path.abspath(folder_name)

    utils.create_folder_with_venv(folder_path)
    try:
        install_libraries(folder_path)
        venv_path = os.path.join(folder_path, ".venv")
        assert os.path.isdir(venv_path)

        glob_pattern = os.path.join(venv_path, "lib*", "python*", "site-packages", "*")
        lib_folders = glob.glob(glob_pattern)
        libs = list(map(os.path.basename, lib_folders))
        assert "pandas" in libs
        assert "numpy" in libs

    finally:
        utils.remove_folder(folder_path)


def test_install_libraries_2():
    """
    Test case:
    In an empty folder try install libraries from the requirements.txt
    should raise error.
    """
    folder_name = "install_libs_test"
    folder_path = os.path.abspath(folder_name)

    utils.create_folder(folder_path)
    try:
        with pytest.raises(FileNotFoundError):
            install_libraries(folder_path)

    finally:
        utils.remove_folder(folder_path)
