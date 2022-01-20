import questionary
from questionary import Choice, Separator
from ..wizard_text import Text
from ..constants import (BACK, YES, NO)
from .common import base_question, get_back_choice


class InitQuestions:

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

        template = questionary.select(
            message=Text.init_prompt_template_question,
            choices=options
        ).unsafe_ask()

        if template == BACK:
            return BACK, None

        location = questionary.text(message=Text.init_prompt_location_question).unsafe_ask()
        return template, location

    @staticmethod
    @base_question
    def ask_init_location():
        return questionary.text(message=Text.init_prompt_location_question).unsafe_ask()

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
        ).unsafe_ask(), len(message.split('\n'))
