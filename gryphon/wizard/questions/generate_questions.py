import questionary
from questionary import Choice, Separator
from .common_functions import base_question, get_back_choice
from ..wizard_text import Text
from ...constants import (QUIT, YES, NO, TYPE_AGAIN)


class GenerateQuestions:

    @staticmethod
    @base_question
    def get_generate_option(categories: list):
        categories = categories.copy()
        categories.extend([
            Separator(Text.menu_separator),
            get_back_choice()
        ])

        return questionary.select(
            message=Text.add_prompt_categories_question,
            choices=categories,
            instruction=Text.add_prompt_instruction
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_which_template(metadata):
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

        return questionary.select(
            message=Text.generate_prompt_template_question,
            choices=options
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_extra_arguments(arguments: list):
        extra_questions = [
            dict(
                type='input',
                name=field['name'],
                message=field['help']
            )
            for field in arguments
        ]
        return questionary.unsafe_prompt(extra_questions)

    @staticmethod
    @base_question
    def confirm_generate(template_name, **kwargs):

        information = Text.generate_confirm_1.replace("{template_name}", template_name)
        information += (
            Text.generate_confirm_2.replace("{arguments}", str(kwargs))
            if len(kwargs) else ""
        )

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

        return questionary.select(
            message=information,
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def generate_keyword_question():
        return questionary.text(message=Text.generate_keyword_argument).unsafe_ask()

    @staticmethod
    @base_question
    def nothing_found():
        choices = [
            get_back_choice(),
            Choice(
                title="Quit",
                value=QUIT
            ),
        ]

        return questionary.select(
            message=Text.could_not_find_any_templates,
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def nothing_found_typing():
        choices = [
            Choice(
                title="Try another keyword",
                value=TYPE_AGAIN
            ),
            Separator(),
            get_back_choice(),
            Choice(
                title="Quit",
                value=QUIT
            ),
        ]

        return questionary.select(
            message=Text.could_not_find_any_templates,
            choices=choices
        ).unsafe_ask()
