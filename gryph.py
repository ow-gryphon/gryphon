"""
OW Gryphon CLI Main module.
"""
from os import path
from pathlib import Path
import json
import click
import gryphon_commands
from gryphon_commands import helpers
from gryphon_commands.registry import RegistryCollection


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
PACKAGE_PATH = Path(__file__).parent
DATA_PATH = PACKAGE_PATH / "gryphon_commands" / "data"


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Base CLI interface."""


@cli.command()
def activate():
    """add templates based on arguments and configurations."""
    # TODO: gryphon activate
    # gryphon_commands.activate()


@cli.command()
@click.argument("library_name")
def add(library_name):
    """add templates based on arguments and configurations."""
    gryphon_commands.add(library_name)


@click.argument("template")
@click.argument('extra', nargs=-1)
def generate(template, extra):
    """generates templates based on arguments and configurations."""
    existing_templates = commands.get_templates(command="generate")
    extra_parameters = helpers.validate_parameters(extra, template, existing_templates)
    template = existing_templates[template]

    gryphon_commands.generate(
        template_path=template.path,
        requirements=template.dependencies,
        **extra_parameters
    )


@click.argument("template")
@click.argument("location", type=click.Path())
@click.argument('extra', nargs=-1)
def init(template, location, extra):
    """Creates a starter repository for analytics projects."""
    existing_templates = commands.get_templates(command="init")
    extra_parameters = helpers.validate_parameters(extra, template, existing_templates)

    template = existing_templates[template]
    gryphon_commands.init(
        template_path=template.path,
        location=location,
        **extra_parameters
    )


functions = {
    "init": init,
    "generate": generate,
    # "add": add
}

config_file = path.join(DATA_PATH / "gryphon_config.json")

with open(config_file, "r") as f:
    settings = json.load(f)
    commands = RegistryCollection.from_config_file(settings, DATA_PATH / "template_registry")

# Extends each of the command docstrings
for name, function in functions.items():

    templates = commands.get_templates()[name]

    # Add command specific help
    function.__doc__ += helpers.get_command_help(templates)

    # Generates the CLICK command (used to be a decorator)
    cli.command()(function)


if __name__ == '__main__':
    cli()

# DONE: Treat FIle not found error when searching for requirements.txt file
# DONE: Show Template description just before the confirmation
# TODO: Make categories on generate command
# TODO: Implement gitflow guidelines
