import questionary
from questionary import Choice, Separator
from .common_functions import base_question, get_back_choice, logger
from ..functions import wrap_text
from ..wizard_text import Text
from ...constants import (TYPING, SHORT_DESC, LONG_DESC, NAME, REFERENCE_LINK, YES, NO)


class AddQuestions:

    @staticmethod
    @base_question
    def get_lib_via_keyboard():
        return questionary.text(message=Text.add_prompt_type_library).unsafe_ask()

    @staticmethod
    @base_question
    def get_add_option(categories: list):
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
            get_back_choice()
        ])
        return questionary.select(
            message=Text.add_prompt_categories_question,
            choices=categories,
            instruction=Text.add_prompt_instruction,
            use_indicator=True
        ).unsafe_ask()

    @staticmethod
    @base_question
    def confirm_add(library: dict):
        information = ""

        if LONG_DESC in library:
            information += f'\t{library[NAME]}\n\n\t{library[LONG_DESC]}\n'

        if REFERENCE_LINK in library:
            information += f'\n\tReferences: {library[REFERENCE_LINK]}\n'

        wrapped, n_lines = wrap_text(information)

        logger.warning(wrapped)

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
        ).unsafe_ask(), n_lines
