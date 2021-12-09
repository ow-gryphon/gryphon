"""
Labskit CLI Main module.
"""
from os import path
from pathlib import Path
import json
import click
import labskit_commands
from labskit_commands import helpers
from labskit_commands.registry import RegistryCollection


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
PACKAGE_PATH = Path(__file__).parent
DATA_PATH = PACKAGE_PATH / "labskit_commands" / "data"


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Base CLI interface."""


@cli.command()
@click.argument("library_name")
def add(library_name):
    """add templates based on arguments and configurations."""
    labskit_commands.add(library_name)


@click.argument("template")
@click.argument('extra', nargs=-1)
def generate(template, extra):
    """generates templates based on arguments and configurations."""
    existing_templates = commands.get_templates(command="generate")
    extra_parameters = helpers.validate_parameters(extra, template, existing_templates)
    template = existing_templates[template]

    labskit_commands.generate(
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
    labskit_commands.init(
        template_path=template.path,
        location=location,
        **extra_parameters
    )


functions = {
    "init": init,
    "generate": generate,
    # "add": add
}

config_file = path.join(PACKAGE_PATH, "labskit_commands", "data", "labskit_config.json")

with open(config_file, "r") as f:
    settings = json.load(f)
    commands = RegistryCollection.from_config_file(settings, DATA_PATH)

# Extends each of the command docstrings
for name, function in functions.items():

    templates = commands.get_templates()[name]

    # Add command specific help
    function.__doc__ += helpers.get_command_help(templates)

    # Generates the CLICK command (used to be a decorator)
    cli.command()(function)


if __name__ == '__main__':
    cli()
