"""
File containing operations that are common to the commands.
"""

import os
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
    try:
        is_absolute_path = location[0] == "/"
    except IndexError:
        # This happens when the "location" is empty ("")
        return CURRENT_PATH

    if not is_absolute_path:
        location = os.path.join(CURRENT_PATH, location)

    return location


def update_templates():
    """
    Function that updates all the templates from their git repository.
    """
    #TODO: choose witch template registry to use (git or pypi or local artifactory)
    #TODO: update the choosen template to match the registry


def create_venv(location):
    """
    Function to a virtual environment inside a folder.
    """
    location = get_destination_path(location)

    # Create venv
    click.echo("Creating virtual environment.")
    os.system(f"python -m venv {location}/.venv")


def install_libraries(location):
    """
    Function to install the libraries from a 'requirements.txt' file
    """
    location = get_destination_path(location)

    # Install requirements
    click.echo("Installing requirements. This may take some minutes ...")
    os.system(f"{location}/.venv/bin/pip --disable-pip-version-check install -r "
              f"{location}/requirements.txt -q")
    click.secho("Installation succeeded.", fg='green')
