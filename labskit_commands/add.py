"""
Module containing the code for the add command in then CLI.
"""
import os
import click
from .command_operations import install_libraries, append_requirement

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
