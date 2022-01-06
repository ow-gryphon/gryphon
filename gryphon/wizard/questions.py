import questionary
from questionary import Choice, Separator
from .text import Text
from .logger import Logging


def base_question(function):
    def _f(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            exit(0)
        except KeyboardInterrupt:
            Logging.log(f'\nOperation cancelled by user\n')
            exit(0)

    return _f


class Questions:

    @staticmethod
    def get_back_choice():
        return Choice(
            title=Text.back_to_previous_menu_option,
            value="back"
        )

    @staticmethod
    @base_question
    def get_lib_via_keyboard():
        return questionary.prompt([
            dict(
                type='input',
                name='library_name',
                message=Text.add_prompt_type_library
            )
        ])['library_name']

    @classmethod
    @base_question
    def get_generate_option(cls, categories: list):
        categories = categories.copy()
        categories.extend([
            Separator(Text.menu_separator),
            cls.get_back_choice()
        ])
        return questionary.unsafe_prompt([
            dict(
                type='list',
                name='category',
                message=Text.add_prompt_categories_question,
                choices=categories,
                instruction=Text.add_prompt_instruction
            )
        ])['category']

    @classmethod
    @base_question
    def get_add_option(cls, categories: list):
        categories = categories.copy()
        categories.extend([
            Separator(Text.menu_separator),
            Choice(
                title=Text.type_library_name_menu_option,
                value="type"
            ),
            cls.get_back_choice()
        ])
        return questionary.unsafe_prompt([
            dict(
                type='list',
                name='library_category',
                message=Text.add_prompt_categories_question,
                choices=categories,
                instruction=Text.add_prompt_instruction
            )
        ])['library_category']

    @staticmethod
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

        return questionary.unsafe_prompt([
            dict(
                type='list',
                name='command',
                message=Text.first_prompt_question,
                choices=choices,
                instruction=Text.first_prompt_question
            )
        ])['command']

    @classmethod
    @base_question
    def ask_which_template(cls, metadata, command="init"):
        options = [
            Choice(
                title=template.display_name,
                value=name
            )
            for name, template in metadata.items()
        ]
        options.extend([
            Separator(Text.menu_separator),
            cls.get_back_choice()
        ])

        if command == "generate":
            questions = cls.generate_1(options)
            responses = questionary.unsafe_prompt(questions)
            return responses['template']

        elif command == "init":
            questions = cls.init_1(options)
            template = questionary.unsafe_prompt(questions[0])['template']
            if template == "back":
                return "back", None

            location = questionary.unsafe_prompt(questions[1])['location']
            return template, location

    @classmethod
    @base_question
    def ask_extra_arguments(cls, arguments: list, command="init"):
        arguments = arguments.copy()
        if command == "generate":
            extra_questions = cls.generate_2(arguments)
            return questionary.unsafe_prompt(extra_questions)

        elif command == "init":
            extra_questions = cls.init_2(arguments)
            return questionary.unsafe_prompt(extra_questions)

    @classmethod
    @base_question
    def prompt_about(cls):
        choices = [
            Choice(
                title="Google",
                value="https://www.google.com/"
            ),
            Choice(
                title="Yahoo",
                value="https://www.yahoo.com/"
            ),
            Separator(Text.menu_separator),
            cls.get_back_choice(),
            Choice(
                title="Quit",
                value="quit"
            ),
        ]

        return questionary.select(
            message=Text.about_prompt_links,
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_init_location():
        return questionary.text(
            message=Text.init_prompt_location_question
        ).ask()

    @staticmethod
    @base_question
    def confirmation(message=None):
        message = Text.base_confirmation if message is None else message
        go_ahead = questionary.confirm(message=message).ask()
        if not go_ahead:
            exit(0)

    @classmethod
    @base_question
    def prompt_about(cls):
        choices = [
            Choice(
                title="Google",
                value="https://www.google.com/"
            ),
            Choice(
                title="Yahoo",
                value="https://www.yahoo.com/"
            ),
            Separator(Text.menu_separator),
            cls.get_back_choice(),
            Choice(
                title="Quit",
                value="quit"
            ),
        ]

        return questionary.select(
            message=Text.about_prompt_links,
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def confirm_init(template_name, template_description, location, **kwargs):

        message = (
            f"\n{template_description}\n" +
            Text.init_confirm_1
            .replace("{template_name}", template_name)
            .replace("{location}", str(location))
        )

        if kwargs:
            message = message + Text.init_confirm_2.replace("{arguments}", kwargs)

        return questionary.select(
            message=message,
            choices=[
                Choice(
                    title="Yes",
                    value="yes"
                ),
                Choice(
                    title="No",
                    value="no"
                ),
                Choice(
                    title="Change project location",
                    value="change_location"
                )
            ]
        ).unsafe_ask()

    @classmethod
    def confirm_generate(cls, template_name, **kwargs):
        cls.confirmation(
            Text.generate_confirm
                .replace("{template_name}", template_name)
                .replace("{arguments}", str(kwargs))
        )

    @classmethod
    def confirm_add(cls, library_name):
        cls.confirmation(
            Text.add_confirm.replace("{library_name}", library_name)
        )

    @staticmethod
    def generate_1(options):
        return [
            dict(
                type='list',
                name='template',
                message=Text.generate_prompt_template_question,
                choices=options
            )
        ]

    @staticmethod
    def generate_2(arguments):
        return [
            dict(
                type='input',
                name=field['name'],
                message=field['help']
            )
            for field in arguments
        ]

    @staticmethod
    @base_question
    def generate_keyword_question():
        return questionary.text(
            message="Type the keyword you want to search for:",
        ).unsafe_ask()

    @classmethod
    @base_question
    def nothing_found(cls):
        choices = [
            Separator("\nCould not find any template with the given keyword"),
            cls.get_back_choice(),
            Choice(
                title="Quit",
                value="quit"
            ),
        ]

        return questionary.select(
            message=Text.about_prompt_links,
            choices=choices
        ).unsafe_ask()

    @staticmethod
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

    @staticmethod
    def init_2(arguments):
        return [
            dict(
                type='input',
                name=field['name'],
                message=field['help']
            )
            for field in arguments
        ]
