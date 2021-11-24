"""
Module containing tests about the functions in the file command_operations.py
"""
import os
from os import path
import shutil
import glob
import subprocess
import pytest
from .utils import create_folder, remove_folder, create_folder_with_venv
from labskit_commands.command_operations import (
    create_venv,
    install_libraries,
    copy_project_template,
    init_new_git_repo,
    initial_git_commit
)

VENV = ".venv"
CWD = os.path.abspath("")


def test_create_venv_1():
    """
    Test case:
    A venv is created successfully, in a previously created folder.
    """
    folder_name = "test_temp"

    create_folder(folder_name)
    abs_path = path.abspath(folder_name)
    try:
        create_venv(folder_name)

        venv_path = path.join(abs_path, VENV)

        assert path.isdir(venv_path)

    finally:
        remove_folder(abs_path)


def test_create_venv_2():
    """
    Test case:
    A venv is created in a folder that does not exists previously.
    """
    folder_name = "not_exists"
    folder_path = path.abspath(folder_name)
    try:
        create_venv(folder_path)

        venv_path = path.join(folder_path, VENV)
        assert path.isdir(venv_path)
    finally:
        remove_folder(folder_path)


def test_install_libraries_1():
    """
    Test case:
    In a prepared folder with venv, install libraries from the requirements.txt
    """
    folder_name = "install_libs_test"
    folder_path = path.abspath(folder_name)

    create_folder_with_venv(folder_path)
    try:
        install_libraries(folder_path)
        venv_path = path.join(folder_path, VENV)
        assert path.isdir(venv_path)

        glob_pattern = path.join(venv_path, "lib*", "python*", "site-packages", "*")
        lib_folders = glob.glob(glob_pattern)
        libs = list(map(path.basename, lib_folders))
        assert "pandas" in libs
        assert "numpy" in libs

    finally:
        remove_folder(folder_path)


def test_install_libraries_2():
    """
    Test case:
    In an empty folder try install libraries from the requirements.txt
    should raise error.
    """
    folder_name = "install_libs_test"
    folder_path = path.abspath(folder_name)

    create_folder(folder_path)
    try:
        with pytest.raises(FileNotFoundError):
            install_libraries(folder_path)

    finally:
        remove_folder(folder_path)


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
        remove_folder(absolute_folder_path)


def test_git_init_1():
    test_folder = "repo_test"
    init_folder = os.getcwd()
    sample_file = path.join(CWD, "tests", "data", "sample_template")
    destination_file = path.join(CWD, test_folder, "sample_template")
    git_path = path.join(CWD, test_folder, ".git")
    remove_folder(test_folder)
    try:
        create_folder(test_folder)
        shutil.copyfile(
            src=sample_file,
            dst=destination_file,
        )
        assert not path.isdir(git_path)
        init_new_git_repo(test_folder)
        assert path.isdir(git_path)
        os.chdir(test_folder)
        logs = subprocess.run(
            ['git', 'log'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ).stdout.decode()

        assert "does not have any commits yet" in logs

    finally:
        os.chdir(init_folder)
        remove_folder(test_folder)


def test_git_commit_1():
    test_folder = "repo_test"
    init_folder = os.getcwd()
    sample_file = path.join(CWD, "tests", "data", "sample_template")
    destination_file = path.join(CWD, test_folder, "sample_template")
    git_path = path.join(CWD, test_folder, ".git")

    create_folder(test_folder)
    shutil.copyfile(
        src=sample_file,
        dst=destination_file,
    )
    try:
        init_new_git_repo(test_folder)
        assert path.isdir(git_path)
        initial_git_commit(test_folder)

        os.chdir(test_folder)
        logs = subprocess.run(
            ['git', 'log'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ).stdout.decode()
        print(logs)
        assert "Initial commit" in logs
    finally:
        os.chdir(init_folder)
        remove_folder(test_folder)
