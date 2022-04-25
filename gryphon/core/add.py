"""
Module containing the code for the add command in then CLI.
"""
import json
import logging
import os

from .common_operations import (
    install_libraries_venv, append_requirement, backup_requirements,
    rollback_requirement, install_libraries_conda, log_add_library
)
from .settings import SettingsManager
from ..constants import VENV, CONDA

logger = logging.getLogger('gryphon')

# TODO: Think about freeze feature (at time of handover)
# TODO: Check if the provided library is a valid one.
# TODO: Have some library list suggestion for each usage category the user has.


def add(library_name):
    """
    Add command from the OW Gryphon CLI.
    """
    logger.info("Adding required lib.")
    requirements_backup = backup_requirements()
    append_requirement(library_name)
    try:
        with open(SettingsManager.get_config_path(), "r", encoding="UTF-8") as f:
            env_manager = json.load(f)["environment_management"]

        if env_manager == VENV:
            install_libraries_venv()
        elif env_manager == CONDA:
            install_libraries_conda()
        else:
            env_list = [VENV, CONDA]
            raise RuntimeError(f"Invalid environment manager on the config file: \"{env_manager}\"."
                               f"Should be one of {env_list}. Restoring the default config file should solve.")
    except RuntimeError as e:
        rollback_requirement(requirements_backup)
        logger.warning("Rolled back the changes from last command.")
        raise e
    else:
        log_add_library(library_name)
    finally:
        os.remove(requirements_backup)
