"""
Module containing the code for the add command in then CLI.
"""
import logging
import os
from pathlib import Path

from .common_operations import (
    append_requirement, backup_requirements,
    rollback_requirement
)
from .operations import EnvironmentManagerOperations, RCManager
from ..constants import VENV, CONDA, REQUIREMENTS

logger = logging.getLogger('gryphon')

# TODO: Check if the provided library is a valid one.
# TODO: Have some library list suggestion for each usage category the user has.


def add(library_name, version=None, cwd=Path.cwd()):
    """
    Add command from the OW Gryphon CLI.
    """
    logger.info("Adding required lib.")

    rc_file = RCManager.get_rc_file(cwd)
    env_path = RCManager.get_environment_manager_path(logfile=rc_file)
    env_manager = RCManager.get_environment_manager(logfile=rc_file)

    requirements_backup = backup_requirements(cwd)
    lib = library_name
    if version is not None:
        lib = f"{library_name}=={version}"

    try:
        append_requirement(lib, location=cwd)

        if env_manager == VENV:
            EnvironmentManagerOperations.install_libraries_venv(
                environment_path=env_path,
                requirements_path=cwd / REQUIREMENTS
            )

        elif env_manager == CONDA:
            EnvironmentManagerOperations.install_libraries_conda(
                environment_path=env_path,
                requirements_path=cwd / REQUIREMENTS
            )

        else:
            env_list = [VENV, CONDA]
            raise RuntimeError(f"Invalid environment manager on the config file: \"{env_manager}\"."
                               f"Should be one of {env_list}. Restoring the default config file should solve.")

    except RuntimeError as e:
        rollback_requirement(requirements_backup, location=cwd)
        logger.warning("Rolled back the changes from last command.")
        raise e
    else:
        RCManager.log_add_library([library_name])
    finally:
        os.remove(requirements_backup)
