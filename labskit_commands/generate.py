"""
Module containing the code for the generate command in then CLI.
"""
import os
import shutil
import glob
import click
from .command_operations import (
    get_destination_path,
    update_templates,
    copy_project_template
)

# TODO: Think about how to give some help and examples about the commands


PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))


def generate(template: str, extra_parameters: dict):
    """
    Generate command from the labskit CLI.
    """
    click.echo("Generating template.")
    try:
        update_templates()
        parse_project_template(template, extra_parameters)
        # install_libraries()
    except Exception as exception:
        raise exception


def pattern_replacement(input_file, mapper):
    """
    Function that takes an input file name and replaces the handlebars according
    to the values present in the mapper dictionary.
    """
    output_file = input_file.replace(".handlebars", "")
    for before, after in mapper.items():
        output_file = output_file.replace(before.lower(), after)

    f_in = open(input_file, "rt", encoding='UTF-8')
    f_out = open(output_file, "wt", encoding='UTF-8')
    try:
        for line in f_in:
            replaced = line

            # read replace each of the arguments in the string
            for before, after in mapper.items():
                replaced = replaced.replace("{{" + before + "}}", after)

            # and write to output file
            f_out.write(replaced)
        f_in.close()
        f_out.close()
    except UnicodeDecodeError:
        click.secho("WARNING: There are binary files inside template folder.", fg='yellow')

    except Exception as exception:
        f_in.close()
        f_out.close()

        raise exception


def parse_project_template(template, mapper):
    """
    Function that copies the template to the selected folder
    and
    """

    temp_path = get_destination_path(f"temp_{template}")
    definitive_path = get_destination_path()

    # Copy files to a temporary folder
    click.echo(f"Creating files at {definitive_path}")

    copy_project_template(
        template=template,
        command="generate",
        folder=temp_path
    )

    # Replace patterns and rename files
    glob_pattern = os.path.join(temp_path, "**")
    files = glob.glob(glob_pattern, recursive=True)

    for file in files:
        is_folder = os.path.isdir(file)
        if is_folder:
            continue
        pattern_replacement(file, mapper)
        os.remove(file)

    # Copy the processed files to the repository
    os.makedirs(definitive_path, exist_ok=True)
    shutil.copytree(
        src=temp_path,
        dst=definitive_path,
        dirs_exist_ok=True
    )
    shutil.rmtree(temp_path)


def populate_rc_file():
    """
    Updates the needed options inside the .labskitrc file.
    """
    # TODO: Create .labskitrc and populate it accordingly
