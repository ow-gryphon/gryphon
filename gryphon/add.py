"""
Module containing the code for the add command in then CLI.
"""
from .logging import Logging
from .command_operations import (
    install_libraries, append_requirement,
    rollback_append_requirement
)
# TODO: Check if the given folder really is a labskit project (like by reading the .rc file)
# TODO: Think about freeze feature (at time of handover)
# TODO: Check if the provided library is a valid one.
# TODO: Have some library list suggestion for each usage category the user has.


def add(library_name):
    """
    Add command from the OW Gryphon CLI.
    """
    Logging.log("Adding required lib.", fg="green")
    append_requirement(library_name)
    try:
        install_libraries()
    except RuntimeError as e:
        rollback_append_requirement(library_name)
        Logging.warn("Rolled back the changes from last command.")
        raise e
