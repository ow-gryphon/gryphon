"""
LKit .
"""
import json
from pathlib import Path
import questionary
import labskit_commands
from labskit_commands import questions
from labskit_commands.registry import RegistryCollection
from labskit_commands.logging import Logging

PACKAGE_PATH = Path(__file__).parent
DATA_PATH = PACKAGE_PATH / "labskit_commands" / "data"


def add():
    """add templates based on arguments and configurations."""

    library_name = questionary.prompt(questions.add)['library_name']

    questions.confirm_add(library_name)

    labskit_commands.add(
        library_name=library_name
    )


def generate():
    """generates templates based on arguments and configurations."""

    templates = commands.get_templates("generate")
    template_name = questions.ask_which_template(templates, command="generate")

    template = templates[template_name]

    extra_parameters = questions.ask_extra_arguments(
        template.arguments,
        command="generate"
    )

    questions.confirm_generate(
        template_name=template_name,
        **extra_parameters
    )
    print(extra_parameters)
    labskit_commands.generate(
        template_path=template.path,
        requirements=template.dependencies,
        **extra_parameters,
    )


def init():
    """Creates a starter repository for analytics projects."""
    templates = commands.get_templates("init")
    template_name, location = questions.ask_which_template(templates)

    template = templates[template_name]
    extra_parameters = questions.ask_extra_arguments(
        arguments=template.arguments,
        command="init"
    )

    questions.confirm_init(
        template_name=template.name,
        location=template.path,
        **extra_parameters
    )

    labskit_commands.init(
        template_path=template.path,
        location=location,
        **extra_parameters
    )


config_file = PACKAGE_PATH / "labskit_commands" / "data" / "labskit_config.json"

with open(config_file, "r") as f:
    settings = json.load(f)
    try:
        commands = RegistryCollection.from_config_file(settings, DATA_PATH)
    except Exception as e:
        Logging.error(f'Registry loading error. {e}')
        exit(1)


def main():

    possible_commands = ["init", "generate", "add"]
    command_question = questions.main_questions(possible_commands)

    try:
        response = questionary.prompt(command_question)['command']
        functions = {
            "init": init,
            "generate": generate,
            "add": add
        }

        command = functions[response]
        try:
            command()
        except Exception as er:
            Logging.error(f'Runtime error. {er}')
            exit(1)

    except KeyError:
        pass


if __name__ == '__main__':
    main()
