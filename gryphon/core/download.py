"""
Module containing the code for the init command in the CLI.
"""
import json
import logging
import os
import shutil
from pathlib import Path

from .common_operations import (
    download_template, clean_readonly_folder
)
from .operations import (
    BashUtils, RCManager, SettingsManager
)
from .registry import Template
from ..constants import (
    DOWNLOAD, REMOTE_INDEX, SUCCESS, LOCAL_TEMPLATE
)

logger = logging.getLogger('gryphon')


def handle_template(template, project_home, rc_file):
    if template.registry_type == REMOTE_INDEX:

        template_folder = download_template(template, project_home)
        
        try:

            # Move files to destination
            shutil.copytree(
                src=Path(template_folder),
                dst=project_home,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(
                    ".git",
                    ".github",
                    "__pycache__",
                    ".gitignore"
                    "envs",
                    ".venv",
                    ".ipynb_checkpoints"
                )
            )
        finally:
            RCManager.log_new_files(template, template_folder, performed_action=DOWNLOAD, logfile=rc_file)
            clean_readonly_folder(template_folder)

    elif template.registry_type == LOCAL_TEMPLATE:

        BashUtils.copy_project_template(
            template_destiny=project_home,
            template_source=Path(template.path)  # / "template"
        )

        RCManager.log_new_files(template, Path(template.path), performed_action=DOWNLOAD, logfile=rc_file)

    else:
        raise RuntimeError(f"Invalid registry type: {template.registry_type}.")


def download(template: Template, location, **kwargs):
    """
    Download command from the OW Gryphon CLI.
    """
    kwargs.copy()

    project_home = Path.cwd() / location

    logger.info(f"Initializing project at {project_home}")

    os.makedirs(project_home, exist_ok=True)

    # RC file
    rc_file = RCManager.get_rc_file(project_home)
    RCManager.log_operation(template, performed_action=DOWNLOAD, logfile=rc_file)

    # TEMPLATE
    handle_template(template, project_home, rc_file)

    logger.log(SUCCESS, "Project created successfully.")
