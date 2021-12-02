"""
File containing operations that are common to the commands.
"""

import os
from os import path
import platform
import shutil
import subprocess
import git
import click


PACKAGE_PATH = path.dirname(path.realpath(__file__))
VENV = ".venv"


def get_destination_path(folder=None):
    """
    Function that helps to define the full path to a directory.

    It checks if the path is an absolute or relative path, then
    if relative, it appends the current folder to it, transforming
    it into a absolute path.
    """
    if folder is None:
        return os.getcwd()

    is_absolute_path = path.isabs(folder)

    if not is_absolute_path:
        folder = path.abspath(folder)

    return folder


def create_venv(folder=None):
    """Function to a virtual environment inside a folder."""
    target_folder = get_destination_path(folder)
    venv_path = path.join(target_folder, VENV)

    # Create venv
    click.echo("Creating virtual environment.")
    os.system(f"python -m venv {venv_path}")


def escape_windows_path(folder_path):
    return '"' + folder_path + '"'


def install_libraries(folder=None):
    """
    Function to install the libraries from a 'requirements.txt' file
    """
    target_folder = get_destination_path(folder)
    requirements_path = path.join(target_folder, "requirements.txt")

    if platform.system() == "Windows":
        # On windows the venv folder structure is different from unix
        pip_path = path.join(target_folder, VENV, "Scripts", "pip")

        # On windows "" double quotes are needed to avoid problems with special chars
        pip_path = escape_windows_path(pip_path)
        requirements_path = escape_windows_path(requirements_path)
    else:
        pip_path = path.join(target_folder, VENV, "bin", "pip")

    # Install requirements
    click.echo("Installing requirements. This may take some minutes ...")

    if not os.path.isfile(pip_path):
        raise RuntimeError(f"virtualenv not found inside folder. Should be at {pip_path}")

    if not os.path.isfile(requirements_path):
        raise FileNotFoundError("requirements.txt file not found.")

    try:
        subprocess.check_output(
            f"{pip_path} --disable-pip-version-check "
            f"install -r {requirements_path}", shell=True)
    except subprocess.CalledProcessError:
        click.secho("Failed to install requirements", fg='red')
        raise RuntimeError("Failed on pip install command.")

    click.secho("Installation succeeded.", fg='green')


# def copy_project_template(registry: str, command: str, template: str, folder: str):
def copy_project_template(template_source: str, template_destiny: str):
    """Copies the templates to destination folder."""
    template_path = path.join(template_source, "template")
    # target_path = get_destination_path(folder)

    os.makedirs(template_destiny, exist_ok=True)
    shutil.copytree(
        src=template_path,
        dst=template_destiny,
        dirs_exist_ok=True
    )


def init_new_git_repo(folder: os.path) -> git.Repo:
    """Init new git repository on folder."""
    return git.Repo.init(folder)


def initial_git_commit(repository: git.Repo):
    """Does the first git commit."""
    repository.git.add(A=True)
    repository.index.commit("Initial commit")


def append_requirement(library_name):
    """Appends a given requirement to the requirements.txt file."""

    current_path = get_destination_path()
    requirements_path = os.path.join(current_path, "requirements.txt")
    with open(requirements_path, "a", encoding='UTF-8') as file:
        file.write(f"\n{library_name}")
