"""
File containing operations that are common to the commands.
"""

import os
from pathlib import Path
import platform
import subprocess
import shutil
import git
from .logging import Logging


VENV = ".venv"


def get_destination_path(folder=None) -> Path:
    """
    Function that helps to define the full path to a directory.

    It checks if the path is an absolute or relative path, then
    if relative, it appends the current folder to it, transforming
    it into a absolute path.
    """
    if folder is None:
        return Path.cwd()

    path_obj = Path(folder)

    if not path_obj.is_absolute():
        return path_obj.resolve()

    return path_obj


def create_venv(folder=None):
    """Function to a virtual environment inside a folder."""
    target_folder = get_destination_path(folder)
    venv_path = target_folder / VENV

    # Create venv
    Logging.log(f"Creating virtual environment on {venv_path}")
    os.system(f"python -m venv \"{venv_path}\"")
    Logging.log("Done creating venv.", fg='green')


def quote_windows_path(folder_path):
    return '"' + folder_path + '"'


def escape_windows_path(folder_path):
    return fr'{folder_path}'


def install_libraries(folder=None):
    """
    Function to install the libraries from a 'requirements.txt' file
    """
    target_folder = get_destination_path(folder)
    requirements_path = target_folder / "requirements.txt"

    if platform.system() == "Windows":
        # On windows the venv folder structure is different from unix
        pip_path = target_folder / VENV / "Scripts" / "pip.exe"
    else:
        pip_path = target_folder / VENV / "bin" / "pip"

    # Install requirements
    Logging.log("Installing requirements. This may take some minutes ...")

    if not pip_path.is_file():
        raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}")
    
    if not requirements_path.is_file():
        raise FileNotFoundError("requirements.txt file not found.")

    try:
        subprocess.check_call([str(pip_path), 'install', '-r', str(requirements_path), '-qqq'])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed on pip install command. {e}")

    Logging.log("Installation succeeded.", fg='green')


def copy_project_template(template_source: str, template_destiny: str):
    """Copies the templates to destination folder."""

    template_path = template_source / "template"
    template_path.mkdir(exist_ok=True)
    
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
    requirements_path = current_path / "requirements.txt"
    with open(requirements_path, "a", encoding='UTF-8') as file:
        file.write(f"\n{library_name}")


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
