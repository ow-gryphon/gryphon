import questionary
from labskit_commands.logging import Logging

add = [
    dict(
        type='input',
        name='library_name',
        message='Type the python library you want to install:'
    )
]


def main_questions(options):
    return [
        dict(
            type='list',
            name='command',
            message='Choose witch action to perform',
            choices=options
        )
    ]


def ask_which_template(metadata, command="init"):

    if command == "generate":
        questions = generate_1(metadata)
        responses = questionary.prompt(questions)
        return responses['template']

    elif command == "init":

        questions = init_1(options=metadata.keys())
        responses = questionary.prompt(questions)
        return responses['template'], responses['location']


def ask_extra_arguments(arguments, command="init"):

    if command == "generate":
        extra_questions = generate_2(arguments)
        return questionary.prompt(extra_questions)

    elif command == "init":
        extra_questions = init_2(arguments)
        return questionary.prompt(extra_questions)


def confirmation(message=None):
    message = "Confirm to proceed with the actions from above?" if message is None else message
    go_ahead = questionary.confirm(message=message).ask()

    if not go_ahead:
        Logging.log("Operation cancelled.")
        exit(1)


def confirm_generate(template_name, **kwargs):
    confirmation(f"Confirm that you want to render the \"{template_name}\" template inside the current project."
                 f"\nUsing the following arguments: {kwargs}")


def confirm_add(library_name):
    confirmation(f"Confirm that you want to install the \"{library_name}\" library to the current project.")


def confirm_init(template_name, location, **kwargs):
    message = f"\n\nConfirm that you want to start a new \"{template_name}\" project" \
              f"\nInside the folder \"{location}\""

    confirmation(
        message + f"\nUsing the following arguments: {kwargs}"
        if kwargs else
        message
    )


def generate_1(metadata):
    return [
        dict(
            type='list',
            name='template',
            message='Choose the desired template:',
            choices=metadata.keys()
        )
    ]


def generate_2(arguments):
    return [
        dict(
            type='input',
            name=field['name'],
            message=field['help']
        )
        for field in arguments
    ]


def init_1(options):
    return [
        dict(
            type='list',
            name='template',
            message='Choose the desired template:',
            choices=options
        ),
        dict(
            type='input',
            name='location',
            message='Path to render the template (absolute or relative to the current folder):',
        )
    ]


def init_2(arguments):
    return [
        dict(
            type='input',
            name=field['name'],
            message=field['help']
        )
        for field in arguments
    ]
