"""
Module containing the code for the add command in then CLI.
"""
import os
import click
from .command_operations import get_destination_path, install_libraries

# TODO: Check if the given folder really is a labskit project (like by reading the .rc file)
# TODO: Think about freeze feature (at time of handover)

PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
CURRENT_PATH = os.getcwd()


def add(library_name):
    """
    Add command from the labskit CLI.
    """
    click.echo("Generating template.")
    try:
        append_requirement(library_name)
        install_libraries()
    except Exception as exception:
        raise exception


def append_requirement(library_name):
    """
    Appends a given requirement to the requirements.txt file.
    """
    location = get_destination_path("")
    with open(f"{location}/requirements.txt", "a", encoding='UTF-8') as file:
        file.write(f"\n{library_name}")
