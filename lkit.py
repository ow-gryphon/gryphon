"""
LKit .
"""
import os
import PyInquirer as piq
import labskit_commands
from labskit_commands import utils


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PACKAGE_PATH, "labskit_commands", "data")


def add():
    """add templates based on arguments and configurations."""
    questions = [
        dict(
            type='input',
            name='library_name',
            message='Type the python library you want to install:'
        )
    ]
    response = piq.prompt(questions)
    labskit_commands.add(
        library_name=response['library_name']
    )


def generate():
    """generates templates based on arguments and configurations."""

    metadata = commands["generate"].get_metadata()
    base_questions = [
        dict(
            type='list',
            name='template',
            message='Choose the desired template:.',
            choices=metadata.keys()
        )
    ]
    responses = piq.prompt(base_questions)
    template = responses['template']

    metadata = metadata[template]["metadata"]
    extra_questions = [
        dict(
            type='input',
            name=field['name'],
            message=field['help']
        )
        for field in metadata.get("arguments", [])
    ]

    extra_parameters = piq.prompt(extra_questions)

    labskit_commands.generate(
        template=template,
        extra_parameters=extra_parameters
    )


def init():
    """Creates a starter repository for analytics projects."""
    metadata = commands["init"].get_metadata()
    base_questions = [
        dict(
            type='list',
            name='template',
            message='Choose the desired template:.',
            choices=metadata.keys()
        ),
        dict(
            type='input',
            name='location',
            message='Path to render the template (absolute or relative to the current folder):',
        )
    ]
    responses = piq.prompt(base_questions)
    template = responses['template']
    location = responses['location']

    metadata = metadata[template]["metadata"]

    extra_questions = [
        dict(
            type='input',
            name=field['name'],
            message=field['help']
        )
        for field in metadata.get("arguments", [])
    ]

    extra_parameters = piq.prompt(extra_questions)

    labskit_commands.init(
        template=template,
        location=location,
        **extra_parameters
    )


functions = {
    "init": init,
    "generate": generate,
    "add": add
}

commands = {}

# Extends each of the command docstrings
for name, function in functions.items():
    commands[name] = utils.CommandLoader(
        command_name=name,
        templates_path=DATA_PATH
    )


def main():
    questions = [
        dict(
            type='list',
            name='command',
            message='Choose what you want to do.',
            choices=commands.keys()
        )
    ]
    response = piq.prompt(questions)

    command = functions[response['command']]
    command()


if __name__ == '__main__':
    main()
