"""
Module containing tests about the functions in the file command_operations.py
"""
from os import path
import glob
import pytest
import utils
from labskit_commands.command_operations import (
    create_venv,
    install_libraries,
    copy_project_template
)


def test_create_venv_1():
    """
    Test case:
    A venv is created successfully, in a previously created folder.
    """
    folder_name = "test_temp"

    utils.create_folder(folder_name)
    abs_path = path.abspath(folder_name)
    try:
        create_venv(folder_name)

        venv_path = path.join(abs_path, ".venv")

        assert path.isdir(venv_path)

    finally:
        utils.remove_folder(abs_path)


def test_create_venv_2():
    """
    Test case:
    A venv is created in a folder that does not exists previously.
    """
    folder_name = "not_exists"
    folder_path = path.abspath(folder_name)
    try:
        create_venv(folder_path)

        venv_path = path.join(folder_path, ".venv")
        assert path.isdir(venv_path)
    finally:
        utils.remove_folder(folder_path)


def test_install_libraries_1():
    """
    Test case:
    In a prepared folder with venv, install libraries from the requirements.txt
    """
    folder_name = "install_libs_test"
    folder_path = path.abspath(folder_name)

    utils.create_folder_with_venv(folder_path)
    try:
        install_libraries(folder_path)
        venv_path = path.join(folder_path, ".venv")
        assert path.isdir(venv_path)

        glob_pattern = path.join(venv_path, "lib*", "python*", "site-packages", "*")
        lib_folders = glob.glob(glob_pattern)
        libs = list(map(path.basename, lib_folders))
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
    folder_path = path.abspath(folder_name)

    utils.create_folder(folder_path)
    try:
        with pytest.raises(FileNotFoundError):
            install_libraries(folder_path)

    finally:
        utils.remove_folder(folder_path)


def test_copy_project_template():
    """
    Tests if the template folder is being properly copied.
    """
    destination_folder = "trivial_template"
    copy_project_template(
        command="init",
        template="trivial",
        folder=destination_folder
    )

    absolute_folder_path = path.abspath(destination_folder)

    try:
        assert path.isdir(absolute_folder_path)
        assert path.isfile(path.join(absolute_folder_path, "requirements.txt"))
        assert path.isfile(path.join(absolute_folder_path, "sample_template"))

    finally:
        utils.remove_folder(absolute_folder_path)
