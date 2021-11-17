"""
Labskit CLI Main module.
"""
import os
import click
import labskit_commands


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PACKAGE_PATH, "labskit_commands", "data")


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
    extra = labskit_commands.utils.validate_parameters(extra, template, commands["generate"].get_metadata())
    labskit_commands.generate(template, extra)


@click.argument("template")
@click.argument("location", type=click.Path())
@click.argument('extra', nargs=-1)
def init(template, location, extra):
    """Creates a starter repository for analytics projects."""
    extra_parameters = labskit_commands.utils.validate_parameters(extra, template, commands["init"].get_metadata())
    labskit_commands.init(
        template=template,
        location=location,
        **extra_parameters
    )


functions = {
    "init": init,
    "generate": generate,
    # "add": add
}

commands = {}

# Extends each of the command docstrings
for name, function in functions.items():

    commands[name] = labskit_commands.utils.CommandLoader(name, package_path=DATA_PATH)
    metadata = commands[name].get_metadata()

    # Add command specific help
    function.__doc__ += labskit_commands.utils.get_command_help(metadata).replace('\n', '\n\n')

    # Generates the CLICK command (used to be a decorator)
    cli.command()(function)


if __name__ == '__main__':
    cli()
