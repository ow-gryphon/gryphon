import questionary
from questionary import Choice, Separator
from labskit_commands.logging import Logging
from labskit_commands.text import Text


def get_back_choice():
    return Choice(
        title=Text.back_to_previous_menu_option,
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
            message=Text.add_prompt_type_library
        )
    ])['library_name']


@base_question
def get_lib_category(categories: list):
    categories = categories.copy()
    categories.extend([
        Separator(Text.menu_separator),
        Choice(
            title=Text.type_library_name_menu_option,
            value="type"
        ),
        get_back_choice()
    ])
    return questionary.prompt([
        dict(
            type='list',
            name='library_category',
            message=Text.add_prompt_categories_question,
            choices=categories,
            instruction=Text.add_prompt_instruction
        )
    ])['library_category']


@base_question
def main_question():
    choices = [
        Choice(
            title=Text.init_display_option,
            value="init"
        ),
        Choice(
            title=Text.generate_display_option,
            value="generate"
        ),
        Choice(
            title=Text.add_display_option,
            value="add"
        ),
        Separator(Text.menu_separator),
        Choice(
            title=Text.about_display_option,
            value="about"
        ),
        Choice(
            title=Text.quit_display_option,
            value="quit"
        )
    ]

    return questionary.prompt([
        dict(
            type='list',
            name='command',
            message=Text.first_prompt_question,
            choices=choices,
            instruction=Text.first_prompt_question
        )
    ])['command']


@base_question
def ask_which_template(metadata, command="init"):
    options = [
        Choice(
            title=template.display_name,
            value=name
        )
        for name, template in metadata.items()
    ]
    options.extend([
        Separator(Text.menu_separator),
        get_back_choice()
    ])

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
            message=Text.generate_prompt_template_question,
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
            message=Text.init_prompt_template_question,
            choices=options
        ),
        dict(
            type='input',
            name='location',
            message=Text.init_prompt_location_question
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
