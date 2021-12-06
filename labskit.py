"""
Labskit CLI Main module.
"""
from os import path
import json
import click
import labskit_commands
from labskit_commands import helpers
from labskit_commands.registry import RegistryCollection


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
PACKAGE_PATH = path.dirname(path.realpath(__file__))
DATA_PATH = path.join(PACKAGE_PATH, "labskit_commands", "data")


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
    generate_metadata = commands.get_metadata()["generate"]
    extra = helpers.validate_parameters(extra, template, generate_metadata)
    template_path = generate_metadata[template]["path"]

    labskit_commands.generate(
        template_path,
        metadata.get("dependencies", []),
        extra_parameters=extra
    )


@click.argument("template")
@click.argument("location", type=click.Path())
@click.argument('extra', nargs=-1)
def init(template, location, extra):
    """Creates a starter repository for analytics projects."""
    extra_parameters = helpers.validate_parameters(extra, template, commands.get_metadata()["init"])

    template_path = commands.get_metadata()["init"][template]["path"]
    labskit_commands.init(
        template_path=template_path,
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

    metadata = commands.get_metadata()[name]

    # Add command specific help
    function.__doc__ += helpers.get_command_help(metadata)

    # Generates the CLICK command (used to be a decorator)
    cli.command()(function)


if __name__ == '__main__':
    cli()
