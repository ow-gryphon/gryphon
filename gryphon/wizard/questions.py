import logging
import questionary
from questionary import Choice, Separator
from .wizard_text import Text
from .constants import (
    TYPING, BACK, SHORT_DESC, LONG_DESC, NAME, REFERENCE_LINK,
    QUIT, INIT, ADD, ABOUT, GENERATE, YES, NO
)


logger = logging.getLogger('gryphon')


def base_question(function):
    def _f(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyboardInterrupt:
            logger.warning(f'\nOperation cancelled by user\n')
            exit(0)

    return _f


class Questions:

    @staticmethod
    def get_back_choice():
        return Choice(
            title=Text.back_to_previous_menu_option,
            value=BACK
        )

    @staticmethod
    @base_question
    def get_lib_via_keyboard():
        return questionary.text(message=Text.add_prompt_type_library).unsafe_ask()

    @classmethod
    @base_question
    def get_generate_option(cls, categories: list):
        categories = categories.copy()
        categories.extend([
            Separator(Text.menu_separator),
            cls.get_back_choice()
        ])

        return questionary.select(
            message=Text.add_prompt_categories_question,
            choices=categories,
            instruction=Text.add_prompt_instruction
        ).unsafe_ask()

    @classmethod
    @base_question
    def get_add_option(cls, categories: list):
        categories = [
            Choice(
                title=item[NAME] + (
                    f' - {item[SHORT_DESC]}'
                    if item.get(SHORT_DESC, False)
                    else ""
                ),
                value=item[NAME]
            )
            for item in categories
        ]

        categories.extend([
            Separator(Text.menu_separator),
            Choice(
                title=Text.type_library_name_menu_option,
                value=TYPING
            ),
            cls.get_back_choice()
        ])
        return questionary.select(
            message=Text.add_prompt_categories_question,
            choices=categories,
            instruction=Text.add_prompt_instruction,
            use_indicator=True
        ).unsafe_ask()

    @staticmethod
    @base_question
    def main_question():
        choices = [
            Choice(
                title=Text.init_display_option,
                value=INIT
            ),
            Choice(
                title=Text.generate_display_option,
                value=GENERATE
            ),
            Choice(
                title=Text.add_display_option,
                value=ADD
            ),
            Separator(Text.menu_separator),
            Choice(
                title=Text.about_display_option,
                value=ABOUT
            ),
            Choice(
                title=Text.quit_display_option,
                value=QUIT
            )
        ]

        return questionary.select(
            message=Text.first_prompt_question,
            choices=choices,
            instruction=Text.first_prompt_question
        ).unsafe_ask()

    @classmethod
    @base_question
    def ask_which_template(cls, metadata, command=INIT):
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

        if command == GENERATE:

            return questionary.select(
                message=Text.generate_prompt_template_question,
                choices=options
            ).unsafe_ask()

        elif command == INIT:

            template = questionary.select(
                message=Text.init_prompt_template_question,
                choices=options
            ).unsafe_ask()

            if template == BACK:
                return BACK, None

            location = questionary.text(message=Text.init_prompt_location_question).unsafe_ask()
            return template, location

    @classmethod
    @base_question
    def ask_extra_arguments(cls, arguments: list):
        extra_questions = [
            dict(
                type='input',
                name=field['name'],
                message=field['help']
            )
            for field in arguments
        ]
        return questionary.unsafe_prompt(extra_questions)

    @classmethod
    @base_question
    def prompt_about(cls, links):

        choices = [
            Choice(
                title=link["title"],
                value=link["value"]
            )
            for link in links
        ]
        choices.append(Separator(Text.menu_separator))
        choices.append(cls.get_back_choice())
        choices.append(
            Choice(
                title="Quit",
                value=QUIT
            )
        )

        return questionary.select(
            message=Text.about_prompt_links,
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_init_location():
        return questionary.text(message=Text.init_prompt_location_question).unsafe_ask()

    @staticmethod
    @base_question
    def confirmation(message=None):
        message = Text.base_confirmation if message is None else message
        go_ahead = questionary.confirm(message=message).ask()
        if not go_ahead:
            exit(0)

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
                    value=YES
                ),
                Choice(
                    title="No",
                    value=NO
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
            Text.generate_confirm_1.replace("{template_name}", template_name) +
            (
                Text.generate_confirm_2.replace("{arguments}", str(kwargs))
                if len(kwargs) else ""
            )
        )

    @classmethod
    @base_question
    def confirm_add(cls, library: dict):
        information = ""

        if LONG_DESC in library:
            information += f'\n\t{library[NAME]}\n\n\t{library[LONG_DESC]}\n'

        if REFERENCE_LINK in library:
            information += f'\n\tReferences: {library[REFERENCE_LINK]}\n'

        logger.warning(information)

        choices = [
            Choice(
                title="Yes",
                value=YES
            ),
            Choice(
                title="No",
                value=NO
            )
        ]

        if REFERENCE_LINK in library:
            choices.append(
                Choice(
                    title=f"See library docs (\"{library[REFERENCE_LINK]}\").",
                    value=library[REFERENCE_LINK]
                )
            )

        return questionary.select(
            message=Text.add_confirm.replace("{library_name}", library[NAME]),
            choices=choices
        ).unsafe_ask(), len(information.split("\n"))

    @staticmethod
    @base_question
    def generate_keyword_question():
        return questionary.text(message=Text.generate_keyword_argument).unsafe_ask()

    @classmethod
    @base_question
    def nothing_found(cls):
        choices = [
            cls.get_back_choice(),
            Choice(
                title="Quit",
                value=QUIT
            ),
        ]

        return questionary.select(
            message=Text.could_not_find_any_templates,
            choices=choices
        ).unsafe_ask()
