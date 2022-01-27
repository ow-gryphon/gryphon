"""
Module containing the code for the generate command in then CLI.
"""

import os
import shutil
from pathlib import Path
import glob
import logging
from .common_operations import (
    get_destination_path,
    copy_project_template,
    append_requirement,
    install_libraries
)
from ..constants import SUCCESS

logger = logging.getLogger('gryphon')

# TODO: Think about how to give some help and examples about the commands


PACKAGE_PATH = Path(os.path.dirname(os.path.realpath(__file__)))


def generate(template_path: Path, requirements: list, **kwargs):
    """
    Generate command from the OW Gryphon CLI.
    """
    logger.info("Generating template.")
    parse_project_template(template_path, kwargs)

    for r in requirements:
        append_requirement(r)

    install_libraries()

    logger.log(SUCCESS, "Installation successful!")


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

    copy_project_template(
        template_destiny=temp_path,
        template_source=template_path
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
