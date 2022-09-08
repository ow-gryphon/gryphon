import questionary
from questionary import Choice, Separator
from .common_functions import base_question, get_back_choice
from ..wizard_text import Text
from ...constants import (
    INIT, INIT_FROM_EXISTING, GENERATE, ADD, HANDOVER, ABOUT, QUIT, SETTINGS, CONFIGURE_PROJECT,
    VALUE, LATEST, REPORT_BUG, FEEDBACK, YES, NO, CONTACT_US
)


class CommonQuestions:

    @staticmethod
    @base_question
    def main_question(inside_existing_project: bool = False):
        choices = [
            Choice(
                title=Text.init_display_option,
                value=INIT
            ),
            Choice(
                title=Text.init_from_existing_display_option,
                value=INIT_FROM_EXISTING
            ),

            Separator(Text.menu_separator),

            Choice(
                title=Text.generate_display_option,
                value=GENERATE
            ),
            Choice(
                title=Text.add_display_option,
                value=ADD
            ),
            Choice(
                title=Text.handover_display_option,
                value=HANDOVER
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
                title=Text.contact_us_display_option,
                value=CONTACT_US
            ),
            Choice(
                title=Text.quit_display_option,
                value=QUIT
            )
        ]

        if inside_existing_project:
            choices.insert(
                5,
                Choice(
                    title=Text.configure_project_display_option,
                    value=CONFIGURE_PROJECT
                )
            )

        return questionary.select(
            message=Text.first_prompt_question,
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def send_feedback():
        choices = [
            Choice(
                title="Send description by email",
                value=YES
            ),
            Choice(
                title="Exit and ignore",
                value=NO
            )
        ]

        return questionary.select(
            message="Gryphon failed for an unexpected reason, do you want to report the issue?",
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def prompt_about(links):

        choices = [
            Choice(
                title=link["title"],
                value=link[VALUE]
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

    @staticmethod
    @base_question
    def ask_template_version(versions):

        choices = [
            Choice(
                title="latest",
                value=LATEST
            )
        ]
        choices.extend([
            Choice(
                title=v,
                value=v
            )
            for v in versions
        ])

        return questionary.select(
            message=Text.settings_ask_template_version,
            choices=choices,
            use_indicator=True
        ).unsafe_ask()
