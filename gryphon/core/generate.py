"""
Module containing the code for the generate command in then CLI.
"""

import glob
import logging
import os
import shutil
from pathlib import Path

from .common_operations import (
    fetch_template,
    mark_notebooks_as_readonly, enable_files_overwrite,
    clean_readonly_folder, append_requirement
)
from .operations import EnvironmentManagerOperations, PathUtils, RCManager
from .registry import Template
from ..constants import GENERATE, VENV, CONDA, REMOTE_INDEX, LOCAL_TEMPLATE, REQUIREMENTS

logger = logging.getLogger('gryphon')


def generate(template: Template, folder=Path.cwd(), **kwargs):
    """
    Generate command from the OW Gryphon CLI.
    """
    current_path = PathUtils.get_destination_path(folder)
    rc_file = RCManager.get_rc_file(folder)
    env_path = RCManager.get_environment_manager_path(logfile=rc_file)
    env_type = RCManager.get_environment_manager(logfile=rc_file)

    logger.info("Generating template.")
    if template.registry_type == REMOTE_INDEX:

        template_folder = fetch_template(template, folder)

        try:
            enable_files_overwrite(
                source_folder=template_folder / "notebooks",
                destination_folder=folder / "notebooks"
            )
            parse_project_template(template_folder, kwargs)
            mark_notebooks_as_readonly(folder / "notebooks")
            RCManager.log_new_files(template, template_folder,
                                    performed_action=GENERATE, logfile=rc_file)

        finally:
            clean_readonly_folder(template_folder)

    elif template.registry_type == LOCAL_TEMPLATE:
        parse_project_template(template.path, kwargs)
        RCManager.log_new_files(template, Path(template.path) / "template", performed_action=GENERATE, logfile=rc_file)
    else:
        raise RuntimeError(f"Invalid registry type: {template.registry_type}.")

    for r in template.dependencies:
        append_requirement(r, location=folder)

    RCManager.log_add_library(template.dependencies)
    if env_type == VENV:
        EnvironmentManagerOperations.install_libraries_venv(
            environment_path=env_path,
            requirements_path=current_path / REQUIREMENTS
        )
    elif env_type == CONDA:
        EnvironmentManagerOperations.install_libraries_conda(
            environment_path=env_path,
            requirements_path=current_path / REQUIREMENTS
        )

    # RC file
    RCManager.log_operation(template, performed_action=GENERATE, logfile=rc_file)
    # RCManager.log_new_files(template, performed_action=GENERATE, logfile=rc_file)


def pattern_replacement(input_file, mapper):
    """
    Function that takes an input file name and replaces the handlebars according
    to the values present in the mapper dictionary.
    """
    output_file = str(input_file).replace(".handlebars", "")
    for before, after in mapper.items():
        output_file = output_file.replace(before.lower(), after)

    try:
        with open(input_file, "rt", encoding='UTF-8') as f_in:
            text = f_in.read()

        # read replace each of the arguments in the string
        for before, after in mapper.items():
            text = text.replace("{{" + before + "}}", after)

        os.makedirs(Path(output_file).parent, exist_ok=True)

        with open(output_file, "w", encoding='UTF-8') as f_out:
            # and write to output file
            f_out.write(text)

        if input_file != output_file:
            os.remove(input_file)

    except UnicodeDecodeError:
        logger.warning("There are binary files inside template folder.")


def parse_project_template(template_path: Path, mapper, destination_folder=None):
    """
    Routine that copies the template to the selected folder
    and replaces patterns.
    """

    temp_path = PathUtils.get_destination_path(f"temp_template")
    definitive_path = PathUtils.get_destination_path(destination_folder)

    # Copy files to a temporary folder
    logger.info(f"Creating files at {definitive_path}")

    # Move files to destination
    origin = Path(template_path)
    shutil.copytree(
        src=origin,
        dst=Path(temp_path),
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(
            origin / ".git/**",
            origin / ".github/**",
            origin / "__pycache__/**",
            origin / "envs/**",
            origin / ".venv/**",
            origin / ".ipynb_checkpoints/**"
        )
    )
    try:
        # Replace patterns and rename files
        glob_pattern = temp_path / "**"
        files = glob.glob(str(glob_pattern), recursive=True)

        for file in files:
            is_folder = Path(file).is_dir()
            if is_folder:
                continue
            pattern_replacement(file, mapper)

        # Copy the processed files to the repository
        os.makedirs(definitive_path, exist_ok=True)
        shutil.copytree(
            src=temp_path,
            dst=definitive_path,
            dirs_exist_ok=True
        )

    finally:
        shutil.rmtree(temp_path)

# TODO: Check if we are copying the .git files to the temporary folder on generate
#  folder we had some problems when deleting this files on windows.
