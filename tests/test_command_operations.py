"""
Module containing tests about the functions in the file common_operations.py
"""
import json
import os
from pathlib import Path
from os import path
import shutil
import subprocess
import pytest
from .utils import (
    create_folder_with_venv, create_folder_with_conda_env,
    get_venv_path, get_conda_path,
    TEST_FOLDER
)
from gryphon.core.registry import Template
from gryphon.core.operations.environment_manager_operations import EnvironmentManagerOperations
from gryphon.core.operations.bash_utils import BashUtils

from gryphon.core.common_operations import (
    init_new_git_repo,
    initial_git_commit,
    log_new_files
)


CWD = os.path.abspath("")


def test_create_venv_1(setup, teardown):
    """
    Test case:
    A venv is created successfully, in a previously created folder.
    """
    cwd = setup()
    try:
        EnvironmentManagerOperations.create_venv(cwd)

        venv_path = get_venv_path(base_folder=cwd)

        assert path.isdir(venv_path)

    finally:
        teardown()


def test_create_venv_2(setup, teardown):
    """
    Test case:
    A venv is created in a folder that does not exists previously.
    """
    cwd = setup()
    try:
        EnvironmentManagerOperations.create_venv(cwd)

        venv_path = get_venv_path(cwd)
        assert path.isdir(venv_path)
    finally:
        teardown()


def test_create_conda_env_1(setup, teardown):
    """
    Test case:
    A venv is created in a folder that does not exists previously.
    """
    cwd = setup()
    try:
        conda_path = get_conda_path(cwd)
        venv_path = get_venv_path(cwd)
        EnvironmentManagerOperations.create_conda_env(cwd)

        assert path.isdir(conda_path)
        assert not path.isdir(venv_path)
    finally:
        teardown()


def test_create_conda_env_2(setup, teardown):
    """
    Test case:
    A venv is created in a folder that does not exists previously.
    """
    cwd = setup()
    try:
        conda_path = get_conda_path(cwd)
        venv_path = get_venv_path(cwd)
        EnvironmentManagerOperations.create_venv(cwd)

        assert not path.isdir(conda_path)
        assert path.isdir(venv_path)
    finally:
        teardown()


def test_install_libraries_1(setup, teardown, get_pip_libraries):
    """
    Test case:
    In a prepared folder with venv, install libraries from the requirements.txt
    """
    cwd = setup()

    create_folder_with_venv(cwd)
    try:

        libs = get_pip_libraries(cwd)
        assert "numpy" not in libs

        EnvironmentManagerOperations.install_libraries_venv(cwd)
        venv_path = get_venv_path(cwd)
        assert venv_path.is_dir()

        libs = get_pip_libraries(cwd)
        assert "numpy" in libs

    finally:
        teardown()


def test_install_libraries_2(setup, teardown):
    """
    Test case:
    In an empty folder try to install libraries from the requirements.txt
    should raise error.
    """
    folder_path = setup()

    try:
        with pytest.raises(RuntimeError):
            EnvironmentManagerOperations.install_libraries_venv(folder_path)

    finally:
        teardown()


def test_install_libraries_conda_1(setup, teardown, get_conda_libraries):
    """
    Test case:
    In a prepared folder with venv, install libraries from the requirements.txt
    """
    cwd = setup()

    create_folder_with_conda_env(folder_name=cwd)
    try:

        libs = get_conda_libraries(cwd)
        assert "numpy" not in libs
        assert "pandas" not in libs

        EnvironmentManagerOperations.install_libraries_conda(cwd)
        conda_path = get_conda_path(cwd)
        assert conda_path.is_dir()

        libs = get_conda_libraries(cwd)
        assert "numpy" in libs
        assert "pandas" in libs

    finally:
        teardown()


def test_copy_project_template(setup, teardown):
    """
    Tests if the template folder is being properly copied.
    """
    pwd = Path(setup())

    BashUtils.copy_project_template(
        template_source=Path(TEST_FOLDER) / "data" / "trivial",
        template_destiny=pwd
    )

    try:
        assert pwd.is_dir()
        assert (pwd / "requirements.txt").is_file()
        assert (pwd / "sample_template").is_file()

    finally:
        teardown()


def test_git_init_1(setup, teardown):
    sample_file = path.join(TEST_FOLDER, "data", "sample_template")
    cwd = setup()

    destination_file = path.join(cwd, "sample_template")
    git_path = path.join(cwd, ".git")

    try:
        shutil.copyfile(
            src=sample_file,
            dst=destination_file,
        )
        assert not path.isdir(git_path)

        init_new_git_repo(cwd)

        assert path.isdir(git_path)

        logs = subprocess.run(
            ['git', 'log'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ).stdout.decode()

        assert "does not have any commits yet" in logs

    finally:
        teardown()


def test_git_commit_1(setup, teardown):
    sample_file = path.join(TEST_FOLDER, "data", "sample_template")
    cwd = setup()

    destination_file = path.join(cwd, "sample_template")
    git_path = path.join(cwd, ".git")

    shutil.copyfile(
        src=sample_file,
        dst=destination_file,
    )
    try:
        repo = init_new_git_repo(cwd)
        assert path.isdir(git_path)

        initial_git_commit(repo)
        logs = subprocess.run(
            ['git', 'log'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ).stdout.decode()
        assert "Initial commit" in logs

    finally:
        teardown()


def test_log_new_files(setup, teardown):
    cwd = setup()
    log_file = cwd / "sample_log"
    with open(log_file, "w") as f:
        f.write("{}")

    try:
        template_path = TEST_FOLDER / "data" / "trivial"
        template = Template.template_from_path(template_path)

        log_new_files(
            template=template,
            performed_action="init",
            logfile=log_file
        )

        with open(log_file, "r") as f:
            contents = json.load(f)
            assert "files" in contents
            assert len(contents["files"]) == 2
            for files in contents["files"]:
                assert "/home/" not in files["path"]

    finally:
        teardown()
