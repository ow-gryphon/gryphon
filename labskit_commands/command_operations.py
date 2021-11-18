"""
File containing operations that are common to the commands.
"""

import os
import platform
import shutil
import subprocess
import click


PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))


def get_destination_path(folder=None):
    """
    Function that helps to define the full path to a directory.

    It checks if the path is an absolute or relative path, then
    if relative, it appends the current folder to it, transforming
    it into a absolute path.
    """
    if folder is None:
        return os.getcwd()

    is_absolute_path = os.path.isabs(folder)

    if not is_absolute_path:
        folder = os.path.abspath(folder)

    return folder


def update_templates():
    """
    Function that updates all the templates from their git repository.
    """
    # TODO: choose witch template registry to use (git or pypi or local artifactory)
    # TODO: update the chosen template to match the registry


def create_venv(folder=None):
    """
    Function to a virtual environment inside a folder.
    """
    target_folder = get_destination_path(folder)
    venv_path = os.path.join(target_folder, ".venv")

    # Create venv
    click.echo("Creating virtual environment.")
    os.system(f"python -m venv {venv_path}")


def install_libraries(folder=None):
    """
    Function to install the libraries from a 'requirements.txt' file
    """
    target_folder = get_destination_path(folder)
    
    if platform.system() == "Windows":
        pip_path = os.path.join(target_folder, ".venv", "Scripts", "pip")
    else:
        pip_path = os.path.join(target_folder, ".venv", "bin", "pip")


    requirements_path = os.path.join(target_folder, "requirements.txt")

    # Install requirements
    click.echo("Installing requirements. This may take some minutes ...")
    try:
        output = subprocess.check_output(
            f"{pip_path} --disable-pip-version-check "
            f"install -r {requirements_path}", shell=True)
    except subprocess.CalledProcessError:
        click.secho("Failed to install requirements", fg='red')
        raise FileNotFoundError("Failed on pip install command.")

    click.secho("Installation succeeded.", fg='green')


def copy_project_template(command: str, template: str, folder: str):
    """
    Copies the templates to destination folder.
    """
    template_path = os.path.join(PACKAGE_PATH, "data", command, template, "template")
    target_path = get_destination_path(folder)

    os.makedirs(target_path, exist_ok=True)
    shutil.copytree(
        src=template_path,
        dst=target_path,
        dirs_exist_ok=True
    )
