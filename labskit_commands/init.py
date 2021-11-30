"""
Module containing the code for the add command in then CLI.
"""
import os
import click
from .command_operations import (
    install_libraries,
    copy_project_template,
    create_venv,
    update_templates,
    init_new_git_repo,
    initial_git_commit
)

PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))


def init(template, location, **kwargs):
    """
    Init command from the labskit CLI.
    """
    click.secho("Creating project scaffolding.", fg='green')

    update_templates()
    click.echo(f"initializing project at {location}")
    copy_project_template(
        template=template,
        command="init",
        folder=location,
    )
    populate_rc_file(folder=location)
    create_venv(folder=location)
    install_libraries(folder=location)
    init_new_git_repo(folder=location)
    initial_git_commit(folder=location)


def populate_rc_file(folder):
    """
    Updates the needed options inside the .labskitrc file.
    """
    # TODO: Create .labskitrc and populate it accordingly

