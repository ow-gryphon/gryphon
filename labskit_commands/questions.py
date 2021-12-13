import questionary
from questionary import Choice
from labskit_commands.logging import Logging


def get_back_choice():
    return Choice(
        title="<< Go back to the previous menu",
        value="back"
    )


def base_question(function):

    def _f(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            exit(0)

    return _f


@base_question
def get_lib_via_keyboard():
    return questionary.prompt([
        dict(
            type='input',
            name='library_name',
            message='Type the name of the python library you want to install:'
        )
    ])['library_name']


@base_question
def get_lib_category(categories: list):
    categories = categories.copy()
    categories.extend([
        Choice(
            title=">> Type the library name manually",
            value="type"
        ),
        get_back_choice()
    ])
    return questionary.prompt([
        dict(
            type='list',
            name='library_category',
            message='What do you need a library for?',
            choices=categories
        )
    ])['library_category']


@base_question
def get_lib(libraries):
    libraries = libraries.copy()
    libraries.extend([
        Choice(
            title=">> Type the library name manually",
            value="type"
        ),
        get_back_choice()
    ])
    return questionary.prompt([
        dict(
            type='list',
            name='library',
            message='I have the following options:',
            choices=libraries
        )
    ])['library']


@base_question
def main_question():
    command_names = {
        "init": "Start a new project.",
        "generate": "Load template code into an existing project",
        "add": "Install Python libraries/packages",
        "about": "About Gryphon",
        "quit": "   Exit"
    }
    return questionary.prompt([
        dict(
            type='list',
            name='command',
            message='What would you like to do? (Use arrow keys to select your option and press Enter)',
            choices=[
                Choice(
                    title=display_question,
                    value=command
                )
                for command, display_question in command_names.items()
            ]
        )
    ])['command']


@base_question
def ask_which_template(metadata, command="init"):
    options = list(metadata.keys())
    options.append(get_back_choice())

    if command == "generate":
        questions = generate_1(options)
        responses = questionary.prompt(questions)
        return responses['template']

    elif command == "init":
        questions = init_1(options)
        template = questionary.prompt(questions[0])['template']
        if template == "back":
            return "back", None

        location = questionary.prompt(questions[1])['location']
        return template, location


@base_question
def ask_extra_arguments(arguments: list, command="init"):
    arguments = arguments.copy()
    # arguments.append(get_back_choice())
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


def generate_1(options):
    return [
        dict(
            type='list',
            name='template',
            message='Please select the template code you would to load:',
            choices=options
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


def init_1(options) -> list:
    return [
        dict(
            type='list',
            name='template',
            message='Please select the template you would like to use:',
            choices=options
        ),
        dict(
            type='input',
            name='location',
            message='Please give your project folder a name:',
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
