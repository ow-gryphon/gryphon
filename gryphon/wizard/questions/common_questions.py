import questionary
from questionary import Choice, Separator
from .common_functions import base_question, get_back_choice
from ..wizard_text import Text
from ...constants import (INIT, ADD, ABOUT, GENERATE, QUIT, SETTINGS)


class CommonQuestions:

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
                title=Text.settings_display_option,
                value=SETTINGS
            ),
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
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def prompt_about(links):

        choices = [
            Choice(
                title=link["title"],
                value=link["value"]
            )
            for link in links
        ]
        choices.append(Separator(Text.menu_separator))
        choices.append(get_back_choice())
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
