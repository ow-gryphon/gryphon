"""
Module containing the code for the add command in then CLI.
"""
import logging
import os
import platform
from pathlib import Path

from .common_operations import (
    append_requirement, backup_requirements,
    rollback_requirement
)
from .operations import RCManager, BashUtils
from ..constants import SUCCESS

logger = logging.getLogger('gryphon')

# TODO: Check if the provided library is a valid one.
# TODO: Have some library list suggestion for each usage category the user has.


def add(library_name, version=None, cwd=Path.cwd()):
    """
    Add command from the OW Gryphon CLI.
    """
    logger.info("Adding required lib.")

    rc_file = RCManager.get_rc_file(cwd)
    env_path = "pip"

    try:
        in_gryphon_project = True
        env_path = RCManager.get_environment_manager_path(logfile=rc_file)

    except KeyError:
        in_gryphon_project = False
        logger.warning("It seems that we are not inside a Gryphon project folder. Installing libraries globally.")

    requirements_backup = backup_requirements(cwd)

    lib = library_name
    if version is not None:
        lib = f"{library_name}=={version}"

    try:
        if in_gryphon_project:
            append_requirement(lib, location=cwd)

        if platform.system() == "Windows":
            BashUtils.execute_and_log(f'\"{env_path / "Scripts" / "pip"}\" install {lib}')
        else:
            BashUtils.execute_and_log(f'\"{env_path / "bin" / "pip"}\" install {lib}')

        logger.log(SUCCESS, "Installation successful!")

    except RuntimeError as e:
        if in_gryphon_project:
            rollback_requirement(requirements_backup, location=cwd)
            logger.warning("Rolled back the changes from last command.")
        raise e
    else:
        if in_gryphon_project:
            RCManager.log_add_library([library_name])
    finally:
        os.remove(requirements_backup)
