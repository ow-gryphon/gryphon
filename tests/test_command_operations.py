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

        path = os.path.join(os.getcwd(), folder_name)
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

    try:
        create_venv(folder_name)

        venv_path = os.path.join(os.getcwd(), folder_name, ".venv")
        assert os.path.isdir(venv_path)
    finally:
        path = os.path.join(os.getcwd(), folder_name)
        utils.remove_folder(path)


def test_install_libraries_1():
    """
    Test case:
    In a prepared folder with venv, install libraries from the requirements.txt
    """
    folder_name = "install_libs_test"
    utils.create_folder_with_venv(folder_name)
    try:
        install_libraries(folder_name)
        venv_path = os.path.join(os.getcwd(), folder_name, ".venv")
        assert os.path.isdir(venv_path)

        lib_folders = glob.glob(f"{venv_path}/lib*/python*/site-packages/*")
        libs = list(map(lambda x: x.split("/")[-1], lib_folders))
        assert "pandas" in libs
        assert "numpy" in libs

    finally:
        path = os.path.join(os.getcwd(), folder_name)
        utils.remove_folder(path)


def test_install_libraries_2():
    """
    Test case:
    In an empty folder try install libraries from the requirements.txt
    should raise error.
    """
    folder_name = "install_libs_test"
    utils.create_folder(folder_name)
    try:
        with pytest.raises(FileNotFoundError):
            install_libraries(folder_name)

    finally:
        path = os.path.join(os.getcwd(), folder_name)
        utils.remove_folder(path)
