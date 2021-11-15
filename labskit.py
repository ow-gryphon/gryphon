"""
Labskit CLI Main module.
"""
import os
import click
import app


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PACKAGE_PATH, "app/data")


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Base CLI interface."""


@cli.command()
@click.argument("library_name")
def add(library_name):
    """add templates based on arguments and configurations."""
    app.add(library_name)


@click.argument("template")
@click.argument('extra', nargs=-1)
def generate(template, extra):
    """generates templates based on arguments and configurations."""
    extra = app.utils.validate_parameters(extra, template, commmands["generate"].get_metadata())
    app.generate(template, extra)


@click.argument("template")
@click.argument("location", type=click.Path())
@click.argument('extra', nargs=-1)
def init(template, location, extra):
    """Creates a starter repository for analytics projects."""
    extra = app.utils.validate_parameters(extra, template, commmands["init"].get_metadata())
    app.init(
        template=template,
        location=location
    )


functions = {
    "init": init,
    "generate": generate,
    # "add": add
}

commmands = {}

# Extends each of the command docstrings
for name, function in functions.items():

    commmands[name] = app.utils.CommandLoader(name, package_path=DATA_PATH)
    metadata = commmands[name].get_metadata()

    # Add command specific help
    function.__doc__ += app.utils.get_command_help(metadata).replace('\n', '\n\n')

    # Generates the CLICK command (used to be a decorator)
    cli.command()(function)


if __name__ == '__main__':
    cli()
