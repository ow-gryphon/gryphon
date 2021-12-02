"""
LKit .
"""
import json
from os import path
import questionary
import labskit_commands
from labskit_commands import questions
from labskit_commands.registry import RegistryCollection

PACKAGE_PATH = path.dirname(path.realpath(__file__))
DATA_PATH = path.join(PACKAGE_PATH, "labskit_commands", "data")


def confirmation(message=None):
    message = "Confirm to proceed with the actions from above?" if message is None else message
    go_ahead = questionary.confirm(message=message).ask()

    if not go_ahead:
        print("Exiting.")
        exit(1)


def add():
    """add templates based on arguments and configurations."""

    response = questionary.prompt(questions.add)['library_name']

    confirmation(f"Confirm that you want to install the \"{response}\" library to the current project.")

    labskit_commands.add(
        library_name=response
    )


def generate():
    """generates templates based on arguments and configurations."""

    metadata = commands.get_metadata()["generate"]

    questions_1 = questions.generate_1(metadata)
    responses = questionary.prompt(questions_1)

    template = responses['template']
    template_metadata = metadata[template]["metadata"]
    template_path = metadata[template]["path"]

    extra_questions = questions.generate_2(template_metadata)
    extra_parameters = questionary.prompt(extra_questions)

    confirmation(f"Confirm that you want to render the \"{template}\" template inside the current project."
                 f"\nUsing the following arguments: {extra_parameters}")

    labskit_commands.generate(
        template_path=template_path,
        extra_parameters=extra_parameters,
        requirements=template_metadata.get("dependencies")
    )


def init():
    """Creates a starter repository for analytics projects."""
    metadata = commands.get_metadata()["init"]

    base_questions = questions.init_1(metadata.keys())
    responses = questionary.prompt(base_questions)

    template = responses['template']
    location = responses['location']

    template_metadata = metadata[template]["metadata"]
    template_path = metadata[template]["path"]
    arguments = template_metadata.get("arguments", [])

    extra_questions = questions.init_2(arguments)
    extra_parameters = questionary.prompt(extra_questions)

    message = f"\n\nConfirm that you want to start a new \"{template}\" project" \
              f"\nInside the folder \"{location}\""

    confirmation(
        message + f"\nUsing the following arguments: {extra_parameters}"
        if extra_parameters else
        message
    )

    labskit_commands.init(
        template_path=template_path,
        location=location,
        **extra_parameters
    )


config_file = path.join(PACKAGE_PATH, "labskit_commands/data/labskit_config.json")

with open(config_file, "r") as f:
    settings = json.load(f)
    commands = RegistryCollection.from_config_file(settings, DATA_PATH)


def main():

    command_question = questions.main_questions(commands.get_metadata().keys())

    try:
        response = questionary.prompt(command_question)['command']
        functions = {
            "init": init,
            "generate": generate,
            "add": add
        }
        command = functions[response]
        command()
    except KeyError:
        pass


if __name__ == '__main__':
    main()
