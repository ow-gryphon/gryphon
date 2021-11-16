"""
Module containing the code for the add command in then CLI.
"""
import os
import click
from .command_operations import (
    install_libraries,
    get_destination_path,
    create_venv,
    update_templates
)

PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
CURRENT_PATH = os.getcwd()


def init(template, location):
    """
    Init command from the labskit CLI.
    """
    click.secho("Creating project scafolding.", fg='green')
    try:
        update_templates()
        copy_project_template(template, location)
        populate_rc_file()
        init_new_git_repo()
        create_venv(location)
        install_libraries()
        initial_git_commit()
    except Exception as exception:
        raise exception


def copy_project_template(template, location):
    """
    Copies the templates to destination folder.
    """
    template_path = os.path.join(PACKAGE_PATH, f"data/init/{template}/template")
    location = get_destination_path(location)

    # click.echo(template_path)
    click.echo(f"initializing project at {location}")

    os.system(f"mkdir -p {location}")
    os.system(f"cp -r {template_path}/* {location}")

    #TODO: Change this from bash commands (os.system) to a more pythonic way
    # so we can then catch errors and give propper feedback to the user.


def populate_rc_file():
    """
    Updates the needed options inside the .labskitrc file.
    """
    #TODO: Create .labskitrc and populate it accordingly


def init_new_git_repo():
    """Init new git repository on folder."""
    #TODO: Init new git repository with a propper name.
    # os.system("git init")
    initial_git_commit()


def initial_git_commit():
    """Does the first git commit."""
    #TODO: Initial commit
    # os.system("git add .")
    # os.system("git commit -m 'Initial commit'")
