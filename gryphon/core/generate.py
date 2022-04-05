"""
Module containing the code for the generate command in then CLI.
"""

import os
import json
import shutil
from pathlib import Path
import glob
import logging
from .registry import Template
from .settings import SettingsManager
from .common_operations import (
    get_destination_path,
    append_requirement,
    install_libraries_venv, install_libraries_conda,
    get_rc_file,
    log_operation, log_new_files, log_add_library,
    download_template, unzip_templates, unify_templates
)
from ..constants import GENERATE, DEFAULT_ENV, VENV, CONDA, REMOTE_INDEX, LOCAL_TEMPLATE


logger = logging.getLogger('gryphon')


def generate(template: Template, requirements: list, folder=Path.cwd(), **kwargs):
    """
    Generate command from the OW Gryphon CLI.
    """
    with open(SettingsManager.get_config_path(), "r", encoding="UTF-8") as f:
        data = json.load(f)
        env_type = data.get("environment_management", DEFAULT_ENV)

    logger.info("Generating template.")
    if template.registry_type == REMOTE_INDEX:

        temporary_folder = download_template(template)
        zip_folder = unzip_templates(temporary_folder)
        template_folder = unify_templates(zip_folder)

        parse_project_template(template_folder, kwargs)

        shutil.rmtree(temporary_folder)
        shutil.rmtree(template_folder)

    elif template.registry_type == LOCAL_TEMPLATE:
        parse_project_template(template.path, kwargs)
    else:
        raise RuntimeError(f"Invalid registry type: {template.registry_type}.")

    for r in requirements:
        append_requirement(r)

    log_add_library(requirements)
    if env_type == VENV:
        install_libraries_venv()
    elif env_type == CONDA:
        install_libraries_conda()

    # RC file
    rc_file = get_rc_file(folder)
    log_operation(template, performed_action=GENERATE, logfile=rc_file)
    log_new_files(template, performed_action=GENERATE, logfile=rc_file)


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

    temp_path = get_destination_path(f"temp_template")
    definitive_path = get_destination_path(destination_folder)

    # Copy files to a temporary folder
    logger.info(f"Creating files at {definitive_path}")

    # Move files to destination
    shutil.copytree(
        src=Path(template_path),
        dst=Path(temp_path),
        dirs_exist_ok=True
    )

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
    shutil.rmtree(temp_path)
