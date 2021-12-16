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
REQUIREMENTS = "requirements.txt"


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
    Logging.log(f"Creating virtual environment in {venv_path}")
    os.system(f"python -m venv \"{venv_path}\"")
    Logging.log("Done creating virtual environment.", fg='green')


def quote_windows_path(folder_path):
    return '"' + folder_path + '"'


def escape_windows_path(folder_path):
    return fr'{folder_path}'


def install_libraries(folder=None):
    """
    Function to install the libraries from a 'requirements.txt' file
    """
    target_folder = get_destination_path(folder)
    requirements_path = target_folder / REQUIREMENTS

    if platform.system() == "Windows":
        # On windows the venv folder structure is different from unix
        pip_path = target_folder / VENV / "Scripts" / "pip.exe"
    else:
        pip_path = target_folder / VENV / "bin" / "pip"

    # Install requirements
    Logging.log("Installing requirements. This may take several minutes ...")

    if not pip_path.is_file():
        raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}")

    if not requirements_path.is_file():
        raise FileNotFoundError("requirements.txt file not found.")

    try:
        subprocess.check_call([str(pip_path), 'install', '-r', str(requirements_path), '-qqq'])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed on pip install command. {e}")

    Logging.log("Installation successful!", fg='green')


def activate_venv(folder=None):
    """
    Function to activate virtual environment.
    """
    target_folder = get_destination_path(folder)
    try:
        if platform.system() == "Windows":
            # On windows the venv folder structure is different from unix
            activate_path = target_folder / VENV / "Scripts" / "activate.bat"
            command = [str(activate_path)]

        else:
            activate_path = target_folder / VENV / "bin" / "activate"
            command = ['bash', str(activate_path)]

        subprocess.check_call(command)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to activate venv. {e}")

    Logging.log("Virtual environment activated!", fg='green')


def change_shell_folder_and_activate_venv(location):
    target_folder = get_destination_path(location)

    if platform.system() == "Windows":
        # On windows the venv folder structure is different from unix
        # activate_path = target_folder / VENV / "Scripts" / "activate.bat"
        pass
    else:
        activate_path = target_folder / VENV / "bin" / "activate"
        os.chdir(location)

        shell = os.environ.get('SHELL', '/bin/sh')
        os.execl(shell, shell, "--rcfile", activate_path)


def copy_project_template(template_source: Path, template_destiny: Path):
    """Copies the templates to destination folder."""

    template_path = template_source / "template"
    template_path.mkdir(exist_ok=True)
    
    shutil.copytree(
        src=template_path,
        dst=template_destiny,
        dirs_exist_ok=True
    )


def init_new_git_repo(folder: Path) -> git.Repo:
    """Init new git repository on folder."""
    return git.Repo.init(folder)


def initial_git_commit(repository: git.Repo):
    """Does the first git commit."""
    repository.git.add(A=True)
    repository.index.commit("Initial commit")


def append_requirement(library_name):
    """Appends a given requirement to the requirements.txt file."""

    current_path = get_destination_path()
    requirements_path = current_path / REQUIREMENTS
    with open(requirements_path, "r", encoding='UTF-8') as file:
        requirements = file.read()

    if library_name not in requirements:
        with open(requirements_path, "a", encoding='UTF-8') as file:
            file.write(f"\n{library_name}")


def rollback_append_requirement(library_name):
    current_path = get_destination_path()
    requirements_path = current_path / REQUIREMENTS

    with open(requirements_path, "r", encoding='UTF-8') as file:
        requirements = file.read()

    requirements_list = requirements.split('\n')
    last_requirement_added = requirements_list[-1]

    if library_name == last_requirement_added:
        with open(requirements_path, "w", encoding='UTF-8') as file:
            file.write('\n'.join(requirements_list[:-1]))


def remove_folder(folder: Path):
    """
    Removes a folder (location relative to cwd or absolute).
    """
    shutil.rmtree(folder, ignore_errors=True)


def create_folder(folder: Path):
    """
    Create a folder in the given path (location relative to cwd or absolute).
    """
    folder.mkdir(exist_ok=True)


def populate_rc_file(folder):
    """
    Updates the needed options inside the .labskitrc file.
    """
    # TODO: Create .labskitrc and populate it accordingly
