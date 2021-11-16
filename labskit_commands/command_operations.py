"""
File containing operations that are common to the commands.
"""

import os
import subprocess
import click


PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
CURRENT_PATH = os.getcwd()


def get_destination_path(location=""):
    """
    Function that helps to define the full path to a directory.

    It checks if the path is an absolute or relative path, then
    if relative, it appends the current folder to it, transforming
    it into a absolute path.
    """
    if len(location) == 0:
        return CURRENT_PATH

    is_absolute_path = location[0] == "/"

    if not is_absolute_path:
        location = os.path.join(CURRENT_PATH, location)

    return location


def update_templates():
    """
    Function that updates all the templates from their git repository.
    """
    # TODO: choose witch template registry to use (git or pypi or local artifactory)
    # TODO: update the chosen template to match the registry


def create_venv(location):
    """
    Function to a virtual environment inside a folder.
    """
    location = get_destination_path(location)

    # Create venv
    click.echo("Creating virtual environment.")
    os.system(f"python -m venv {location}/.venv")


def install_libraries(location=""):
    """
    Function to install the libraries from a 'requirements.txt' file
    """
    location = get_destination_path(location)

    # Install requirements
    click.echo("Installing requirements. This may take some minutes ...")
    try:
        output = subprocess.check_output(
            f"{location}/.venv/bin/pip --disable-pip-version-check "
            f"install -r {location}/requirements.txt", shell=True)
    except subprocess.CalledProcessError:
        click.secho("Failed to install requirements", fg='red')
        raise FileNotFoundError("Failed on pip install command.")

    click.secho("Installation succeeded.", fg='green')


def copy_project_template(command, template, location):
    """
    Copies the templates to destination folder.
    """
    template_path = os.path.join(PACKAGE_PATH, f"data/{command}/{template}/template")
    location = get_destination_path(location)

    os.system(f"mkdir -p {location}")
    os.system(f"cp -r {template_path}/* {location}")

    # TODO: Change this from bash commands (os.system) to a more pythonic way
    # so we can then catch errors and give proper feedback to the user.
