"""
Module containing the code for the add command in then CLI.
"""
import os
import click
from .command_operations import (
    install_libraries,
    copy_project_template,
    create_venv,
    update_templates
)

PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
CURRENT_PATH = os.getcwd()


def init(template, location, **kwargs):
    """
    Init command from the labskit CLI.
    """
    click.secho("Creating project scaffolding.", fg='green')
    kwargs.copy()
    try:
        update_templates()

        click.echo(f"initializing project at {location}")
        copy_project_template(
            template=template,
            command="init",
            location=location
        )
        populate_rc_file()
        init_new_git_repo()
        create_venv(location=location)
        install_libraries(location=location)
        initial_git_commit()
    except Exception as exception:
        raise exception


def populate_rc_file():
    """
    Updates the needed options inside the .labskitrc file.
    """
    # TODO: Create .labskitrc and populate it accordingly


def init_new_git_repo():
    """Init new git repository on folder."""
    # TODO: Init new git repository with a proper name.
    os.system("git init")


def initial_git_commit():
    """Does the first git commit."""
    os.system("git add .")
    os.system("git commit -m 'Initial commit'")
