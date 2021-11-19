"""
Module containing the code for the add command in then CLI.
"""
import os
import click
from .command_operations import get_destination_path, install_libraries

# TODO: Check if the given folder really is a labskit project (like by reading the .rc file)
# TODO: Think about freeze feature (at time of handover)
# TODO: Check if the provided library is a valid one.


def add(library_name):
    """
    Add command from the labskit CLI.
    """
    click.echo("Adding required lib.")
    append_requirement(library_name)
    install_libraries()


def append_requirement(library_name):
    """
    Appends a given requirement to the requirements.txt file.
    """
    current_path = get_destination_path()
    requirements_path = os.path.join(current_path, "requirements.txt")
    with open(requirements_path, "a", encoding='UTF-8') as file:
        file.write(f"\n{library_name}")
