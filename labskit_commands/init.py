"""
Module containing the code for the add command in then CLI.
"""
import os
import click
from .command_operations import (
    install_libraries,
    copy_project_template,
    create_venv,
    init_new_git_repo,
    initial_git_commit
)

PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))


def init(template_path, location, **kwargs):
    """
    Init command from the labskit CLI.
    """
    click.secho("Creating project scaffolding.", fg='green')
    kwargs.copy()

    click.echo(f"initializing project at {location}")
    copy_project_template(
        template_destiny=location,
        template_source=template_path
    )
    populate_rc_file(folder=location)
    create_venv(folder=location)
    install_libraries(folder=location)
    repo = init_new_git_repo(folder=location)
    initial_git_commit(repo)


def populate_rc_file(folder):
    """
    Updates the needed options inside the .labskitrc file.
    """
    # TODO: Create .labskitrc and populate it accordingly
