import questionary
from questionary import Choice, Separator

from .common_functions import base_question, base_text_prompt, get_back_choice, logger
from ..functions import wrap_text
from ..wizard_text import Text
from ...constants import (YES, NO, SYSTEM_DEFAULT, READ_MORE, CHANGE_LOCATION)


class InitQuestions:

    @staticmethod
    @base_question
    def ask_which_template(metadata):
        options = [
            Choice(
                title=f"{template.display_name} ({template.registry_type})",
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

        return template

    @staticmethod
    @base_text_prompt
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
    def confirm_init(template, location, read_more_option=False, **kwargs):

        n_lines = 0
        if template.description:
            text, n_lines = wrap_text(f"{template.description}\n")
            logger.warning(text)

        message = (
            Text.init_confirm_1
            .replace("{template_name}", template.display_name)
            .replace("{location}", str(location))
        )

        if kwargs:
            message = message + Text.init_confirm_2.replace("{arguments}", kwargs)

        n_lines += len(message.split('\n'))

        options = [
            Choice(
                title="Yes",
                value=YES
            ),
            Choice(
                title="No",
                value=NO
            )
        ]
        if read_more_option:
            options.append(
                Choice(
                    title="Read more",
                    value=READ_MORE
                )
            )

        options.append(
            Choice(
                title="Change project location",
                value=CHANGE_LOCATION
            )
        )
        return questionary.select(
            message=message,
            choices=options
        ).unsafe_ask(), n_lines

    @staticmethod
    @base_question
    def ask_just_location():
        return (
            questionary
            .text(message=Text.init_prompt_location_question)
            .unsafe_ask()
        )

    @staticmethod
    @base_question
    def ask_python_version(versions):

        choices = [
            Choice(
                title=Text.settings_python_use_system_default,
                value=SYSTEM_DEFAULT
            )
        ]
        choices.extend([
            Choice(
                title=v,
                value=v
            )
            for v in versions
        ])

        choices.extend([
            Separator(),
            get_back_choice()
        ])

        return questionary.select(
            message=Text.settings_ask_python_version,
            choices=choices,
            use_indicator=True
        ).unsafe_ask()
